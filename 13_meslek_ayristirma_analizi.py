# Nisan ve Mayıs 2026 için iş amaçlı kullanım farkının simetrik Kitagawa ayrıştırması.
# Ortak meslek kategorileri her bölge ve ay için kendi içinde %100'e normalize edilir.
from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent
veri = pd.read_csv(proje / 'outputs' / 'meslek_kullanim_profili_2026.csv', dtype={'occupation_code': str})
zorunlu = {'date_start', 'bolge', 'occupation_code', 'occupation_name', 'usage_pct', 'work_pct'}
assert zorunlu.issubset(veri.columns), f'Eksik sütunlar: {zorunlu - set(veri.columns)}'
sonuclar = []
ozetler = []
for tarih in ('2026-04-01', '2026-05-01'):
    donem = veri.loc[veri['date_start'] == tarih]
    tr = donem.loc[donem['bolge'] == 'Türkiye', ['occupation_code','occupation_name','usage_pct','work_pct']]
    dw = donem.loc[donem['bolge'] == 'Dünya', ['occupation_code','usage_pct','work_pct']]
    ortak = tr.merge(dw, on='occupation_code', suffixes=('_tr','_global'), validate='one_to_one')
    assert len(ortak) == 20, f'{tarih}: Beklenen 20 ortak kategori, bulunan {len(ortak)}'
    assert ortak[['usage_pct_tr','usage_pct_global','work_pct_tr','work_pct_global']].notna().all().all()
    ortak['agirlik_tr'] = ortak['usage_pct_tr'] / ortak['usage_pct_tr'].sum()
    ortak['agirlik_global'] = ortak['usage_pct_global'] / ortak['usage_pct_global'].sum()
    ortak['is_orani_tr'] = ortak['work_pct_tr'] / 100
    ortak['is_orani_global'] = ortak['work_pct_global'] / 100
    ortak['dagilim_etkisi'] = (ortak['agirlik_tr'] - ortak['agirlik_global']) * (ortak['is_orani_tr'] + ortak['is_orani_global']) * 50
    ortak['kategori_ici_etki'] = (ortak['is_orani_tr'] - ortak['is_orani_global']) * (ortak['agirlik_tr'] + ortak['agirlik_global']) * 50
    ortak['toplam_etki'] = ortak['dagilim_etkisi'] + ortak['kategori_ici_etki']
    tr_oran = (ortak['agirlik_tr'] * ortak['work_pct_tr']).sum()
    dw_oran = (ortak['agirlik_global'] * ortak['work_pct_global']).sum()
    fark = tr_oran - dw_oran
    assert abs(ortak['toplam_etki'].sum() - fark) < 1e-8
    ortak.insert(0, 'date_start', tarih)
    sonuclar.append(ortak)
    ozetler.append({'date_start': tarih, 'ortak_meslek_sayisi':len(ortak), 'turkiye_is_pct':tr_oran, 'dunya_is_pct':dw_oran, 'toplam_fark':fark, 'dagilim_etkisi':ortak['dagilim_etkisi'].sum(), 'kategori_ici_etki':ortak['kategori_ici_etki'].sum(), 'kontrol_hatasi':fark-ortak['toplam_etki'].sum()})

cikti = proje / 'outputs'
cikti.mkdir(exist_ok=True)
pd.concat(sonuclar, ignore_index=True).to_csv(cikti / 'meslek_ayristirma_2026_iki_ay.csv', index=False, encoding='utf-8-sig')
pd.DataFrame(ozetler).to_csv(cikti / 'meslek_ayristirma_2026_ozet.csv', index=False, encoding='utf-8-sig')
print(pd.DataFrame(ozetler).round(4).to_string(index=False))
print('İki dönem için ayrıştırma tamamlandı; eski meslek_ayristirma_2026.csv değiştirilmedi.')
