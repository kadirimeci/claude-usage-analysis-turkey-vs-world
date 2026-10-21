from pathlib import Path
import pandas as pd

# Dosya yolları
proje = Path(__file__).resolve().parent.parent
ham_dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

# Orijinal CSV dosyasını oku
veri = pd.read_csv(ham_dosya, low_memory=False)

# Kullanacağımız göstergeler
metrikler = {
    "use_case_work_pct": "work_pct",
    "use_case_personal_pct": "personal_pct",
    "use_case_coursework_pct": "coursework_pct",
    "collaboration_bucket_automation_pct": "automation_pct",
    "collaboration_bucket_augmentation_pct": "augmentation_pct"
}

# Dünya geneli kayıtlarını seçme
kuresel = veri[
    (veri["geo_level"] == "global")
    & (veri["category_name"] == "overall")
    & (veri["hierarchy_level"] == 0)
    & (veri["metric_id"].isin(metrikler))
].copy()

# Her dönem için tek satır oluştur
tablo = kuresel.pivot(
    index=["date_start", "date_end"],
    columns="metric_id",
    values="value"
).reset_index()

# Sütunları düzenle
tablo = tablo.rename(columns=metrikler)
tablo.columns.name = None

sutunlar = [
    "date_start",
    "date_end",
    "work_pct",
    "personal_pct",
    "coursework_pct",
    "automation_pct",
    "augmentation_pct"
]

tablo = tablo[sutunlar].sort_values("date_start")

# Kontroller
assert len(tablo) == 2, "Beklenmeyen dönem sayısı!"

assert not tablo.isna().any().any(), "Eksik gösterge bulundu!"

# CSV dosyasını kaydet
cikti = cikti_klasoru / "kuresel_kullanim_2026.csv"
tablo.to_csv(cikti, index=False, encoding="utf-8-sig")

print("\n--- DÜNYA GENELİ KULLANIM VERİLERİ ---")
print(tablo.to_string(index=False))

print(f"\nDosya kaydedildi: {cikti}")
