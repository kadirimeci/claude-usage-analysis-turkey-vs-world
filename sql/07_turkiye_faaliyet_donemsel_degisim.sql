-- Türkiye'de Nisan-Mayıs 2026 faaliyet değişimleri
-- Yalnızca iki dönemde de bulunan faaliyetler

WITH nisan AS (
    SELECT
        task_code,
        usage_pct,
        work_pct,
        automation_pct
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.gorev_otomasyon_2026`
    WHERE
        bolge = 'Türkiye'
        AND date_start = DATE '2026-04-01'
),

mayis AS (
    SELECT
        task_code,
        task_name,
        usage_pct,
        work_pct,
        automation_pct
    FROM
        `prefab-bruin-483617-b9.anthropic_ai_analiz.gorev_otomasyon_2026`
    WHERE
        bolge = 'Türkiye'
        AND date_start = DATE '2026-05-01'
)

SELECT
    m.task_name AS faaliyet,

    n.usage_pct AS nisan_kullanim,
    m.usage_pct AS mayis_kullanim,
    ROUND(m.usage_pct - n.usage_pct, 2)
        AS kullanim_degisim_puan,

    n.work_pct AS nisan_is_amacli,
    m.work_pct AS mayis_is_amacli,
    ROUND(m.work_pct - n.work_pct, 2)
        AS is_amacli_degisim_puan,

    n.automation_pct AS nisan_otomasyon,
    m.automation_pct AS mayis_otomasyon,
    ROUND(m.automation_pct - n.automation_pct, 2)
        AS otomasyon_degisim_puan

FROM mayis AS m

INNER JOIN nisan AS n
    ON m.task_code = n.task_code

ORDER BY
    kullanim_degisim_puan DESC;
