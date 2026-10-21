-- Mayıs 2026: Meslek gruplarında Türkiye-Dünya karşılaştırması

WITH turkiye AS (
    SELECT
        CAST(occupation_code AS STRING) AS occupation_code,
        occupation_name,
        usage_pct,
        work_pct,
        automation_pct
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_kullanim_profili_2026`
    WHERE
        bolge = 'Türkiye'
        AND date_start = DATE '2026-05-01'
),

dunya AS (
    SELECT
        CAST(occupation_code AS STRING) AS occupation_code,
        work_pct,
        automation_pct
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_kullanim_profili_2026`
    WHERE
        bolge = 'Dünya'
        AND date_start = DATE '2026-05-01'
)

SELECT
    t.occupation_name AS meslek_grubu,
    t.usage_pct AS turkiye_kullanim_payi,

    t.work_pct AS turkiye_is_amacli,
    d.work_pct AS dunya_is_amacli,

    ROUND(
        t.work_pct - d.work_pct, 2
    ) AS is_amacli_fark,

    t.automation_pct AS turkiye_otomasyon,
    d.automation_pct AS dunya_otomasyon,

    ROUND(
        t.automation_pct - d.automation_pct, 2
    ) AS otomasyon_farki

FROM turkiye AS t

INNER JOIN dunya AS d
    ON t.occupation_code = d.occupation_code

ORDER BY
    is_amacli_fark DESC;
