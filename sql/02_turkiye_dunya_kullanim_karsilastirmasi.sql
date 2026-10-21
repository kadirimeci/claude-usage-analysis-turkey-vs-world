-- Türkiye ve dünya genelinde Claude kullanım karşılaştırması
-- Farklar yüzde puan cinsinden hesaplanmaktadır.

SELECT
    t.date_start AS donem,

    t.work_pct AS turkiye_is,
    d.work_pct AS dunya_is,
    ROUND(t.work_pct - d.work_pct, 2) AS is_farki,

    t.personal_pct AS turkiye_kisisel,
    d.personal_pct AS dunya_kisisel,
    ROUND(t.personal_pct - d.personal_pct, 2) AS kisisel_farki,

    t.coursework_pct AS turkiye_egitim,
    d.coursework_pct AS dunya_egitim,
    ROUND(t.coursework_pct - d.coursework_pct, 2) AS egitim_farki,

    t.automation_pct AS turkiye_otomasyon,
    d.automation_pct AS dunya_otomasyon,
    ROUND(t.automation_pct - d.automation_pct, 2) AS otomasyon_farki,

    t.augmentation_pct AS turkiye_is_birligi,
    d.augmentation_pct AS dunya_is_birligi,
    ROUND(t.augmentation_pct - d.augmentation_pct, 2) AS is_birligi_farki

FROM
    `prefab-bruin-483617-b9.anthropic_ai_analiz.ulke_kullanim_amaclari_2026` AS t

INNER JOIN
    `prefab-bruin-483617-b9.anthropic_ai_analiz.kuresel_kullanim_2026` AS d
    ON t.date_start = d.date_start

WHERE
    t.geo_id = 'TUR'

ORDER BY
    donem;
