from pathlib import Path
import pandas as pd

# Dosya yolu
proje = Path(__file__).resolve().parent.parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"

# Ham veri
veri = pd.read_csv(dosya, low_memory=False)

# Meslek ve görev kayıtları
meslek_gorev = veri[
    veri["category_name"].isin(["soc_occupation", "onet"])
].copy()

print("\n--- MESLEK VE GÖREV KAYIT SAYILARI ---")
print(meslek_gorev["category_name"].value_counts())

print("\n--- MESLEK VE GÖREV METRİKLERİ ---")
print(
    meslek_gorev.groupby(["category_name", "metric_id"])
    .size()
    .to_string()
)

print("\n--- HİYERARŞİ SEVİYELERİ ---")
print(
    meslek_gorev.groupby(
        ["category_name", "hierarchy_level"]
    ).size()
)

print("\n--- TÜRKİYE'DE MESLEK KATEGORİLERİ ---")
turkiye = meslek_gorev[
    (meslek_gorev["geo_id"] == "TUR")
    & (meslek_gorev["geo_level"] == "country")
]

print(
    turkiye.groupby(
        ["date_start", "category_name"]
    )["node_name"].nunique()
)

print("\n--- TÜRKİYE'DEN ÖRNEK MESLEK KAYITLARI ---")
print(
    turkiye[
        turkiye["category_name"] == "soc_occupation"
    ][
        [
            "date_start",
            "hierarchy_level",
            "metric_id",
            "node_name",
            "value"
        ]
    ].head(20).to_string(index=False)
)

print("\n--- TÜRKİYE'DEN ÖRNEK GÖREV KAYITLARI ---")
print(
    turkiye[
        turkiye["category_name"] == "onet"
    ][
        [
            "date_start",
            "hierarchy_level",
            "metric_id",
            "node_name",
            "value"
        ]
    ].head(20).to_string(index=False)
)
