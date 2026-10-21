from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent.parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"

veri = pd.read_csv(dosya, low_memory=False)

# Türkiye ve dünya meslek kayıtları
meslek = veri[
    (veri["category_name"] == "soc_occupation")
    & (
        ((veri["geo_level"] == "country")
         & (veri["geo_id"] == "TUR"))
        | (veri["geo_level"] == "global")
    )
].copy()

metrikler = [
    "pct",
    "use_case_work_pct",
    "use_case_personal_pct",
    "use_case_coursework_pct",
    "collaboration_bucket_automation_pct",
    "collaboration_bucket_augmentation_pct"
]

secili = meslek[
    meslek["metric_id"].isin(metrikler)
]

print("\n--- HİYERARŞİ VE METRİK KAPSAMI ---")
print(
    secili.groupby(
        ["hierarchy_level", "metric_id"]
    ).size().to_string()
)

print("\n--- TÜRKİYE MAYIS: MESLEK SEVİYELERİ ---")
turkiye = secili[
    (secili["geo_id"] == "TUR")
    & (secili["date_start"] == "2026-05-01")
]

print(
    turkiye.groupby(
        ["hierarchy_level", "metric_id"]
    )["node_external_id"].nunique().to_string()
)

print("\n--- ANA MESLEK GRUPLARINDA METRİK ÖRNEKLERİ ---")
ornek = turkiye[
    turkiye["hierarchy_level"] == 1
]

print(
    ornek.pivot_table(
        index=["node_external_id", "node_name"],
        columns="metric_id",
        values="value",
        aggfunc="first"
    ).head(10).to_string()
)
