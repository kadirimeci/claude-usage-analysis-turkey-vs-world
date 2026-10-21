from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent.parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"

veri = pd.read_csv(dosya, low_memory=False)

# Çıktı türü metriklerini bul
cikti = veri[
    veri["metric_id"].str.startswith("artifact_", na=False)
].copy()

# Türkiye ve dünya genelini seç
cikti = cikti[
    (
        (cikti["geo_level"] == "country")
        & (cikti["geo_id"] == "TUR")
    )
    | (cikti["geo_level"] == "global")
]

print("\n--- ÇIKTI METRİKLERİ ---")
print(sorted(cikti["metric_id"].unique()))

print("\n--- KATEGORİ VE SEVİYE KAPSAMI ---")
print(
    cikti.groupby(
        ["category_name", "hierarchy_level"]
    ).size().to_string()
)

print("\n--- GENEL DÜZEYDE ÇIKTI KAPSAMI ---")
genel = cikti[
    (cikti["category_name"] == "overall")
    & (cikti["hierarchy_level"] == 0)
].copy()

genel["bolge"] = genel["geo_level"].map({
    "country": "Türkiye",
    "global": "Dünya"
})

print(
    genel.groupby(
        ["date_start", "bolge"]
    )["metric_id"].nunique()
)

print("\n--- TÜRKİYE MAYIS 2026 ÇIKTI TÜRLERİ ---")
turkiye = genel[
    (genel["geo_id"] == "TUR")
    & (genel["date_start"] == "2026-05-01")
].copy()

print(
    turkiye[
        ["metric_id", "value"]
    ]
    .sort_values("value", ascending=False)
    .to_string(index=False)
)

print("\n--- ÇIKTI PAYLARI TOPLAMI ---")
print(
    genel.groupby(
        ["date_start", "bolge"]
    )["value"].sum()
)
