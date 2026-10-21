from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent.parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"

# Büyük dosyadan yalnızca gereken sütunları oku
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
    dosya,
    usecols=sutunlar,
    low_memory=False
)

# Meslek kategorilerindeki çıktı türleri
meslek_cikti = veri[
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

meslek_cikti["bolge"] = meslek_cikti["geo_level"].map({
    "country": "Türkiye",
    "global": "Dünya"
})

print("\n--- TOPLAM KAYIT ---")
print(len(meslek_cikti))

print("\n--- DÖNEM VE BÖLGE BAZINDA KAPSAM ---")
print(
    meslek_cikti.groupby(
        ["date_start", "bolge"]
    ).agg(
        meslek_sayisi=("node_external_id", "nunique"),
        cikti_turu_sayisi=("metric_id", "nunique"),
        kayit_sayisi=("metric_id", "size")
    ).to_string()
)

# Her meslekte çıktı oranlarının toplamı
kontrol = (
    meslek_cikti.groupby(
        [
            "date_start",
            "bolge",
            "node_external_id",
            "node_name"
        ],
        dropna=False
    )
    .agg(
        cikti_turu_sayisi=("metric_id", "nunique"),
        toplam_yuzde=("value", "sum"),
        eksik_deger=("value", lambda x: x.isna().sum())
    )
    .reset_index()
)

print("\n--- ÇIKTI TÜRÜ SAYISI DAĞILIMI ---")
print(
    kontrol["cikti_turu_sayisi"]
    .value_counts()
    .sort_index()
)

print("\n--- YÜZDE TOPLAMLARI ---")
print(
    kontrol.groupby(["date_start", "bolge"])
    ["toplam_yuzde"]
    .agg(["min", "max", "mean"])
    .round(2)
    .to_string()
)

print("\n--- SORUNLU KATEGORİLER ---")
sorunlu = kontrol[
    (kontrol["cikti_turu_sayisi"] != 32)
    | (kontrol["toplam_yuzde"].sub(100).abs() > 0.5)
    | (kontrol["eksik_deger"] > 0)
]

if sorunlu.empty:
    print("Sorunlu kategori bulunmadı.")
else:
    print(sorunlu.to_string(index=False))

print("\n--- TEKRARLAYAN KAYIT KONTROLÜ ---")
tekrar = meslek_cikti.duplicated(
    [
        "date_start",
        "bolge",
        "node_external_id",
        "metric_id"
    ]
).sum()

print(f"Tekrarlayan kayıt: {tekrar}")

print("\n--- ÖRNEK MESLEK KATEGORİLERİ ---")
print(
    meslek_cikti[
        ["node_external_id", "node_name"]
    ]
    .drop_duplicates()
    .head(10)
    .to_string(index=False)
)
