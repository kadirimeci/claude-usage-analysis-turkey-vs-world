from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent.parent
ham_dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"
cikti_klasoru = proje / "outputs"
cikti_klasoru.mkdir(exist_ok=True)

sutunlar = [
    "date_start",
    "geo_id",
    "geo_level",
    "category_name",
    "hierarchy_level",
    "metric_id",
    "value",
    "node_name",
    "node_external_id"
]

veri = pd.read_csv(
    ham_dosya,
    usecols=sutunlar,
    low_memory=False
)

secili = veri[
    (veri["category_name"] == "soc_occupation")
    & (veri["hierarchy_level"] == 1)
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

tablo = secili.rename(columns={
    "node_external_id": "occupation_code",
    "node_name": "occupation_name",
    "metric_id": "artifact_code",
    "value": "artifact_pct"
})[
    [
        "date_start",
        "bolge",
        "occupation_code",
        "occupation_name",
        "artifact_code",
        "artifact_pct"
    ]
].copy()

tablo["occupation_code"] = (
    tablo["occupation_code"].astype(str)
)

# Veri kontrolleri
assert len(tablo) == 2688, "Beklenmeyen kayıt sayısı!"

assert not tablo.duplicated(
    [
        "date_start",
        "bolge",
        "occupation_code",
        "artifact_code"
    ]
).any(), "Tekrarlayan kayıt var!"

assert tablo["artifact_pct"].notna().all(), (
    "Eksik oran bulundu!"
)

assert tablo["artifact_pct"].between(0, 100).all(), (
    "Geçersiz yüzde değeri!"
)

# Kategori bazında yüzde toplamları
toplamlar = tablo.groupby(
    ["date_start", "bolge", "occupation_code"]
)["artifact_pct"].sum()

assert (toplamlar - 100).abs().le(0.5).all(), (
    "Çıktı payları %100'e yakın değil!"
)

# Kaydet
hedef = cikti_klasoru / "meslek_cikti_profili_2026.csv"

tablo.to_csv(
    hedef,
    index=False,
    encoding="utf-8-sig"
)

print("\n--- TABLO BAŞARIYLA OLUŞTURULDU ---")
print(f"Toplam kayıt: {len(tablo)}")
print(f"Meslek-dönem-bölge grubu: {len(toplamlar)}")
print(f"Çıktı türü: {tablo['artifact_code'].nunique()}")
print(f"Tekrarlayan kayıt: 0")
print(f"Eksik oran: 0")
print(f"Dosya: {hedef}")

print("\n--- ÖRNEK VERİ ---")
print(tablo.head(10).to_string(index=False))
