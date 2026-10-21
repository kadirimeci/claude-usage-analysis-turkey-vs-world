from pathlib import Path
import pandas as pd

# Dosya yolları
proje = Path(__file__).resolve().parent.parent
dosya = proje / "data" / "aei_claude_ai_2026-06-26.csv"

veri = pd.read_csv(dosya, low_memory=False)

# Türkiye - Mayıs 2026 - O*NET görev verileri
gorevler = veri[
    (veri["date_start"] == "2026-05-01")
    & (veri["geo_level"] == "country")
    & (veri["geo_id"] == "TUR")
    & (veri["category_name"] == "onet")
].copy()

print("\n--- GÖREV HİYERARŞİ SEVİYELERİ ---")
print(
    gorevler.groupby(
        ["hierarchy_level", "metric_id"]
    ).size().to_string()
)

# Her hiyerarşi seviyesinde kullanım payları
paylar = gorevler[
    gorevler["metric_id"] == "pct"
]

print("\n--- SEVİYELERE GÖRE PAY KONTROLÜ ---")
print(
    paylar.groupby("hierarchy_level").agg(
        kayit_sayisi=("value", "size"),
        toplam_pay=("value", "sum"),
        farkli_gorev=("node_name", "nunique")
    )
)

# Her seviyeden örnek kayıtlar
for seviye in sorted(gorevler["hierarchy_level"].unique()):
    ornek = paylar[
        paylar["hierarchy_level"] == seviye
    ]

    print(f"\n--- SEVİYE {seviye}: İLK 10 GÖREV ---")
    print(
        ornek.nlargest(10, "value")[
            [
                "node_name",
                "node_external_id",
                "value"
            ]
        ].to_string(index=False)
    )
