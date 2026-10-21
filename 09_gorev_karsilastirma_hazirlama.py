from pathlib import Path
import pandas as pd

# Proje dosyaları
proje = Path(__file__).resolve().parent
ham_dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

veri = pd.read_csv(ham_dosya, low_memory=False)

# Ana faaliyet kategorilerini seç
gorevler = veri[
    (veri["category_name"] == "onet")
    & (veri["hierarchy_level"] == 3)
    & (veri["metric_id"] == "pct")
    & (
        (
            (veri["geo_level"] == "country")
            & (veri["geo_id"] == "TUR")
        )
        | (veri["geo_level"] == "global")
    )
].copy()

# Bölge bilgisi
gorevler["bolge"] = gorevler["geo_level"].map({
    "country": "Türkiye",
    "global": "Dünya"
})

# Analiz tablosunu oluştur
tablo = gorevler[
    [
        "date_start",
        "bolge",
        "node_external_id",
        "node_name",
        "value"
    ]
].rename(columns={
    "node_external_id": "task_code",
    "node_name": "task_name",
    "value": "usage_pct"
})

# Veri kalitesi kontrolleri
anahtar = ["date_start", "bolge", "task_code"]

assert not tablo.duplicated(anahtar).any(), (
    "Tekrarlanan görev kaydı bulundu!"
)

assert not tablo["usage_pct"].isna().any(), (
    "Eksik kullanım payı bulundu!"
)

# Dosyayı kaydet
cikti = cikti_klasoru / "gorev_karsilastirma_2026.csv"

tablo.to_csv(
    cikti,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- GÖREV KARŞILAŞTIRMA TABLOSU ---")
print(f"Toplam satır: {len(tablo)}")

print("\n--- DÖNEM VE BÖLGE KAYIT SAYILARI ---")
print(
    tablo.groupby(["date_start", "bolge"]).size()
)

print("\n--- KULLANIM PAYLARI TOPLAMI ---")
print(
    tablo.groupby(["date_start", "bolge"])["usage_pct"].sum()
)

print("\n--- TÜRKİYE MAYIS 2026 İLK 10 FAALİYET ---")
print(
    tablo[
        (tablo["date_start"] == "2026-05-01")
        & (tablo["bolge"] == "Türkiye")
    ]
    .nlargest(10, "usage_pct")
    .to_string(index=False)
)

print(f"\nDosya kaydedildi: {cikti}")
