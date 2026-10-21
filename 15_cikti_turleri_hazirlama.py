from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent
ham_dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

veri = pd.read_csv(ham_dosya, low_memory=False)

# Genel düzeydeki çıktı türlerini seç
secili = veri[
    (veri["category_name"] == "overall")
    & (veri["hierarchy_level"] == 0)
    & (veri["metric_id"].str.startswith("artifact_", na=False))
    & (
        (
            (veri["geo_level"] == "country")
            & (veri["geo_id"] == "TUR")
        )
        | (veri["geo_level"] == "global")
    )
].copy()

secili["bolge"] = secili["geo_level"].map({
    "country": "Türkiye",
    "global": "Dünya"
})

secili = secili.rename(columns={
    "metric_id": "artifact_code",
    "value": "usage_pct"
})

tablo = secili[
    ["date_start", "bolge", "artifact_code", "usage_pct"]
].copy()

# Kontroller
assert not tablo.duplicated(
    ["date_start", "bolge", "artifact_code"]
).any(), "Tekrarlanan çıktı türü bulundu!"

assert tablo["usage_pct"].notna().all(), (
    "Eksik kullanım oranı bulundu!"
)

print("\n--- KAYIT SAYILARI ---")
print(tablo.groupby(["date_start", "bolge"]).size())

print("\n--- ÇIKTI PAYLARI TOPLAMI ---")
print(
    tablo.groupby(["date_start", "bolge"])["usage_pct"].sum()
)

# Mayıs Türkiye-Dünya karşılaştırması
mayis = tablo[
    tablo["date_start"] == "2026-05-01"
]

karsilastirma = mayis.pivot(
    index="artifact_code",
    columns="bolge",
    values="usage_pct"
).reset_index()

karsilastirma["fark_yuzde_puan"] = (
    karsilastirma["Türkiye"]
    - karsilastirma["Dünya"]
).round(2)

print("\n--- TÜRKİYE'DE DAHA YÜKSEK PAYA SAHİP ÇIKTILAR ---")
print(
    karsilastirma.nlargest(
        10, "fark_yuzde_puan"
    ).to_string(index=False)
)

print("\n--- TÜRKİYE'DE DAHA DÜŞÜK PAYA SAHİP ÇIKTILAR ---")
print(
    karsilastirma.nsmallest(
        10, "fark_yuzde_puan"
    ).to_string(index=False)
)

# CSV kaydet
cikti = cikti_klasoru / "cikti_turleri_2026.csv"

tablo.to_csv(
    cikti,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nDosya kaydedildi: {cikti}")
