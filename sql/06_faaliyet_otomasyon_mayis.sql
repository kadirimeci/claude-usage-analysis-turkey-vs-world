-- Mayıs 2026: Faaliyet bazında otomasyon karşılaştırması
-- Yalnızca Türkiye ve dünya genelinde ortak bulunan faaliyetler

WITH karsilastirma AS (
    SELECT
        task_code,
        MAX(IF(bolge = 'Türkiye', task_name, NULL))
            AS faaliyet,

        MAX(IF(bolge = 'Türkiye', usage_pct, NULL))
            AS turkiye_kullanim_payi,

        MAX(IF(bolge = 'Türkiye', work_pct, NULL))
            AS turkiye_is_amacli,

        MAX(IF(bolge = 'Türkiye', automation_pct, NULL))
            AS turkiye_otomasyon,

        MAX(IF(bolge = 'Dünya', automation_pct, NULL))
            AS dunya_otomasyon

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.gorev_otomasyon_2026`

    WHERE
        date_start = DATE '2026-05-01'

    GROUP BY
        task_code
)

SELECT
    faaliyet,
    turkiye_kullanim_payi,
    turkiye_is_amacli,
    turkiye_otomasyon,
    dunya_otomasyon,

    ROUND(
        turkiye_otomasyon - dunya_otomasyon,
        2
    ) AS otomasyon_farki

FROM karsilastirma

WHERE
    turkiye_otomasyon IS NOT NULL
    AND dunya_otomasyon IS NOT NULL

ORDER BY
    turkiye_otomasyon DESC;
