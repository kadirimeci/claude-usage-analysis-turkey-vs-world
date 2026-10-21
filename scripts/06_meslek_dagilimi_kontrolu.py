from pathlib import Path
import pandas as pd

# Ham veri dosyasını oku
proje = Path(__file__).resolve().parent.parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"

veri = pd.read_csv(dosya, low_memory=False)

# Türkiye - Mayıs 2026 - ana meslek grupları
meslekler = veri[
    (veri["date_start"] == "2026-05-01")
    & (veri["geo_level"] == "country")
    & (veri["geo_id"] == "TUR")
    & (veri["category_name"] == "soc_occupation")
    & (veri["hierarchy_level"] == 1)
    & (veri["metric_id"] == "pct")
].copy()

# Büyükten küçüğe sırala
meslekler = meslekler.sort_values(
    "value", ascending=False
)

print("\n--- TÜRKİYE MAYIS 2026: ANA MESLEK GRUPLARI ---")
print(
    meslekler[
        ["node_name", "node_external_id", "value"]
    ].to_string(index=False)
)

print("\n--- KONTROL SONUÇLARI ---")
print(f"Meslek grubu sayısı: {len(meslekler)}")
print(f"Toplam pay: %{meslekler['value'].sum():.2f}")
print(f"Tekrarlanan meslek kodu: {meslekler['node_external_id'].duplicated().sum()}")
print(f"Eksik değer: {meslekler['value'].isna().sum()}")
