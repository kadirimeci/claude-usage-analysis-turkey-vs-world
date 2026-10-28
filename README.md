# Türkiye ve Dünya Genelinde Claude Kullanımı | Veri Analizi

**Anthropic Economic Index (AEI) · Nisan–Mayıs 2026 · Python · Google BigQuery / SQL · Power BI**

Türkiye'deki Claude kullanımının dünya geneliyle nasıl farklılaştığını inceleyen, gerçek veri kaynaklarına dayalı bağımsız bir veri analizi projesidir. Çalışma; kullanım amaçlarını, mesleki görev sınıflandırmalarını, otomasyon ve iş birliği biçimlerini, çıktı türlerini ve dönemsel değişimleri karşılaştırır.

> **Proje durumu:** Veri hazırlama, Python ve SQL analizleri, ayrıştırma hesaplamaları, temel doğrulamalar ve altı sayfalık Power BI raporu tamamlandı. Bulgular LinkedIn'de bir araştırma makalesi olarak yayımlandı.

## Araştırma soruları

- Claude etkileşimleri Türkiye'de iş, kişisel ve eğitim amaçları arasında nasıl dağılıyor?
- Türkiye ile dünya genelinin kullanım profilleri hangi alanlarda ayrışıyor?
- Kaynak verideki mesleki görev sınıflandırmalarının dağılımı nasıl değişiyor?
- Otomasyon ile insan destekli kullanım biçimleri nasıl farklılaşıyor?
- Belge, e-posta, açıklama, kod ve uygulama gibi çıktı türleri nasıl dağılıyor?
- Gözlenen farkların ne kadarı kategori dağılımından, ne kadarı kategori içindeki oranlardan kaynaklanıyor?
- Nisan–Mayıs döneminde Türkiye ve dünya genelindeki göreli kullanım payları nasıl değişiyor?

## Veri kaynağı ve kapsam

| Alan | Açıklama |
|---|---|
| Kaynak | [Anthropic Economic Index](https://www.anthropic.com/economic-index) |
| Projede kullanılan veri sürümü | 26 Haziran 2026 olarak belgelenmiş sürüm |
| Dönem | Nisan ve Mayıs 2026 |
| Coğrafya | Türkiye (`TUR`) ve dünya geneli (`global`) |
| Analiz birimi | Toplulaştırılmış ve sınıflandırılmış Claude etkileşimlerine ait oranlar |

Ham kaynak veri dosyası, boyutu nedeniyle bu depoya dahil edilmemiştir. Kaynak verinin kullanım ve erişim koşulları için ilgili veri sağlayıcısının dokümantasyonu esas alınmalıdır.

## Seçilmiş bulgular

Aşağıdaki kullanım amacı oranları Mayıs 2026 dönemine aittir:

| Kullanım amacı | Türkiye | Dünya geneli | Türkiye − dünya |
|---|---:|---:|---:|
| İş | %40,37 | %43,36 | −2,99 yüzde puan |
| Kişisel | %43,34 | %40,20 | +3,14 yüzde puan |
| Eğitim / ders | %16,29 | %16,45 | −0,16 yüzde puan |

**Mesleki dağılım:** Projede kullanılan sınıflandırmaya göre Türkiye'de Bilgisayar ve Matematik kategorisinin Mayıs 2026 kullanım payı %28,15; dünya genelinde %23,80 olarak hesaplandı. Bu oranlar ilgili mesleklerde çalışan kişilerin Claude kullanma oranlarını göstermez.

**Otomasyon ve iş birliği:** Tamamlanan Power BI raporu için belgelenen ağırlıklandırılmış Mayıs sonuçları Türkiye'de yaklaşık %49,98 otomasyon ve %50,02 iş birliği; dünya genelinde %48,63 otomasyon ve %51,37 iş birliğidir. Bu değerler, aşağıda açıklanan **20 ortak kategoriye yeniden ağırlıklandırılmış ayrıştırma** sonuçlarıyla aynı kapsamda kabul edilmemelidir.

### Ayrıştırma analizinin ayrı kapsamı

Önceki Python/SQL analizlerinde **20 ortak görev kategorisi** kullanılarak yapılan yeniden ağırlıklandırılmış Mayıs karşılaştırmasında:

- Kod düzeltme / hata ayıklama çıktı türünde fark: **+2,00 yüzde puan**
- Uygulama / web sitesi çıktı türünde fark: **+1,54 yüzde puan**
- Belge / rapor çıktı türünde fark: **−3,00 yüzde puan**
- E-posta / mesaj çıktı türünde fark: **−2,36 yüzde puan**

Aynı 20 ortak kategori kapsamındaki otomasyon farkı **+1,3757 yüzde puan** olarak hesaplanmıştır. Simetrik Kitagawa ayrıştırmasında bu farkın **+0,9163 yüzde puanı kategori dağılımı**, **+0,4594 yüzde puanı kategori içi oranlar** bileşenidir.

> **Kapsam uyarısı:** Bu ayrıştırma, ortak kategoriler üzerinde ayrı bir normalizasyon ve ağırlıklandırma kullanır. Genel Power BI otomasyon oranlarıyla sayısal olarak birebir eşit olması beklenmemelidir. Buradaki farklar tanımlayıcıdır; nedensellik veya istatistiksel anlamlılık kanıtı değildir.

## Kullanılan araçlar

| Araç | Kullanım |
|---|---|
| Python | Veri keşfi, dönüşüm, kalite kontrolü, ayrıştırma ve doğrulama betikleri |
| Google BigQuery / SQL | Veri sorgulama, gruplama ve Türkiye–dünya karşılaştırmaları |
| Power BI | Altı sayfalık analiz raporu, ölçümler ve etkileşimli görselleştirmeler |
| CSV / Markdown | Ara sonuçlar, karşılaştırma tabloları ve analiz raporları |

## Proje yapısı

```text
anthropic-ai-usage-analysis/
├── README.md
├── .gitignore
├── Claude_Kullanim_Analizi_2026.pbix   # Power BI raporu
├── scripts/                         # Python analiz ve doğrulama betikleri
├── sql/                             # BigQuery SQL sorguları
├── outputs/                         # CSV analiz çıktıları ve toplu analiz raporu
└── data/                            # Yerel kaynak veri; depoya dahil edilmeyebilir
```

- `scripts/`: Veri keşfi, analiz ve doğrulama adımları için Python betikleri.
- `sql/`: BigQuery üzerinde kullanılan SQL sorguları.
- `outputs/`: Analizlerin ürettiği CSV tabloları ve `07_TOPLU_ANALIZ_RAPORU.md`.
- `Claude_Kullanim_Analizi_2026.pbix`: Power BI Desktop ile açılabilen tamamlanmış rapor.
- `data/`: Yerel kaynak veri alanı; ham dosyaların tamamı GitHub'da bulunmayabilir.

> Power BI `.pbix` dosyası GitHub üzerinde etkileşimli olarak görüntülenmez. Raporu incelemek için dosyayı indirip Power BI Desktop ile açmak gerekir.

## Çalıştırma ve doğrulama

Python 3 ve gerekli bağımlılıkların kurulu olduğu bir ortam kullanılmalıdır. Bazı betikler yerel `data/` klasöründeki kaynak CSV dosyalarına, SQL sorguları ise uygun BigQuery proje ve tablolarına ihtiyaç duyar.

Aşağıdaki örnekler Windows PowerShell içindir ve proje ana dizininde çalıştırılır:

**Mevcut çıktıların temel doğrulaması:**

```powershell
.\.venv\Scripts\python.exe .\scripts\19_proje_veri_dogrulama.py
```

**İki dönemlik meslek ayrıştırma analizi:**

```powershell
.\.venv\Scripts\python.exe .\scripts\13_meslek_ayristirma_analizi.py
```

**Toplu analiz:**

```powershell
.\.venv\Scripts\python.exe .\scripts\18_toplu_analiz.py
```

Bu komutlar mevcut proje dosyalarında belgelenen betik adlarına dayanmaktadır; tüm bağımlılıkların veya veri erişimlerinin farklı bir bilgisayarda hazır olduğu varsayılmamalıdır. Proje tek komutla uçtan uca yeniden üretim garantisi vermez.

## Yorumlama sınırları

- Mesleki sınıflandırmalar, Claude etkileşimlerinin ilişkilendirildiği görev/meslek alanlarına dayanır; kullanıcıların doğrulanmış meslekleri olarak yorumlanamaz.
- Meslek gruplarının kullanım payı, o meslekteki çalışanların Claude benimseme oranı değildir.
- Otomasyon, sınıflandırılmış Claude etkileşiminin kullanım biçimidir; bir mesleğin otomatikleştirilebilir görev oranını veya iş kaybı riskini ölçmez.
- Sonuçlar yalnızca incelenen Claude verilerine aittir; Türkiye'deki bütün yapay zekâ araçlarının kullanımını temsil etmez.
- Dünya geneli Türkiye'yi de içerir; karşılaştırma Türkiye ile Türkiye dışındaki ülkeler arasında değildir.
- Yalnızca iki ay incelendiğinden uzun dönemli eğilim ve nedensellik çıkarımı yapılamaz.
- Kapsam ve kategori eşleşmeleri nedeniyle bazı payların toplamı %100'e ulaşmayabilir. Farklı normalizasyon ve ağırlıklandırma yöntemleriyle hesaplanan oranlar doğrudan eşitlenmemelidir.
- Örneklem büyüklüğü ve güven aralığına ilişkin yeterli bilgi olmadan istatistiksel anlamlılık iddiası kurulmaz.

---

**Kaynak:** Anthropic Economic Index (AEI). Bu depo bağımsız bir portföy çalışmasıdır; Anthropic tarafından hazırlanmış veya onaylanmış resmî bir rapor değildir.
