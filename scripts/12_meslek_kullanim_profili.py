from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent.parent
ham_dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

# İhtiyacımız olan metrikler
metrikler = {
    "pct": "usage_pct",
    "use_case_work_pct": "work_pct",
    "use_case_personal_pct": "personal_pct",
    "use_case_coursework_pct": "coursework_pct",
    "collaboration_bucket_automation_pct": "automation_pct",
    "collaboration_bucket_augmentation_pct": "augmentation_pct"
}

veri = pd.read_csv(ham_dosya, low_memory=False)

secili = veri[
    (veri["category_name"] == "soc_occupation")
    & (veri["hierarchy_level"] == 1)
    & (veri["metric_id"].isin(metrikler))
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

anahtar = [
    "date_start",
    "bolge",
    "node_external_id",
    "metric_id"
]

assert not secili.duplicated(anahtar).any(), (
    "Tekrarlanan meslek-metrik kaydı bulundu!"
)

tablo = secili.pivot(
    index=[
        "date_start",
        "bolge",
        "node_external_id",
        "node_name"
    ],
    columns="metric_id",
    values="value"
).reset_index()

tablo = tablo.rename(columns={
    "node_external_id": "occupation_code",
    "node_name": "occupation_name",
    **metrikler
})

tablo.columns.name = None

sutunlar = [
    "date_start",
    "bolge",
    "occupation_code",
    "occupation_name",
    "usage_pct",
    "work_pct",
    "personal_pct",
    "coursework_pct",
    "automation_pct",
    "augmentation_pct"
]

tablo = tablo[sutunlar]

print("\n--- KAYIT SAYILARI ---")
print(tablo.groupby(["date_start", "bolge"]).size())

print("\n--- EKSİK DEĞERLER ---")
print(tablo.isna().sum())

print("\n--- KULLANIM AMAÇLARI TOPLAMI ---")
tablo["amac_toplam"] = (
    tablo["work_pct"]
    + tablo["personal_pct"]
    + tablo["coursework_pct"]
)
print(tablo["amac_toplam"].describe())

print("\n--- OTOMASYON VE İŞ BİRLİĞİ TOPLAMI ---")
tablo["isbirligi_toplam"] = (
    tablo["automation_pct"]
    + tablo["augmentation_pct"]
)
print(tablo["isbirligi_toplam"].describe())

# Kontrol sütunlarını kaldır
tablo = tablo.drop(
    columns=["amac_toplam", "isbirligi_toplam"]
)

cikti = cikti_klasoru / "meslek_kullanim_profili_2026.csv"

tablo.to_csv(
    cikti,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- TÜRKİYE MAYIS 2026 ---")
print(
    tablo[
        (tablo["date_start"] == "2026-05-01")
        & (tablo["bolge"] == "Türkiye")
    ]
    .sort_values("usage_pct", ascending=False)
    .head(10)
    .to_string(index=False)
)

print(f"\nDosya kaydedildi: {cikti}")
