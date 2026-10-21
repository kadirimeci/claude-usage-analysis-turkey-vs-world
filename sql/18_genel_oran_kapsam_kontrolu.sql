-- Genel çıktı oranları ile meslek bazlı ağırlıklı oranların karşılaştırılması
-- Analiz dönemi: Nisan-Mayıs 2026
-- Amaç: Meslek kapsamı nedeniyle oluşan farkları ve hesaplama tutarlılığını ölçmek

WITH meslek_agirlikli AS (
    SELECT
        c.date_start,
        c.bolge,
        c.artifact_code,

        SUM(
            m.usage_pct * c.artifact_pct / 100
        ) AS agirlikli_oran,

        COUNT(DISTINCT c.occupation_code)
            AS meslek_sayisi

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_cikti_profili_2026` c

    INNER JOIN
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_kullanim_profili_2026` m

    ON c.date_start = m.date_start
       AND c.bolge = m.bolge
       AND CAST(c.occupation_code AS STRING)
           = CAST(m.occupation_code AS STRING)

    GROUP BY
        c.date_start,
        c.bolge,
        c.artifact_code
)

SELECT
    g.date_start,
    g.bolge,
    g.artifact_code,

    ROUND(g.usage_pct, 4)
        AS genel_oran,

    ROUND(m.agirlikli_oran, 4)
        AS meslek_agirlikli_oran,

    ROUND(
        g.usage_pct - m.agirlikli_oran,
        4
    ) AS kapsam_farki,

    m.meslek_sayisi

FROM
    `prefab-bruin-483617-b9.anthropic_ai_analiz.cikti_turleri_2026` g

LEFT JOIN meslek_agirlikli m
    ON g.date_start = m.date_start
    AND g.bolge = m.bolge
    AND g.artifact_code = m.artifact_code

ORDER BY
    g.date_start,
    g.bolge,
    ABS(g.usage_pct - m.agirlikli_oran) DESC;
