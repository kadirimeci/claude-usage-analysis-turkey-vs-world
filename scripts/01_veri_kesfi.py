from pathlib import Path
import pandas as pd

# Ana veri dosyasının konumu
proje_klasoru = Path(__file__).resolve().parent.parent
dosya_yolu = proje_klasoru / "data" / "aei_claude_ai_2026-06-26.csv"

# CSV dosyasını okuyoruz
veri = pd.read_csv(dosya_yolu, low_memory=False)

# 1. Veri setinin boyutu
print("\n--- VERİ SETİNİN BOYUTU ---")
print(f"Toplam satır: {len(veri):,}")
print(f"Toplam sütun: {len(veri.columns)}")

# 2. Sütun isimleri
print("\n--- SÜTUN İSİMLERİ ---")
print(veri.columns.tolist())

# 3. İlk 5 kayıt
print("\n--- İLK 5 KAYIT ---")
print(veri.head().to_string(index=False))

# 4. Veri tipleri
print("\n--- VERİ TİPLERİ ---")
print(veri.dtypes)

# 5. Veri dönemleri
print("\n--- VERİ DÖNEMLERİ ---")
print(veri[["date_start", "date_end"]].drop_duplicates())

# 6. Coğrafi seviyeler
print("\n--- COĞRAFİ SEVİYELER ---")
print(veri["geo_level"].value_counts(dropna=False))

# 7. Analiz kategorileri
print("\n--- ANALİZ KATEGORİLERİ ---")
print(veri["category_name"].value_counts(dropna=False))

# 8. Türkiye kayıtları
turkiye_verisi = veri[
    (veri["geo_id"] == "TUR")
    & (veri["geo_level"] == "country")
]

print("\n--- TÜRKİYE VERİLERİ ---")
print(f"Türkiye kayıt sayısı: {len(turkiye_verisi):,}")
print(turkiye_verisi["date_start"].value_counts())

# 9. Eksik değerler
print("\n--- EKSİK DEĞERLER ---")
print(veri.isna().sum())

# 10. Tekrarlanan kayıtlar
print("\n--- TAMAMEN AYNI SATIRLAR ---")
print(veri.duplicated().sum())


# 11. Veri setindeki metrikler
print("\n--- METRİKLER ---")
print(veri["metric_id"].value_counts().to_string())

# 12. Kategorilere göre metrik sayısı
print("\n--- KATEGORİLERE GÖRE METRİK SAYISI ---")
print(
    veri.groupby("category_name")["metric_id"]
    .nunique()
    .sort_values(ascending=False)
)

# 13. Türkiye'deki metrikler
print("\n--- TÜRKİYE'DEKİ METRİKLER ---")
print(
    turkiye_verisi["metric_id"]
    .value_counts()
    .to_string()
)

# 14. Genel kullanım göstergeleri
genel_kullanim = veri[
    (veri["geo_level"].isin(["country", "global"]))
    & (veri["category_name"] == "overall")
    & (veri["hierarchy_level"] == 0)
]

print("\n--- GENEL KULLANIM METRİKLERİ ---")
print(
    genel_kullanim["metric_id"]
    .drop_duplicates()
    .sort_values()
    .to_string(index=False)
)

# 15. Türkiye'nin genel kullanım kayıtları
turkiye_genel = genel_kullanim[
    genel_kullanim["geo_id"] == "TUR"
]

print("\n--- TÜRKİYE GENEL KULLANIM VERİLERİ ---")
print(
    turkiye_genel[
        ["date_start", "metric_id", "value"]
    ].sort_values(["date_start", "metric_id"])
    .to_string(index=False)
)
