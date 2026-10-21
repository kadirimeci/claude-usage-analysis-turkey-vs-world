from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)


def oku(dosya, kolonlar, satir):
    df = pd.read_csv(ROOT / dosya, encoding='utf-8-sig')
    eksik = set(kolonlar) - set(df.columns)
    if eksik:
        raise ValueError(f'{dosya}: eksik sütunlar: {sorted(eksik)}')
    if len(df) != satir:
        raise ValueError(f'{dosya}: {satir} satır bekleniyor, {len(df)} bulundu')
    return df


def kaydet(df, ad):
    df.to_csv(OUT / ad, index=False, encoding='utf-8-sig', float_format='%.6f')


a = oku('adim24_cikti_ayristirma.csv', ['date_start', 'artifact_code', 'turkiye_oran', 'dunya_oran', 'dagilim_etkisi', 'kategori_ici_etki', 'toplam_fark', 'kontrol_farki', 'ortak_meslek_sayisi'], 64)
k = oku('adim25_kapsam.csv', ['date_start', 'bolge', 'artifact_code', 'genel_oran', 'meslek_agirlikli_oran', 'kapsam_farki', 'meslek_sayisi'], 128)
o = oku('adim26_otomasyon.csv', ['date_start', 'occupation_name', 'turkiye_otomasyon', 'dunya_otomasyon', 'otomasyon_farki', 'turkiye_kullanim_payi', 'dunya_kullanim_payi'], 40)

for df in (a, k, o):
    df['date_start'] = pd.to_datetime(df['date_start']).dt.strftime('%Y-%m')
    if df.isna().any().any():
        raise ValueError('Girdi dosyalarından birinde eksik değer var')

if a.duplicated(['date_start', 'artifact_code']).any() or k.duplicated(['date_start', 'bolge', 'artifact_code']).any() or o.duplicated(['date_start', 'occupation_name']).any():
    raise ValueError('Bir veya daha fazla tabloda tekrarlanan anahtar bulundu')

if (a['ortak_meslek_sayisi'] != 20).any():
    raise ValueError('Çıktı ayrıştırmasında ortak meslek sayısı 20 değil')

hata = (a['dagilim_etkisi'] + a['kategori_ici_etki'] - a['toplam_fark']).abs().max()
if hata > 0.0003 or (a['toplam_fark'] - a['kontrol_farki']).abs().max() > 0.0003:
    raise ValueError(f'Ayrıştırma kontrolünde tutarsızlık: {hata}')

a['mutlak_fark'] = a['toplam_fark'].abs()
a['baskin_etki'] = a.apply(lambda r: 'Kategori içi' if abs(r['kategori_ici_etki']) > abs(r['dagilim_etkisi']) else ('Dağılım' if abs(r['dagilim_etkisi']) > abs(r['kategori_ici_etki']) else 'Eşit'), axis=1)
kaydet(a.sort_values(['date_start', 'mutlak_fark'], ascending=[True, False]), '01_cikti_tum_ayristirmalar.csv')

pivot = a.pivot(index='artifact_code', columns='date_start', values='toplam_fark')
if set(pivot.columns) != {'2026-04', '2026-05'}:
    raise ValueError('Nisan ve Mayıs dönemleri bulunamadı')
t = pivot.rename(columns={'2026-04': 'nisan_farki', '2026-05': 'mayis_farki'}).reset_index()
t['fark_degisim'] = t['mayis_farki'] - t['nisan_farki']
t['ayni_yon'] = (t['nisan_farki'] * t['mayis_farki'] > 0)
t['iki_ay_ortalama_mutlak_fark'] = (t['nisan_farki'].abs() + t['mayis_farki'].abs()) / 2
t['oncelik'] = t.apply(lambda r: 'Güçlü ve tutarlı' if r['ayni_yon'] and min(abs(r['nisan_farki']), abs(r['mayis_farki'])) >= 0.5 else 'Küçük/değişken fark', axis=1)
t = t.sort_values('iki_ay_ortalama_mutlak_fark', ascending=False)
kaydet(t, '02_cikti_donemsel_tutarlilik.csv')

k['hesap_kontrolu'] = k['genel_oran'] - k['meslek_agirlikli_oran']
k['hesap_hatasi'] = k['hesap_kontrolu'] - k['kapsam_farki']
if k['hesap_hatasi'].abs().max() > 0.0002:
    raise ValueError('Kapsam tablosunda hesap tutarsızlığı')
kaydet(k.sort_values(['date_start', 'bolge', 'kapsam_farki'], ascending=[True, True, False]), '03_kapsam_detay.csv')
ko = k.groupby(['date_start', 'bolge'], as_index=False).agg(genel_toplam=('genel_oran', 'sum'), meslek_agirlikli_toplam=('meslek_agirlikli_oran', 'sum'), toplam_fark=('kapsam_farki', 'sum'), meslek_sayisi=('meslek_sayisi', 'first'))
kaydet(ko, '04_kapsam_ozeti.csv')

o['agirlik_ortalama'] = (o['turkiye_kullanim_payi'] + o['dunya_kullanim_payi']) / 2
o['agirlik_farki'] = o['turkiye_kullanim_payi'] - o['dunya_kullanim_payi']
o['otomasyon_ortalama'] = (o['turkiye_otomasyon'] + o['dunya_otomasyon']) / 2
for donem, ix in o.groupby('date_start').groups.items():
    toplam_tr = o.loc[ix, 'turkiye_kullanim_payi'].sum()
    toplam_dw = o.loc[ix, 'dunya_kullanim_payi'].sum()
    o.loc[ix, 'tr_agirlik'] = o.loc[ix, 'turkiye_kullanim_payi'] / toplam_tr
    o.loc[ix, 'dw_agirlik'] = o.loc[ix, 'dunya_kullanim_payi'] / toplam_dw

o['dagilim_katkisi'] = (o['tr_agirlik'] - o['dw_agirlik']) * (o['turkiye_otomasyon'] + o['dunya_otomasyon']) / 2
o['kategori_ici_katkisi'] = (o['tr_agirlik'] + o['dw_agirlik']) / 2 * o['otomasyon_farki']
o['toplam_katki'] = o['dagilim_katkisi'] + o['kategori_ici_katkisi']
o['mutlak_katki'] = o['toplam_katki'].abs()
kaydet(o.sort_values(['date_start', 'mutlak_katki'], ascending=[True, False]), '05_otomasyon_meslek_katkilari.csv')

ozet = o.groupby('date_start', as_index=False).agg(dagilim_etkisi=('dagilim_katkisi', 'sum'), kategori_ici_etki=('kategori_ici_katkisi', 'sum'), toplam_fark=('toplam_katki', 'sum'))
ozet['kontrol_turkiye'] = o.groupby('date_start').apply(lambda x: (x['tr_agirlik'] * x['turkiye_otomasyon']).sum(), include_groups=False).to_numpy()
ozet['kontrol_dunya'] = o.groupby('date_start').apply(lambda x: (x['dw_agirlik'] * x['dunya_otomasyon']).sum(), include_groups=False).to_numpy()
ozet['kontrol_hatasi'] = ozet['toplam_fark'] - (ozet['kontrol_turkiye'] - ozet['kontrol_dunya'])
if ozet['kontrol_hatasi'].abs().max() > 0.00001:
    raise ValueError('Otomasyon ayrıştırma kontrolünde tutarsızlık')
kaydet(ozet, '06_otomasyon_ayristirma_ozeti.csv')

lines = [
    '# Türkiye–Dünya Claude Kullanımı | Toplu Analiz',
    '',
    'Dönem: Nisan–Mayıs 2026. Veriler Claude etkileşimlerini ve mesleki görev sınıflandırmalarını temsil eder; nüfus geneli veya çalışan meslekleri hakkında doğrudan çıkarım yapılamaz.',
    '',
    '## Veri kontrolleri',
    f'- Çıktı ayrıştırması: {len(a)} satır, {a.artifact_code.nunique()} çıktı türü; maksimum ayrıştırma yuvarlama hatası {hata:.6f} yüzde puan.',
    f'- Kapsam karşılaştırması: {len(k)} satır.',
    f'- Otomasyon karşılaştırması: {len(o)} satır, {o.occupation_name.nunique()} ortak meslek kategorisi.',
    f'- İki ayda aynı işaretli çıktı farkı: {int(t.ayni_yon.sum())}/{len(t)}. Çok küçük değerlerde işaret değişimi pratik önem taşımayabilir.',
    '',
    '## Çıktı türleri: iki ayda en yüksek ortalama mutlak farklar',
]
for _, r in t.head(10).iterrows():
    lines.append(f"- {r['artifact_code']}: Nisan {r['nisan_farki']:+.4f}, Mayıs {r['mayis_farki']:+.4f} yüzde puan; {r['oncelik']}.")
lines += ['', '## Çıktı ayrıştırması', '']
for month, g in a.groupby('date_start'):
    n = (g['baskin_etki'] == 'Kategori içi').sum()
    lines.append(f'- {month}: 32 çıktı türünün {n} tanesinde mutlak kategori içi etki, mutlak dağılım etkisinden büyük.')
lines += ['', '## Meslek kapsamı', '']
for _, r in ko.iterrows():
    lines.append(f"- {r['date_start']} {r['bolge']}: genel çıktı toplamı {r['genel_toplam']:.3f}%, mesleklerden ağırlıklı toplam {r['meslek_agirlikli_toplam']:.3f}%, fark {r['toplam_fark']:.3f} puan ({int(r['meslek_sayisi'])} kategori).")
lines += ['', '## Otomasyon ayrıştırması', '']
for _, r in ozet.iterrows():
    lines.append(f"- {r['date_start']}: Türkiye {r['kontrol_turkiye']:.4f}%, dünya {r['kontrol_dunya']:.4f}%; fark {r['toplam_fark']:+.4f} puan; dağılım {r['dagilim_etkisi']:+.4f}, kategori içi {r['kategori_ici_etki']:+.4f} puan.")
    alt = o[o.date_start == r['date_start']].sort_values('toplam_katki', ascending=False)
    lines.append('  - Pozitif katkısı en yüksek 3 kategori: ' + '; '.join(f"{x.occupation_name} ({x.toplam_katki:+.3f})" for x in alt.head(3).itertuples()) + '.')
    lines.append('  - Negatif katkısı en yüksek 3 kategori: ' + '; '.join(f"{x.occupation_name} ({x.toplam_katki:+.3f})" for x in alt.tail(3).itertuples()) + '.')
lines += ['', '## Metodolojik notlar', '- Ayrıştırmalar 20 ortak meslek kategorisi üzerinde, her bölge ve ay için ayrı ayrı %100’e normalize edilen ağırlıklarla hesaplanır.', '- Ayrıştırma terimleri matematiksel katkılardır, nedensel etki değildir.', '- Meslek temelli çıktı toplamları ile genel çıktı oranları aynı kapsamda değildir; farkları doğrudan belirli eksik mesleklere atfetmeyin.', '- Kategorilerin kullanım oranları ve otomasyon oranları kaynakta iki ondalığa yuvarlanmış olduğundan hesaplarda küçük sapmalar beklenir.', '- İşaret tutarlılığı istatistiksel anlamlılık kanıtı değildir; bu dosyalarda örneklem büyüklüğü ve belirsizlik aralıkları yoktur.', '- Bu paket yalnızca 24–26. adımlardan elde edilen CSV dosyalarını kullanır. Diğer analizlerin ham tablolarını içermediği için yeni görev/amaç çapraz analizleri üretilmez.']
(OUT / '07_TOPLU_ANALIZ_RAPORU.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Analiz tamamlandı. 7 çıktı dosyası:', OUT)
for f in sorted(OUT.iterdir()):
    print(' -', f.name)
