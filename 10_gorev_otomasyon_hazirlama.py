from pathlib import Path
import pandas as pd

# Proje dosyaları
proje = Path(__file__).resolve().parent
ham_dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

veri = pd.read_csv(ham_dosya, low_memory=False)

# Görev bazında otomasyon ve insan-AI iş birliği
metrikler = {
    "collaboration_bucket_automation_pct": "automation_pct",
    "collaboration_bucket_augmentation_pct": "augmentation_pct",
    "use_case_work_pct": "work_pct",
    "pct": "usage_pct"
}

secili = veri[
    (veri["category_name"] == "onet")
    & (veri["hierarchy_level"] == 3)
    & (veri["metric_id"].isin(metrikler))
    & (
        (
            (veri["geo_level"] == "country")
            & (veri["geo_id"] == "TUR")
        )
        | (veri["geo_level"] == "global")
    )
].copy()

# Bölge etiketleri
secili["bolge"] = secili["geo_level"].map({
    "country": "Türkiye",
    "global": "Dünya"
})

# Metrikleri sütunlara dönüştür
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
    "node_external_id": "task_code",
    "node_name": "task_name",
    **metrikler
})

tablo.columns.name = None

# Sütun sıralaması
sutunlar = [
    "date_start",
    "bolge",
    "task_code",
    "task_name",
    "usage_pct",
    "work_pct",
    "automation_pct",
    "augmentation_pct"
]

tablo = tablo[sutunlar]

# Kontroller
assert not tablo.duplicated(
    ["date_start", "bolge", "task_code"]
).any(), "Tekrarlanan görev bulundu!"

print("\n--- EKSİK DEĞERLER ---")
print(tablo.isna().sum())

print("\n--- OTOMASYON + İŞ BİRLİĞİ TOPLAMI ---")
tablo["toplam"] = (
    tablo["automation_pct"]
    + tablo["augmentation_pct"]
)

print(tablo["toplam"].describe())

# Kontrol sütununu kaldır
tablo = tablo.drop(columns="toplam")

# CSV kaydı
cikti = cikti_klasoru / "gorev_otomasyon_2026.csv"

tablo.to_csv(
    cikti,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- TABLO BOYUTU ---")
print(tablo.shape)

print("\n--- TÜRKİYE MAYIS 2026 İLK 10 GÖREV ---")
print(
    tablo[
        (tablo["date_start"] == "2026-05-01")
        & (tablo["bolge"] == "Türkiye")
    ]
    .nlargest(10, "usage_pct")
    .to_string(index=False)
)

print(f"\nDosya kaydedildi: {cikti}")
