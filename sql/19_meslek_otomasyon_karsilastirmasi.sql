-- Meslek kategorilerine göre otomasyon kullanımının karşılaştırılması
-- Analiz dönemi: Nisan-Mayıs 2026
-- Amaç: Türkiye ve dünya arasındaki otomasyon farklarını
-- mesleki görev kategorileri düzeyinde incelemek

WITH karsilastirma AS (
    SELECT
        date_start,
        occupation_code,
        occupation_name,

        MAX(
            IF(bolge = 'Türkiye', automation_pct, NULL)
        ) AS turkiye_otomasyon,

        MAX(
            IF(bolge = 'Dünya', automation_pct, NULL)
        ) AS dunya_otomasyon,

        MAX(
            IF(bolge = 'Türkiye', usage_pct, NULL)
        ) AS turkiye_kullanim_payi,

        MAX(
            IF(bolge = 'Dünya', usage_pct, NULL)
        ) AS dunya_kullanim_payi

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_kullanim_profili_2026`

    GROUP BY
        date_start,
        occupation_code,
        occupation_name
)

SELECT
    date_start,
    occupation_name,

    ROUND(turkiye_otomasyon, 2)
        AS turkiye_otomasyon,

    ROUND(dunya_otomasyon, 2)
        AS dunya_otomasyon,

    ROUND(
        turkiye_otomasyon - dunya_otomasyon,
        2
    ) AS otomasyon_farki,

    ROUND(turkiye_kullanim_payi, 2)
        AS turkiye_kullanim_payi,

    ROUND(dunya_kullanim_payi, 2)
        AS dunya_kullanim_payi

FROM karsilastirma

WHERE
    turkiye_otomasyon IS NOT NULL
    AND dunya_otomasyon IS NOT NULL

ORDER BY
    date_start,
    ABS(otomasyon_farki) DESC;
