# Türkiye–Dünya Claude Kullanımı | Toplu Analiz

Dönem: Nisan–Mayıs 2026. Veriler Claude etkileşimlerini ve mesleki görev sınıflandırmalarını temsil eder; nüfus geneli veya çalışan meslekleri hakkında doğrudan çıkarım yapılamaz.

## Veri kontrolleri
- Çıktı ayrıştırması: 64 satır, 32 çıktı türü; maksimum ayrıştırma yuvarlama hatası 0.000100 yüzde puan.
- Kapsam karşılaştırması: 128 satır.
- Otomasyon karşılaştırması: 40 satır, 20 ortak meslek kategorisi.
- İki ayda aynı işaretli çıktı farkı: 31/32. Çok küçük değerlerde işaret değişimi pratik önem taşımayabilir.

## Çıktı türleri: iki ayda en yüksek ortalama mutlak farklar
- artifact_document_or_report_pct: Nisan -3.1882, Mayıs -2.9972 yüzde puan; Güçlü ve tutarlı.
- artifact_email_or_message_pct: Nisan -2.3271, Mayıs -2.3624 yüzde puan; Güçlü ve tutarlı.
- artifact_code_fix_or_debug_pct: Nisan +2.3980, Mayıs +2.0030 yüzde puan; Güçlü ve tutarlı.
- artifact_explanation_or_answer_pct: Nisan +1.4725, Mayıs +1.6198 yüzde puan; Güçlü ve tutarlı.
- artifact_app_or_website_pct: Nisan +1.5128, Mayıs +1.5447 yüzde puan; Güçlü ve tutarlı.
- artifact_script_or_snippet_pct: Nisan +1.3541, Mayıs +1.3666 yüzde puan; Güçlü ve tutarlı.
- artifact_resume_or_job_application_pct: Nisan -1.0437, Mayıs -1.0009 yüzde puan; Güçlü ve tutarlı.
- artifact_academic_paper_or_thesis_pct: Nisan +0.5144, Mayıs +0.7676 yüzde puan; Güçlü ve tutarlı.
- artifact_none_pct: Nisan -0.8122, Mayıs -0.3986 yüzde puan; Küçük/değişken fark.
- artifact_marketing_or_social_content_pct: Nisan -0.6221, Mayıs -0.5615 yüzde puan; Güçlü ve tutarlı.

## Çıktı ayrıştırması

- 2026-04: 32 çıktı türünün 26 tanesinde mutlak kategori içi etki, mutlak dağılım etkisinden büyük.
- 2026-05: 32 çıktı türünün 24 tanesinde mutlak kategori içi etki, mutlak dağılım etkisinden büyük.

## Meslek kapsamı

- 2026-04 Dünya: genel çıktı toplamı 100.020%, mesleklerden ağırlıklı toplam 94.582%, fark 5.438 puan (22 kategori).
- 2026-04 Türkiye: genel çıktı toplamı 100.010%, mesleklerden ağırlıklı toplam 95.742%, fark 4.268 puan (20 kategori).
- 2026-05 Dünya: genel çıktı toplamı 100.030%, mesleklerden ağırlıklı toplam 98.739%, fark 1.291 puan (22 kategori).
- 2026-05 Türkiye: genel çıktı toplamı 99.980%, mesleklerden ağırlıklı toplam 98.341%, fark 1.639 puan (20 kategori).

## Otomasyon ayrıştırması

- 2026-04: Türkiye 50.5471%, dünya 48.9639%; fark +1.5832 puan; dağılım +1.0192, kategori içi +0.5640 puan.
  - Pozitif katkısı en yüksek 3 kategori: Computer and Mathematical (+3.765); Architecture and Engineering (+0.731); Life, Physical, and Social Science (+0.518).
  - Negatif katkısı en yüksek 3 kategori: Educational Instruction and Library (-0.588); Business and Financial Operations (-0.658); Office and Administrative Support (-1.042).
- 2026-05: Türkiye 49.9832%, dünya 48.6075%; fark +1.3757 puan; dağılım +0.9163, kategori içi +0.4594 puan.
  - Pozitif katkısı en yüksek 3 kategori: Computer and Mathematical (+3.285); Architecture and Engineering (+0.799); Life, Physical, and Social Science (+0.316).
  - Negatif katkısı en yüksek 3 kategori: Management (-0.487); Educational Instruction and Library (-0.666); Office and Administrative Support (-0.946).

## Metodolojik notlar
- Ayrıştırmalar 20 ortak meslek kategorisi üzerinde, her bölge ve ay için ayrı ayrı %100’e normalize edilen ağırlıklarla hesaplanır.
- Ayrıştırma terimleri matematiksel katkılardır, nedensel etki değildir.
- Meslek temelli çıktı toplamları ile genel çıktı oranları aynı kapsamda değildir; farkları doğrudan belirli eksik mesleklere atfetmeyin.
- Kategorilerin kullanım oranları ve otomasyon oranları kaynakta iki ondalığa yuvarlanmış olduğundan hesaplarda küçük sapmalar beklenir.
- İşaret tutarlılığı istatistiksel anlamlılık kanıtı değildir; bu dosyalarda örneklem büyüklüğü ve belirsizlik aralıkları yoktur.
- Bu paket yalnızca 24–26. adımlardan elde edilen CSV dosyalarını kullanır. Diğer analizlerin ham tablolarını içermediği için yeni görev/amaç çapraz analizleri üretilmez.
