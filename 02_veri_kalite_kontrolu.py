from pathlib import Path
import pandas as pd

proje = Path(__file__).resolve().parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"

veri = pd.read_csv(dosya, low_memory=False)

# Ülke düzeyindeki genel kullanım kayıtları
genel = veri[
    (veri["geo_level"] == "country")
    & (veri["category_name"] == "overall")
    & (veri["hierarchy_level"] == 0)
].copy()

print("\n--- ÜLKE SAYILARI ---")
print(genel.groupby("date_start")["geo_id"].nunique())

# Bir ülke, dönem ve metrik için birden fazla kayıt var mı?
anahtar = ["date_start", "geo_id", "metric_id"]

tekrarlar = genel.duplicated(
    subset=anahtar,
    keep=False
)

print("\n--- TEKRARLANAN GÖSTERGELER ---")
print(f"Tekrarlanan kayıt sayısı: {tekrarlar.sum()}")

if tekrarlar.any():
    print(
        genel.loc[tekrarlar, anahtar]
        .sort_values(anahtar)
        .head(20)
    )

# Kullanım amaçlarının toplamı
amaclar = genel[
    genel["metric_id"].isin([
        "use_case_work_pct",
        "use_case_personal_pct",
        "use_case_coursework_pct"
    ])
]

amac_tablosu = amaclar.pivot(
    index=["date_start", "geo_id"],
    columns="metric_id",
    values="value"
)

amac_tablosu["toplam"] = amac_tablosu.sum(
    axis=1,
    min_count=3
)

print("\n--- KULLANIM AMAÇLARI TOPLAM KONTROLÜ ---")
print(amac_tablosu["toplam"].describe())

print("\n--- 100'DEN SAPAN KAYIT SAYISI ---")
sapmalar = (
    amac_tablosu["toplam"].notna()
    & ((amac_tablosu["toplam"] - 100).abs() > 0.1)
)

print(sapmalar.sum())

print("\n--- EKSİK GÖSTERGELİ ÜLKE-DÖNEM SAYISI ---")
print(amac_tablosu["toplam"].isna().sum())
