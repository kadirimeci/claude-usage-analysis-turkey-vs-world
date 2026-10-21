-- Meslek kullanım ağırlıkları ile çıktı türlerinin eşleştirilmesi
-- Mayıs 2026 | Türkiye ve Dünya

WITH birlesik AS (
    SELECT
        c.date_start,
        c.bolge,
        c.occupation_code,
        c.occupation_name,
        c.artifact_code,
        c.artifact_pct,
        m.usage_pct AS occupation_usage_pct

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_cikti_profili_2026` c

    LEFT JOIN
        `prefab-bruin-483617-b9.anthropic_ai_analiz.meslek_kullanim_profili_2026` m

    ON c.date_start = m.date_start
       AND c.bolge = m.bolge
       AND CAST(c.occupation_code AS STRING)
           = CAST(m.occupation_code AS STRING)

    WHERE c.date_start = DATE '2026-05-01'
)

SELECT
    bolge,
    COUNT(*) AS toplam_kayit,
    COUNT(DISTINCT occupation_code) AS meslek_sayisi,
    COUNT(DISTINCT artifact_code) AS cikti_turu_sayisi,
    COUNTIF(occupation_usage_pct IS NULL) AS eslesmeyen_kayit,

    ROUND(
        SUM(
            IF(
                artifact_code = 'artifact_code_fix_or_debug_pct',
                occupation_usage_pct * artifact_pct / 100,
                0
            )
        ),
        2
    ) AS kod_duzeltme_agirlikli_payi

FROM birlesik

GROUP BY bolge
ORDER BY bolge;
