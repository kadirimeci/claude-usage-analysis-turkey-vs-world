-- Nisan ve Mayıs 2026
-- Türkiye ile dünya genelindeki çıktı türü farkları

WITH karsilastirma AS (
    SELECT
        date_start,
        artifact_code,

        MAX(IF(bolge = 'Türkiye', usage_pct, NULL))
            AS turkiye_pay,

        MAX(IF(bolge = 'Dünya', usage_pct, NULL))
            AS dunya_pay

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.cikti_turleri_2026`

    GROUP BY date_start, artifact_code
),

donemler AS (
    SELECT
        artifact_code,

        MAX(IF(date_start = DATE '2026-04-01',
            turkiye_pay - dunya_pay, NULL))
            AS nisan_farki,

        MAX(IF(date_start = DATE '2026-05-01',
            turkiye_pay - dunya_pay, NULL))
            AS mayis_farki

    FROM karsilastirma

    WHERE
        turkiye_pay IS NOT NULL
        AND dunya_pay IS NOT NULL

    GROUP BY artifact_code
)

SELECT
    artifact_code,
    ROUND(nisan_farki, 2) AS nisan_farki,
    ROUND(mayis_farki, 2) AS mayis_farki,

    ROUND(
        mayis_farki - nisan_farki,
        2
    ) AS farkin_degisim_puani

FROM donemler

ORDER BY ABS(mayis_farki) DESC;
