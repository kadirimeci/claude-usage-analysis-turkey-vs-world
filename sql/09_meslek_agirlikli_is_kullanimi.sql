-- Meslek dağılımından hesaplanan iş amaçlı kullanım
-- ile genel kullanım oranının karşılaştırılması

WITH meslek AS (
    SELECT
        date_start,
        bolge,
        COUNT(*) AS meslek_sayisi,
        ROUND(SUM(usage_pct), 2) AS kapsanan_pay,

        ROUND(
            SAFE_DIVIDE(
                SUM(usage_pct * work_pct),
                SUM(usage_pct)
            ), 2
        ) AS kapsanan_mesleklerde_is_payi,

        ROUND(
            SUM(usage_pct * work_pct) / 100,
            2
        ) AS toplam_uzerinden_katki

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_kullanim_profili_2026`

    GROUP BY date_start, bolge
),

genel AS (
    SELECT
        date_start,
        'Türkiye' AS bolge,
        work_pct AS genel_is_payi
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.ulke_kullanim_amaclari_2026`
    WHERE geo_id = 'TUR'

    UNION ALL

    SELECT
        date_start,
        'Dünya' AS bolge,
        work_pct AS genel_is_payi
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.kuresel_kullanim_2026`
)

SELECT
    m.date_start AS donem,
    m.bolge,
    m.meslek_sayisi,
    m.kapsanan_pay,
    m.kapsanan_mesleklerde_is_payi,
    m.toplam_uzerinden_katki,
    g.genel_is_payi,

    ROUND(
        g.genel_is_payi - m.toplam_uzerinden_katki,
        2
    ) AS aciklanmayan_katki

FROM meslek AS m

JOIN genel AS g
    ON m.date_start = g.date_start
    AND m.bolge = g.bolge

ORDER BY donem, bolge;
