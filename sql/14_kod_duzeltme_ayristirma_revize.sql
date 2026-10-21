-- Kod düzeltme çıktısının ayrıştırılması
-- Türkiye vs Dünya | Mayıs 2026
-- 20 ortak meslek kategorisi

WITH temel AS (
    SELECT
        c.bolge,
        c.occupation_code,
        c.occupation_name,
        c.artifact_pct,
        m.usage_pct

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_cikti_profili_2026` c

    INNER JOIN
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_kullanim_profili_2026` m

    ON c.date_start = m.date_start
       AND c.bolge = m.bolge
       AND CAST(c.occupation_code AS STRING)
           = CAST(m.occupation_code AS STRING)

    WHERE
        c.date_start = DATE '2026-05-01'
        AND c.artifact_code = 'artifact_code_fix_or_debug_pct'
),

ortak_meslekler AS (
    SELECT occupation_code
    FROM temel
    GROUP BY occupation_code
    HAVING COUNT(DISTINCT bolge) = 2
),

ortak_veri AS (
    SELECT t.*
    FROM temel t
    INNER JOIN ortak_meslekler o
        ON t.occupation_code = o.occupation_code
),

agirliklar AS (
    SELECT
        *,
        SAFE_DIVIDE(
            usage_pct,
            SUM(usage_pct) OVER (PARTITION BY bolge)
        ) AS agirlik
    FROM ortak_veri
),

karsilastirma AS (
    SELECT
        occupation_code,
        MAX(occupation_name) AS occupation_name,

        MAX(IF(bolge = 'Türkiye', agirlik, NULL))
            AS agirlik_tr,

        MAX(IF(bolge = 'Dünya', agirlik, NULL))
            AS agirlik_dunya,

        MAX(IF(bolge = 'Türkiye', artifact_pct / 100, NULL))
            AS oran_tr,

        MAX(IF(bolge = 'Dünya', artifact_pct / 100, NULL))
            AS oran_dunya

    FROM agirliklar
    GROUP BY occupation_code
),

etkiler AS (
    SELECT
        occupation_name,

        (agirlik_tr - agirlik_dunya)
        * (oran_tr + oran_dunya) / 2 * 100
            AS dagilim_etkisi,

        (oran_tr - oran_dunya)
        * (agirlik_tr + agirlik_dunya) / 2 * 100
            AS kategori_ici_etki,

        agirlik_tr * oran_tr * 100
            AS turkiye_katki,

        agirlik_dunya * oran_dunya * 100
            AS dunya_katki

    FROM karsilastirma
)

-- ADIM 21
-- Kod düzeltme çıktısının genel ayrıştırma özeti

SELECT
    ROUND(SUM(dagilim_etkisi), 4)
        AS toplam_dagilim_etkisi,

    ROUND(SUM(kategori_ici_etki), 4)
        AS toplam_kategori_ici_etki,

    ROUND(
        SUM(dagilim_etkisi + kategori_ici_etki),
        4
    ) AS toplam_fark,

    ROUND(SUM(turkiye_katki), 4)
        AS turkiye_agirlikli_oran,

    ROUND(SUM(dunya_katki), 4)
        AS dunya_agirlikli_oran,

    ROUND(
        SUM(turkiye_katki) - SUM(dunya_katki),
        4
    ) AS kontrol_farki

FROM etkiler;
