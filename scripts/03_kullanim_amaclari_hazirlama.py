from pathlib import Path
import pandas as pd

# Proje klasörleri
proje = Path(__file__).resolve().parent.parent
ham_dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

# Ana veri setini okuma
veri = pd.read_csv(ham_dosya, low_memory=False)

# Analiz edeceğimiz metrikler
metrikler = {
    "use_case_work_pct": "work_pct",
    "use_case_personal_pct": "personal_pct",
    "use_case_coursework_pct": "coursework_pct",
    "collaboration_bucket_automation_pct": "automation_pct",
    "collaboration_bucket_augmentation_pct": "augmentation_pct"
}

# Ülke düzeyindeki genel kullanım göstergeleri
secili = veri[
    (veri["geo_level"] == "country")
    & (veri["category_name"] == "overall")
    & (veri["hierarchy_level"] == 0)
    & (veri["metric_id"].isin(metrikler))
].copy()

# Her ülke ve dönem tek satır olacak
tablo = secili.pivot(
    index=["date_start", "date_end", "geo_id"],
    columns="metric_id",
    values="value"
).reset_index()

# Sütunları yeniden adlandır
tablo = tablo.rename(columns=metrikler)
tablo.columns.name = None

# Sütun sıralaması
sutunlar = [
    "date_start",
    "date_end",
    "geo_id",
    "work_pct",
    "personal_pct",
    "coursework_pct",
    "automation_pct",
    "augmentation_pct"
]

tablo = tablo[sutunlar].sort_values(
    ["date_start", "geo_id"]
)

# Veri kalitesi kontrolleri
assert not tablo.duplicated(
    ["date_start", "geo_id"]
).any(), "Tekrarlanan ülke-dönem kaydı bulundu!"

assert not tablo[
    ["work_pct", "personal_pct", "coursework_pct"]
].isna().any().any(), "Eksik kullanım amacı bulundu!"

# CSV dosyasını oluştur
cikti = cikti_klasoru / "ulke_kullanim_amaclari_2026.csv"
tablo.to_csv(cikti, index=False, encoding="utf-8-sig")

print("\n--- VERİ HAZIRLAMA TAMAMLANDI ---")
print(f"Toplam satır: {len(tablo)}")
print(f"Toplam sütun: {len(tablo.columns)}")

print("\n--- DÖNEMLERE GÖRE ÜLKE SAYILARI ---")
print(tablo.groupby("date_start")["geo_id"].nunique())

print("\n--- TÜRKİYE KAYITLARI ---")
print(tablo[tablo["geo_id"] == "TUR"].to_string(index=False))

print(f"\nDosya kaydedildi: {cikti}")
