-- Meslek kategorilerine göre çıktı türlerinin karşılaştırılması
-- Türkiye vs Dünya | Mayıs 2026

WITH karsilastirma AS (
    SELECT
        occupation_code,
        occupation_name,
        artifact_code,

        MAX(
            IF(bolge = 'Türkiye', artifact_pct, NULL)
        ) AS turkiye_pct,

        MAX(
            IF(bolge = 'Dünya', artifact_pct, NULL)
        ) AS dunya_pct

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_cikti_profili_2026`

    WHERE
        date_start = DATE '2026-05-01'
        AND occupation_code IN (15, 13, 43)

    GROUP BY
        occupation_code,
        occupation_name,
        artifact_code
),

farklar AS (
    SELECT
        occupation_code,
        occupation_name,
        artifact_code,
        ROUND(turkiye_pct, 2) AS turkiye_pct,
        ROUND(dunya_pct, 2) AS dunya_pct,

        ROUND(
            turkiye_pct - dunya_pct,
            2
        ) AS fark_yuzde_puan

    FROM karsilastirma

    WHERE
        turkiye_pct IS NOT NULL
        AND dunya_pct IS NOT NULL
),

sirali AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY occupation_code
            ORDER BY ABS(fark_yuzde_puan) DESC
        ) AS sira

    FROM farklar
)

SELECT
    occupation_name,
    artifact_code,
    turkiye_pct,
    dunya_pct,
    fark_yuzde_puan

FROM sirali

WHERE sira <= 5

ORDER BY
    occupation_name,
    sira;
