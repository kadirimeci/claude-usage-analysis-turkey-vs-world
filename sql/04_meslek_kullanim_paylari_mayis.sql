-- Mayıs 2026: Türkiye ve dünya genelinde
-- aynı meslek gruplarının Claude kullanım payları

WITH turkiye AS (
    SELECT
        occupation_code,
        occupation_name,
        usage_pct AS turkiye_pay
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_karsilastirma_2026`
    WHERE
        bolge = 'Türkiye'
        AND date_start = '2026-05-01'
),

dunya AS (
    SELECT
        occupation_code,
        usage_pct AS dunya_pay
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_karsilastirma_2026`
    WHERE
        bolge = 'Dünya'
        AND date_start = '2026-05-01'
)

SELECT
    t.occupation_code AS meslek_kodu,
    t.occupation_name AS meslek_grubu,
    t.turkiye_pay,
    d.dunya_pay,
    ROUND(t.turkiye_pay - d.dunya_pay, 2)
        AS fark_yuzde_puan
FROM turkiye AS t
INNER JOIN dunya AS d
    ON t.occupation_code = d.occupation_code
ORDER BY fark_yuzde_puan DESC;
