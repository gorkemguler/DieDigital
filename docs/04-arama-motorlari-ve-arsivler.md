# 4. Arama motorları ve arşivler

Arama motoru içeriği barındırmaz, sadece gösterir. Bu yüzden sıra hep aynı:

1. **Kaynağı** kaldırt ya da değiştirt: kendin sil ([2. bölüm](02-icerik-temizligi.md)), site sahibinden iste ([6. bölüm](06-baskalarinin-elindeki-izler.md)), yasal yola başvur ([8. bölüm](08-hukuki-haklar.md)).
2. Sonra arama motorundan sonucun **güncellenmesini** ya da **kaldırılmasını** iste.

Kaynak durdukça arama motorundan kaldırılan sonuç geri gelir. İstisna: kaynağa ulaşamadığın durumlar (site sahibi cevap vermiyor, yurt dışında, terk edilmiş); orada doğrudan arama motoruna başvurursun.

## 4.1 Önce ne çıktığını gör

**Nasıl aranır:**

- Gizli pencerede, tüm hesaplardan çıkmış olarak ara. Kişiselleştirilmiş sonuçlar yanıltır.
- Google, Bing, Yandex ve DuckDuckGo'da ayrı ayrı ara; sonuçlar farklıdır.
- İlk iki sayfaya değil, en az beş sayfaya bak.
- Bulduğun her sonucu bir tabloya yaz: adres, ne var (ad, fotoğraf, telefon...), kaynağın sahibi, ne yapılacak.

**Aranacak sorgular** (her birinde kendi bilgini yaz):

| Ne | Sorgu |
|---|---|
| Adın | `"Ad Soyad"` |
| Adın ve şehrin | `"Ad Soyad" "Şehir"` |
| Adın ve işin/okulun | `"Ad Soyad" "Şirket"` · `"Ad Soyad" "Üniversite"` |
| Adının farklı yazılışları | `"Ad Soyad"` · `"Soyad Ad"` · `"A. Soyad"` · Türkçe karaktersiz yazılış (`"Ayse Yilmaz"` gibi) |
| Sosyal medyada | `"Ad Soyad" site:linkedin.com` · `site:facebook.com` · `site:instagram.com` · `site:x.com` · `site:tiktok.com` |
| Belgelerde (CV, listeler, sonuçlar) | `"Ad Soyad" filetype:pdf` · `filetype:docx` · `filetype:xlsx` |
| Forum ve sözlüklerde | `"Ad Soyad" site:eksisozluk.com` · `site:reddit.com` |
| Resmî ilanlarda | `"Ad Soyad" site:gov.tr` · `site:ilan.gov.tr` |
| Arşivde | `"Ad Soyad" site:web.archive.org` |
| E-posta adresin | `"sen@ornek.com"` · `"sen"` (sadece @ işaretinden önceki kısım) |
| Kullanıcı adın | `"takma_adim"` |
| Telefonun | `"0532 123 45 67"` · `"05321234567"` · `"+90 532 123 45 67"` · `"532 123 45 67"` |
| Adresin | `"Sokak adı" "No"` · site adı ile |
| Plakan | `"34 ABC 123"` |

**Görseller:** Profil fotoğraflarınla ve sık kullandığın fotoğraflarınla Google Lens, Bing Görsel Arama ve Yandex Görseller'de tersine görsel araması yap. Yandex yüz eşleştirmede genellikle daha "başarılıdır". Yüz arama motorları için [5. bölüm](05-veri-simsarlari-ve-rehberler.md).

**Uyarı kur:** Google Alerts (https://www.google.com/alerts) ile adın, e-postan ve kullanıcı adın için uyarı oluştur; yeni bir sonuç çıkınca haberin olsun ([13. bölüm](13-takip-ve-bakim.md)).

> **Araçla:** `diedigital footprint dorks --name ... --email ... --phone ...` bu sorguların hepsini dört arama motoru için hazır bağlantılarla işaretlenebilir bir listeye döker.

## 4.2 Google

| Araç | Ne için |
|---|---|
| [Seninle ilgili sonuçlar](https://myactivity.google.com/results-about-you) | Telefon, adres, e-posta içeren sonuçların kaldırılması; yeni sonuç çıkınca uyarı. Bölgene göre henüz açık olmayabilir. |
| [Kişisel bilgilerin kaldırılması](https://support.google.com/websearch/troubleshooter/9685456) | İfşa (doxxing), kimlik numarası, banka/kart bilgisi, imza, tıbbi kayıt, rızasız özel görüntüler, reşit olmayanların görüntüleri. |
| [Güncel olmayan içerik](https://search.google.com/search-console/remove-outdated-content) | Kaynak sayfa silindi ya da değişti ama Google eski hâlini gösteriyor. En çok kullanacağın araç. |
| [Unutulma hakkı (AB)](https://reportcontent.google.com/forms/rtbf) | AB / AEA'da yaşıyorsan: "adım + bu URL" eşleşmesinin kaldırılması. |
| [Hukuki kaldırma talepleri](https://support.google.com/legal/answer/3110420) | Diğer hukuki gerekçeler; ülke olarak Türkiye seçilebilir. |

**"Güncel olmayan içerik" aracı nasıl kullanılır?**

1. Kaynak sayfa silindiyse ya da senin bilgin sayfadan çıkarıldıysa, Google'da çıkan sonucun adresini kopyala.
2. Araca yapıştır. Sayfa tamamen silindiyse Google kontrol edip sonucu kaldırır.
3. Sayfa duruyor ama adın çıkarıldıysa, "sayfada artık geçmeyen bir kelime" olarak adını yaz; Google önbellekteki açıklamayı günceller.

**Görseller:** Aynı araçlar Google Görseller için de geçerli. Kendi sitendeki bir görselse önce görseli kaldır, sonra güncel olmayan içerik aracını kullan.

## 4.3 Bing, DuckDuckGo, Yahoo

DuckDuckGo ve Yahoo sonuçlarının büyük kısmı Bing'den gelir; Bing'de yapılan kaldırma onlara da yansır.

- [Bing İçerik Kaldırma Aracı](https://www.bing.com/webmasters/tools/contentremoval): kaynak sayfa silinmiş ya da değişmişse eski sonucu ve önbelleği kaldırır.
- AB'de yaşıyorsan Bing'in Avrupa'ya özel arama sonucu engelleme formu (Bing'in gizlilik ve destek sayfalarında).

## 4.4 Yandex

Türkiye'de hâlâ kullanılıyor ve Google'ın kaldırdığı sonuçlar Yandex'te kalabiliyor. Site sahibiysen Yandex Webmaster'daki sayfa kaldırma aracını kullan. Değilsen Yandex destek formundan kaldırma iste; kaynak sayfa kaldırılmışsa sonuç genellikle bir süre sonra kendiliğinden düşer.

## 4.5 Türkiye'de yasal yol

**KVKK ve arama motorları:** Kişisel Verileri Koruma Kurulu'nun 23.06.2020 tarihli ve 2020/481 sayılı kararıyla, adınla yapılan aramalarda çıkan sonuçların indeksten çıkarılması için önce arama motoruna başvurabileceğin, sonuç alamazsan Kurul'a şikâyet edebileceğin kabul edildi. Kurul; bilginin güncelliği, kamusal rolün, haber değeri ve kamu yararı gibi ölçütlere bakar. Başvuru metni: [Ek B](ek-b-dilekce-ornekleri.md).

**5651 sayılı Kanun:**

- **md. 9:** Kişilik hakkını ihlal eden içerik için içerik veya yer sağlayıcıya başvurabilir ya da doğrudan sulh ceza hâkimliğine gidebilirsin. Hâkim içeriğin yayından çıkarılmasına, erişimin engellenmesine ve adının bu internet adresleriyle arama motorlarında ilişkilendirilmemesine karar verebilir.
- **md. 9/A:** Özel hayatın gizliliğini ihlal eden içerik için doğrudan Bilgi Teknolojileri ve İletişim Kurumu'na başvurarak acil erişim engeli istenebilir; karar sonradan hâkim onayına sunulur.

Bu yollar avukatla çok daha etkili işler. Haber sitelerindeki eski haberler için önce sitenin kendisinden isim kısaltması (A.B. gibi) veya haberin kaldırılmasını iste ([Ek B](ek-b-dilekce-ornekleri.md)); çoğu site makul taleplerde bunu yapıyor.

## 4.6 Arşivler

### Wayback Machine (archive.org)

Arşivde ne olduğunu görmek için: `https://web.archive.org/web/*/alanadi.com/*` (kendi siten, eski profillerin, hakkında sayfalar).

Internet Archive, kişisel veri içeren arşiv kayıtlarını talep üzerine kaldırıyor. URL listesiyle info@archive.org adresine e-posta gönder (metin: [Ek B](ek-b-dilekce-ornekleri.md)). Sitenin sahibiysen bunu belirt; sahibi değilsen sayfalarda adının ve bilgilerinin geçtiğini açıkla.

### archive.today (archive.ph, archive.is)

Kaldırma talepleri nadiren karşılanıyor. Yine de sitenin geri bildirim/kötüye kullanım bağlantısından, kişisel veri gerekçesiyle iste ve kaydını tut.

### Google önbelleği

Google 2024'te önbellek bağlantılarını kaldırdı. Arama sonucunda eski açıklama görünüyorsa "Güncel olmayan içerik" aracı yeterli.

### Toplu tarama veri setleri ve yapay zekâ

Common Crawl gibi veri setlerine girmiş eski taramalardan veri çıkarmak pratikte mümkün değil. Yapay zekâ şirketlerinin bazıları (ör. OpenAI: https://privacy.openai.com) modellerin seninle ilgili ürettiği kişisel bilgiler için itiraz ve silme formları sunuyor; diğerlerine GDPR/KVKK dilekçesi gönderebilirsin. Bir yapay zekâ asistanına adını sorup ne söylediğine bakmak da bir kontrol yöntemidir.

## Bölüm sonu kontrolü

- [ ] Tüm sorgular dört arama motorunda ve görsel aramada denendi, sonuçlar tabloya yazıldı
- [ ] Her sonuç için kaynak kaldırıldı ya da kaldırma istendi
- [ ] Kaynağı kaldırılan sonuçlar için Google ve Bing'e güncelleme talebi gönderildi
- [ ] Kaynağı kaldırılamayanlar için arama motoru / KVKK / 5651 yolu başlatıldı
- [ ] Wayback Machine'deki kayıtlar için kaldırma istendi
- [ ] Google Alerts kuruldu
