# 4. Arama motorları ve arşivler

Arama motoru içeriği barındırmaz, sadece gösterir. Bu yüzden sıra hep aynı:

1. **Kaynağı** kaldırt ya da değiştirt (site sahibi, platform, yasal yol).
2. Sonra arama motorundan sonucun **güncellenmesini** iste.

Kaynak durdukça arama motorundan kaldırılan sonuç geri gelir. İstisna: kaynağa ulaşamadığın durumlar (yurt dışında, sahibi cevap vermiyor); orada doğrudan arama motoruna başvurursun.

## Önce ne çıktığını gör

```bash
diedigital footprint dorks --name "Ad Soyad" --email sen@ornek.com \
  --username takma_adim --phone "+90 5xx xxx xx xx" --city İstanbul --out arama.md
```

`arama.md` her sorgu için Google, Bing, DuckDuckGo ve Yandex bağlantılarını içeren bir kontrol listesidir. İpuçları:

- Gizli pencerede ve oturum kapalıyken ara; kişiselleştirilmiş sonuçlar yanıltır.
- İlk iki sayfaya değil, en az beş sayfaya bak.
- Telefon numarası için araç farklı yazılışları (0532 123 45 67, 05321234567, +90...) birlikte arar.
- **Görseller:** Profil fotoğraflarınla Google Lens, Bing Görsel Arama ve Yandex Görseller'de tersine görsel araması yap. Yüz arama motorları için [05](05-veri-simsarlari-ve-rehberler.md).

Bulduğun her sonucu envantere ekle (`diedigital inventory add ...`).

## Google

| Araç | Ne için |
|---|---|
| [Seninle ilgili sonuçlar](https://myactivity.google.com/results-about-you) | Telefon, adres, e-posta içeren sonuçların kaldırılması; yeni sonuç çıkınca uyarı. Bölgene göre henüz açık olmayabilir. |
| [Kişisel bilgilerin kaldırılması](https://support.google.com/websearch/troubleshooter/9685456) | İfşa (doxxing), kimlik numarası, banka/kart bilgisi, imza, tıbbi kayıt, rızasız özel görüntüler, reşit olmayanların görüntüleri. |
| [Güncel olmayan içerik](https://search.google.com/search-console/remove-outdated-content) | Kaynak sayfa silindi ya da değişti ama Google eski hâlini gösteriyor. En çok kullanacağın araç. |
| [Unutulma hakkı (AB)](https://reportcontent.google.com/forms/rtbf) | AB / AEA'da yaşıyorsan: "adım + bu URL" eşleşmesinin kaldırılması. |
| [Hukuki kaldırma talepleri](https://support.google.com/legal/answer/3110420) | Diğer hukuki gerekçeler; ülke olarak Türkiye seçilebilir. |

## Bing, DuckDuckGo, Yahoo

DuckDuckGo ve Yahoo sonuçlarının büyük kısmı Bing'den gelir; Bing'de yapılan kaldırma onlara da yansır.

- [Bing İçerik Kaldırma Aracı](https://www.bing.com/webmasters/tools/contentremoval): kaynak sayfa silinmiş/değişmişse eski sonucu ve önbelleği kaldırır.
- AB'de yaşıyorsan Bing'in Avrupa'ya özel arama sonucu engelleme formu (Bing > Gizlilik bölümünde).

## Yandex

Türkiye'de hâlâ kullanılıyor ve Google'ın kaldırdığı sonuçlar Yandex'te kalabiliyor. Site sahibiysen Yandex Webmaster'daki "Remove pages from search" aracını kullan. Değilsen Yandex destek formundan kaldırma iste; kaynak sayfa kaldırılmışsa genellikle kendiliğinden düşer.

## Türkiye'de yasal yol

**KVKK ve arama motorları:** Kişisel Verileri Koruma Kurulu'nun 23.06.2020 tarihli ve 2020/481 sayılı kararıyla, adınla yapılan aramalarda çıkan sonuçların indeksten çıkarılması için önce arama motoruna başvurabileceğin, sonuç alamazsan Kurul'a şikâyet edebileceğin kabul edildi. Kurul; bilginin güncelliği, kamusal rolün, haber değeri ve kamu yararı gibi ölçütlere bakar.

**5651 sayılı Kanun:**

- **md. 9:** Kişilik hakkını ihlal eden içerik için içerik veya yer sağlayıcıya başvurabilir ya da doğrudan sulh ceza hâkimliğine gidebilirsin. Hâkim içeriğin yayından çıkarılmasına, erişimin engellenmesine ve adının bu internet adresleriyle arama motorlarında ilişkilendirilmemesine karar verebilir.
- **md. 9/A:** Özel hayatın gizliliğini ihlal eden içerik için doğrudan Bilgi Teknolojileri ve İletişim Kurumu'na başvurarak acil erişim engeli istenebilir; karar sonradan hâkim onayına sunulur.

Bu yollar avukatla çok daha etkili işler. Özellikle haber sitelerindeki eski haberler için önce sitenin kendisinden isim kısaltması (A.B. gibi) veya haberin kaldırılmasını iste; çoğu site makul taleplerde bunu yapıyor.

## Arşivler

### Wayback Machine (archive.org)

Internet Archive, kişisel veri içeren arşiv kayıtlarını talep üzerine kaldırıyor. URL listesiyle e-posta gönder:

```bash
diedigital letters render --template archive-removal \
  --url https://eskisitem.com/hakkimda --url https://forum.ornek.com/uye/ben --out arsiv.txt
```

`arsiv.txt`'yi kontrol et, sonra info@archive.org adresine gönder. Arşivde ne olduğunu görmek için: `https://web.archive.org/web/*/alanadi.com/*`

### archive.today (archive.ph, archive.is)

Kaldırma talepleri nadiren karşılanıyor. Yine de sitenin geri bildirim/kötüye kullanım bağlantısından, kişisel veri gerekçesiyle iste ve kaydını tut.

### Google önbelleği

Google 2024'te önbellek bağlantılarını kaldırdı. Arama sonucunda eski açıklama (snippet) görünüyorsa "Güncel olmayan içerik" aracı yeterli.

### Toplu tarama veri setleri ve yapay zekâ

Common Crawl gibi veri setlerine girmiş eski taramalardan veri çıkarmak pratikte mümkün değil. Yapay zekâ şirketlerinin bazıları (ör. OpenAI: https://privacy.openai.com) modellerin seninle ilgili ürettiği kişisel bilgiler için itiraz ve silme formları sunuyor; diğerlerine GDPR/KVKK dilekçesi gönderebilirsin.
