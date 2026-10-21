# Analiz çıktı dosyalarında dönem, anahtar tekilliği, toplam ve ayrıştırma tutarlılığını denetler.
from pathlib import Path
import pandas as pd

kok = Path(__file__).resolve().parent
out = kok / 'outputs'
kontroller = [
    ('meslek_kullanim_profili_2026.csv', ['date_start','bolge','occupation_code'], 84),
    ('meslek_cikti_profili_2026.csv', ['date_start','bolge','occupation_code','artifact_code'], 2688),
    ('cikti_turleri_2026.csv', ['date_start','bolge','artifact_code'], 128),
    ('meslek_ayristirma_2026_iki_ay.csv', ['date_start','occupation_code'], 40),
]
for ad, anahtar, beklenen in kontroller:
    df = pd.read_csv(out / ad)
    assert len(df) == beklenen, f'{ad}: {len(df)} satır; beklenen {beklenen}'
    assert df[anahtar].notna().all().all(), f'{ad}: anahtarda boş değer'
    assert not df.duplicated(anahtar).any(), f'{ad}: tekrarlanan anahtar'
    assert set(df['date_start'].astype(str)) == {'2026-04-01','2026-05-01'}, f'{ad}: beklenmeyen dönem'
    print(f'OK: {ad}: {len(df)} satır')

cikti = pd.read_csv(out / 'meslek_cikti_profili_2026.csv')
toplam = cikti.groupby(['date_start','bolge','occupation_code'])['artifact_pct'].sum()
assert toplam.between(99.8, 100.2).all(), 'Meslek çıktı yüzdeleri ~100 değil'

ozet = pd.read_csv(out / 'meslek_ayristirma_2026_ozet.csv')
assert (ozet['kontrol_hatasi'].abs() < 1e-8).all(), 'Ayrıştırma toplamı tutarsız'
print('Tüm kontroller geçti.')
