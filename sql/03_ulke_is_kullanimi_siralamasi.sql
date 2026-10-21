-- Türkiye'nin kullanım amaçlarına göre ülke sıralamaları
-- Yüksek kullanım payı, daha üst sıra anlamına gelir.

WITH siralamalar AS (
    SELECT
        date_start,
        geo_id,
        work_pct,
        personal_pct,
        coursework_pct,
        automation_pct,

        COUNT(*) OVER (
            PARTITION BY date_start
        ) AS toplam_ulke,

        RANK() OVER (
            PARTITION BY date_start
            ORDER BY work_pct DESC
        ) AS is_sirasi,

        RANK() OVER (
            PARTITION BY date_start
            ORDER BY personal_pct DESC
        ) AS kisisel_sirasi,

        RANK() OVER (
            PARTITION BY date_start
            ORDER BY coursework_pct DESC
        ) AS egitim_sirasi,

        RANK() OVER (
            PARTITION BY date_start
            ORDER BY automation_pct DESC
        ) AS otomasyon_sirasi

    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.ulke_kullanim_amaclari_2026`
)

SELECT
    date_start AS donem,
    toplam_ulke,
    is_sirasi,
    kisisel_sirasi,
    egitim_sirasi,
    otomasyon_sirasi
FROM siralamalar
WHERE geo_id = 'TUR'
ORDER BY donem;
