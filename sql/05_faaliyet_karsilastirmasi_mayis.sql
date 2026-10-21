-- Mayıs 2026: Türkiye ve dünya genelinde
-- ortak faaliyet kategorilerinin karşılaştırılması

WITH turkiye AS (
    SELECT
        task_code,
        task_name,
        usage_pct AS turkiye_pay
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.gorev_karsilastirma_2026`
    WHERE
        bolge = 'Türkiye'
        AND date_start = DATE '2026-05-01'
),

dunya AS (
    SELECT
        task_code,
        usage_pct AS dunya_pay
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.gorev_karsilastirma_2026`
    WHERE
        bolge = 'Dünya'
        AND date_start = DATE '2026-05-01'
)

SELECT
    t.task_code AS gorev_kodu,
    t.task_name AS faaliyet,
    t.turkiye_pay,
    d.dunya_pay,
    ROUND(t.turkiye_pay - d.dunya_pay, 2)
        AS fark_yuzde_puan
FROM turkiye AS t
INNER JOIN dunya AS d
    ON t.task_code = d.task_code
ORDER BY fark_yuzde_puan DESC;
