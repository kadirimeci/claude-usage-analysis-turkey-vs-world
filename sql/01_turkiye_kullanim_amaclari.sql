-- 1. Türkiye'nin kullanım amaçlarını ve otomasyon oranlarını inceleme

SELECT
    date_start AS donem,
    geo_id AS ulke_kodu,
    work_pct AS is_amacli_kullanim,
    personal_pct AS kisisel_kullanim,
    coursework_pct AS egitim_amacli_kullanim,
    automation_pct AS otomasyon,
    augmentation_pct AS insan_ai_is_birligi
FROM
    prefab-bruin-483617-b9.anthropic_ai_analiz.ulke_kullanim_amaclari_2026
WHERE
    geo_id = 'TUR'
ORDER BY
    donem;
