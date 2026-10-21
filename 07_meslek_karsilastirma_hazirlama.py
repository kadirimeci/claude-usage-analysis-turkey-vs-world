from pathlib import Path
import pandas as pd

# Dosya konumları
proje = Path(__file__).resolve().parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

veri = pd.read_csv(dosya, low_memory=False)

# Ana meslek gruplarının kullanım payları
meslekler = veri[
    (veri["category_name"] == "soc_occupation")
    & (veri["hierarchy_level"] == 1)
    & (veri["metric_id"] == "pct")
    & (
        ((veri["geo_level"] == "country")
         & (veri["geo_id"] == "TUR"))
        | (veri["geo_level"] == "global")
    )
].copy()

# Coğrafi grupları isimlendir
meslekler["bolge"] = meslekler["geo_level"].map({
    "country": "Türkiye",
    "global": "Dünya"
})

# Karşılaştırma tablosu
tablo = meslekler[
    [
        "date_start",
        "bolge",
        "node_external_id",
        "node_name",
        "value"
    ]
].rename(columns={
    "node_external_id": "occupation_code",
    "node_name": "occupation_name",
    "value": "usage_pct"
})

# Aynı meslek ve dönemde mükerrer kayıt kontrolü
anahtar = [
    "date_start",
    "bolge",
    "occupation_code"
]

assert not tablo.duplicated(anahtar).any(), (
    "Tekrarlanan meslek kaydı bulundu!"
)

# CSV olarak kaydet
cikti = cikti_klasoru / "meslek_karsilastirma_2026.csv"
tablo.to_csv(cikti, index=False, encoding="utf-8-sig")

print("\n--- MESLEK KARŞILAŞTIRMA TABLOSU ---")
print(f"Toplam satır: {len(tablo)}")

print("\n--- DÖNEM VE BÖLGE BAZINDA KAYIT SAYILARI ---")
print(tablo.groupby(["date_start", "bolge"]).size())

print("\n--- MESLEK PAYLARI TOPLAMI ---")
print(
    tablo.groupby(["date_start", "bolge"])["usage_pct"]
    .sum()
)

print("\n--- TÜRKİYE MAYIS 2026 İLK 5 MESLEK ---")
print(
    tablo[
        (tablo["date_start"] == "2026-05-01")
        & (tablo["bolge"] == "Türkiye")
    ]
    .nlargest(5, "usage_pct")
    .to_string(index=False)
)

print(f"\nDosya kaydedildi: {cikti}")
