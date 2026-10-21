# Türkiye ve Dünya Genelinde Claude Kullanımı | Veri Analizi

**Anthropic Economic Index · Nisan–Mayıs 2026 · Python · Google BigQuery SQL**

Türkiye'deki Claude kullanımının dünya genelinden nasıl ayrıştığını inceleyen veri analizi projesi. Çalışma; **kullanım amaçları, mesleki görev kategorileri, otomasyon / insan destekli kullanım biçimleri ve üretilen çıktı türleri** üzerine odaklanır.

> **Proje durumu:** Veri hazırlama, karşılaştırmalı analizler, ayrıştırma hesaplamaları ve temel doğrulamalar tamamlandı. **Power BI dashboard'u geliştirme aşamasındadır.**

## Araştırma soruları

- Claude etkileşimleri Türkiye'de iş, kişisel ve eğitim amaçları arasında nasıl dağılıyor?
- Türkiye ile dünya genelinin kullanım profilleri hangi alanlarda farklılaşıyor?
- Mesleki **görev kategorileri** ve bu kategorilerin kullanım ağırlıkları sonuçları nasıl etkiliyor?
- Otomasyon ile insan destekli kullanım oranları nasıl ayrışıyor?
- Belge, e-posta, açıklama, kod, uygulama ve diğer çıktı türlerinin payları nasıl değişiyor?
- Gözlenen farkların ne kadarı görev kategorilerinin **dağılımından**, ne kadarı **kategori içindeki oranlardan** geliyor?

## Veri kaynağı ve kapsam

- **Kaynak:** [Anthropic Economic Index](https://www.anthropic.com/economic-index)
- **Veri sürümü:** 26 Haziran 2026
- **İncelenen dönem:** Nisan ve Mayıs 2026
- **Coğrafya:** Türkiye (`TUR`) ve dünya geneli (`global`)
- **Analiz birimi:** Toplulaştırılmış ve sınıflandırılmış Claude etkileşimlerine ait oranlar

Ham veri dosyası boyutu nedeniyle bu depoya eklenmemiştir. Kaynak veriye ilişkin kullanım koşulları için Anthropic'in yayımladığı veri ve dokümantasyon esas alınmalıdır.

## Öne çıkan bulgular

| Gösterge | Türkiye · Mayıs 2026 | Dünya · Mayıs 2026 | Türkiye − dünya |
|---|---:|---:|---:|
| İş amaçlı kullanım | %40,37 | %43,36 | −2,99 yp |
| Kişisel kullanım | %43,34 | %40,20 | +3,14 yp |
| Eğitim / ders amaçlı kullanım | %16,29 | %16,45 | −0,16 yp |
| Otomasyon | %50,00 | %48,62 | +1,38 yp |

**Çıktı profili:** 20 ortak görev kategorisi üzerinde yeniden ağırlıklandırılmış Mayıs karşılaştırmasında kod düzeltme / hata ayıklama **+2,00 yp**, uygulama / web sitesi **+1,54 yp**; belge / rapor **−3,00 yp** ve e-posta / mesaj **−2,36 yp** fark göstermektedir.

**Otomasyon ayrıştırması:** 20 ortak görev kategorisindeki Mayıs otomasyon farkı **+1,3757 yüzde puandır**. Simetrik ayrıştırmada bunun **+0,9163 puanı dağılım**, **+0,4594 puanı kategori içi** bileşendir.

Bu değerler **tanımlayıcı** bulgulardır; neden-sonuç ilişkisi veya istatistiksel anlamlılık kanıtı değildir.

## Kullanılan araçlar ve yöntemler

| Araç | Kullanım |
|---|---|
| Python | Veri keşfi, kalite kontrolleri, dönüşümler ve ayrıştırma hesaplamaları |
| Google BigQuery / SQL | Türkiye–dünya karşılaştırmaları, gruplama ve veri analizi |
| CSV | Ara analiz tablolarının ve sonuçların aktarımı |
| Power BI | Planlanan etkileşimli dashboard; henüz tamamlanmadı |

Meslek kategorileri arasındaki farklar için **simetrik Kitagawa ayrıştırması** kullanılmıştır. Ortak 20 kategorinin kullanım payları, her bölge ve dönem için kendi içinde %100'e normalize edilmiştir. Böylece toplam fark, *dağılım bileşeni* ve *kategori içi bileşen* olarak raporlanmıştır.

## Proje dosyaları

```text
anthropic-ai-usage-analysis/
├── README.md
├── .gitignore
├── 01_veri_kesfi.py ... 19_proje_veri_dogrulama.py
├── sql/                         # BigQuery analiz sorguları
├── outputs/                     # İşlenmiş analiz sonuçları ve raporlar
├── adim24_cikti_ayristirma.csv
├── adim25_kapsam.csv
├── adim26_otomasyon.csv
└── data/                        # Ham veri (GitHub'a eklenmez)
```

Python dosyaları analiz sürecinin adımlarına göre numaralandırılmıştır. `sql/` klasöründeki sorgular, BigQuery geçmişinden arşivlenen çalışmaları içerir. `outputs/` klasörü ise analizlerin oluşturduğu tabloları ve özet raporları barındırır.

## Çalıştırma ve doğrulama

Python 3 ve gerekli paketlerin kurulu olduğu bir sanal ortam kullanın. Bazı veri hazırlama betikleri, yerel `data/` klasöründeki kaynak CSV'yi gerektirir. BigQuery üzerinde çalışan sorgular için ayrıca uygun Google Cloud projesi ve veri tabloları gereklidir.

Mevcut çıktı dosyalarının temel kontrollerini çalıştırmak için Windows PowerShell'de:

```powershell
.\.venv\Scripts\python.exe 19_proje_veri_dogrulama.py
```

İş amaçlı kullanımın iki dönemlik meslek ayrıştırmasını yeniden üretmek için:

```powershell
.\.venv\Scripts\python.exe 13_meslek_ayristirma_analizi.py
```

Toplu analiz için:

```powershell
.\.venv\Scripts\python.exe 18_toplu_analiz.py
```

> **Tekrar üretilebilirlik notu:** Bütün iş akışının sıfırdan çalışması için kaynak verinin temin edilmesi, gerekli Python bağımlılıklarının kurulması ve BigQuery tablolarının oluşturulması gerekir. Bu depo tek komutla uçtan uca yeniden üretim garantisi vermez.

## Yorumlama sınırları

- **Meslek** etiketleri, kullanıcıların gerçek meslekleri değil, etkileşimlerin ilişkilendirildiği **görev alanlarıdır**.
- **Otomasyon**, sınıflandırılmış etkileşim biçimini ifade eder; bir işin tamamen insansız yürütüldüğü anlamına gelmez.
- Sonuçlar **Claude etkileşimleriyle** ilgilidir; Türkiye'de yapay zekâ benimseme oranı veya nüfus genelindeki kullanım oranı değildir.
- Karşılaştırılan **dünya geneli Türkiye'yi de içerir**.
- İncelenen dönem yalnızca **iki aydır**; uzun vadeli eğilim veya nedensellik iddiası kurulamaz.
- Örneklem büyüklüğü ve güven aralığı bilgisi bulunmadığından gözlenen farklar için istatistiksel anlamlılık iddiasında bulunulmaz.
- Genel çıktı oranları ile 20 ortak görev kategorisinde **yeniden ağırlıklandırılmış** ayrıştırma oranları farklı kapsamlara sahiptir; doğrudan birbirine eşitlenmemelidir.

## Sonraki aşama

Power BI ile yönetici özeti, kullanım amaçları, görev kategorileri, otomasyon ayrıştırması, çıktı türleri ve metodoloji sayfalarından oluşan bir dashboard hazırlanması planlanmaktadır.

---

**Veri kaynağı:** Anthropic Economic Index. Bu çalışma bağımsız bir portföy projesidir; Anthropic tarafından hazırlanmış veya onaylanmış resmî bir rapor değildir.
