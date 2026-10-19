# 1. Envanter ve yedek

Bilmediğin hesabı silemezsin. Çoğu insanın, hatırladığından çok daha fazla çevrimiçi hesabı vardır. Bu bölümün sonunda elinde üç şey olacak: tam bir hesap listesi, verilerinin yedeği ve yeni iz üretmeyi durdurmuş bir sen.

## 1.1 Önce iz üretmeyi durdur

Silmeye başlamadan önce, bugünden itibaren:

- Yeni paylaşım yapma, yorum yazma, fotoğraf yükleme.
- Yeni hesap açma. Mecbur kalırsan takma ad bir e-posta kullan ([11. bölüm](11-gorunmez-yasamak.md)).
- Telefonda konum servislerini, konum geçmişini ve fotoğraflara konum eklemeyi kapat.
- Uygulamaların rehberine erişimini kapat (Ayarlar > Gizlilik > Kişiler).
- "Google / Facebook / Apple ile giriş yap" düğmelerini kullanmayı bırak.

## 1.2 Envanter tablosu

Bir tablo aç: çevrimdışı bir elektronik tablo ya da kâğıt. Bulut tabanlı bir belgeye koyma; bu liste senin hakkındaki en hassas belgelerden biri olacak.

| Hizmet | Adres | Kullanıcı adı / e-posta | Bağlı telefon | Ödeme bilgisi | Yedek | İçerik silindi | Silme talebi | Bekleme bitişi | Silindi | Not |
|---|---|---|---|---|---|---|---|---|---|---|
| Örnek Forum | forum.ornek.com | eski_takma_ad | yok | yok | – | ✓ 12.03 | 12.03 | – | ✓ 15.03 | |

Her hesap şu aşamalardan geçer: **bulundu → yedeklendi → içerik temizlendi → silme istendi → bekleme süresi bitti → silindi doğrulandı.** Silinemeyenleri "silinemiyor" diye işaretle ve nedenini yaz (yasal saklama, cevapsız şirket, erişim kaybı).

> **Araçla:** `diedigital inventory` aynı tabloyu tutar, bilinen hizmetler için silme bağlantılarını ekler ve işaretlenebilir bir rapor üretir ([Ek C](ek-c-araclar.md)).

## 1.3 Hesaplarını bul

Aşağıdaki kaynakların hepsini tara. Her biri, diğerlerinin kaçırdığı hesapları bulur.

### Bütün e-posta adreslerin ve telefon numaraların

Önce kimliklerinin listesini çıkar; hesaplar bunlara bağlı:

- Şu an kullandığın ve geçmişte kullandığın **tüm** e-posta adresleri: eski Hotmail/Yahoo/Yandex adresleri, okul ve iş adresleri, kendi alan adındaki adresler.
- Şu anki ve eski **telefon numaraların**.
- Kullandığın **kullanıcı adları ve takma adlar**.

Eski bir e-postaya erişimin yoksa şimdi kurtarmayı dene. O adresle açılmış hesapları silmek için ona ihtiyacın olacak.

### Parola yöneticisi ve tarayıcı

Kayıtlı şifreler en iyi listedir. Listeye bakarak tabloya geçir ya da dışa aktar:

- **Chrome:** Ayarlar > Otomatik doldurma ve şifreler > Google Şifre Yöneticisi
- **Firefox:** adres çubuğuna `about:logins`
- **Safari / iCloud Anahtar Zinciri:** macOS ve iOS'ta Şifreler uygulaması
- **Bitwarden, 1Password, KeePass:** Kasadaki tüm kayıtlar

Dışa aktardığın bir dosya varsa iş bitince güvenle sil; içinde tüm şifrelerin vardır.

> **Araçla:** `diedigital inventory import sifreler.csv` şifreleri okumadan sadece site ve kullanıcı adlarını alır.

### E-posta kutun

Her hesap açılışında bir "hoş geldin" ya da "e-postanı doğrula" mesajı gelir. Her e-posta adresinde şu aramaları yap:

**Gmail** (arama kutusuna yapıştır):

```
subject:(welcome OR verify OR "confirm your" OR "your account" OR "hoş geldiniz" OR doğrula OR doğrulama OR üyeliğiniz OR "hesabınız" OR "şifre sıfırlama")
```

**Outlook / Hotmail:** arama kutusunda tek tek: `hoş geldiniz`, `welcome`, `doğrulama`, `verify`, `hesabınız`

Ayrıca:

- `unsubscribe` veya `abonelikten çık` geçen e-postalar: sana bülten gönderen her marka, büyük ihtimalle bir hesabın olan yerdir.
- `fatura`, `sipariş`, `receipt`, `order`: alışveriş yaptığın siteler.
- `giriş yapıldı`, `new sign-in`, `login`: aktif kullandığın hesaplar.

Sonuçları gönderen alan adına göre gruplayıp tabloya ekle.

> **Araçla:** `diedigital discover imap` posta kutusunu salt okunur açar, sadece başlıklara bakar ve olası hesapları puanlayarak listeler.

### "Google / Apple / Facebook ile giriş" hesapları

Şifresiz açtığın hesaplar parola yöneticisinde görünmez:

- **Google:** https://myaccount.google.com/connections
- **Apple:** Ayarlar > [Adın] > Apple ile Giriş
- **Facebook:** Ayarlar > Uygulamalar ve web siteleri
- **Microsoft, GitHub, X, LinkedIn:** Ayarlar > Bağlı uygulamalar / İzin verilen uygulamalar

Her birini tabloya ekle. Bağlantıyı kaldırmak hesabı silmez; sadece giriş yolunu keser. Önce hesabı sil, sonra bağlantıyı kaldır.

### Veri sızıntıları

https://haveibeenpwned.com adresinde her e-posta adresini ve telefon numaranı ara. Her sızıntı, orada bir hesabın olduğu anlamına gelir; çoğunu çoktan unutmuşsundur. Mozilla Monitor (https://monitor.mozilla.org) da benzer bir tarama yapar.

### "Şifremi unuttum" testi

Hesabın olup olmadığından emin olmadığın bir sitede e-postanla "şifremi unuttum" iste. "Bu e-posta kayıtlı değil" demiyorsa ve sıfırlama e-postası geliyorsa hesabın vardır. Bazı siteler bilgiyi gizlemek için her durumda aynı mesajı gösterir; o zaman gelen kutunu kontrol et.

### Kullanıcı adların

Her kullanıcı adını tırnak içinde arama motorunda ara: `"eski_takma_adim"`. Sonra büyük sitelerde doğrudan dene: `instagram.com/eski_takma_adim`, `x.com/...`, `tiktok.com/@...`, `github.com/...`, `reddit.com/user/...`, `youtube.com/@...`, `pinterest.com/...`, `twitch.tv/...`, `medium.com/@...`, `t.me/...`

> **Araçla:** `diedigital footprint username eski_takma_adim` 30'dan fazla siteyi birlikte kontrol eder.

### Telefonun, eski telefonların ve uygulama mağazaları

- Telefondaki yüklü uygulamalar.
- **App Store:** Hesap > Satın Alınanlar. Yıllar önce yükleyip sildiğin uygulamalar da burada.
- **Google Play:** Profil > Uygulamaları ve cihazı yönet > Yönet > "Bu cihazda yüklü değil".
- SMS'lerde doğrulama kodu gönderen gönderici adları.

### Ödemeler

- Kredi kartı ve banka ekstrelerindeki tekrarlayan ödemeler.
- App Store ve Google Play abonelikleri.
- PayPal ve benzeri hizmetlerde "otomatik ödemeler" listesi.

### Tarayıcı geçmişi ve yer imleri

Uzun süredir aynı tarayıcıyı kullanıyorsan geçmişte sık girdiğin siteler ve yer imleri unuttuğun hesapları hatırlatır.

### Hafıza listesi

Kategori kategori kendine sor:

- **Sosyal ve içerik:** sosyal ağlar, bloglar, video, müzik, fotoğraf siteleri, forumlar, sözlükler, soru-cevap siteleri
- **Mesajlaşma:** WhatsApp, Telegram, Signal, Discord, Skype, eski MSN/ICQ hesapları
- **Alışveriş:** e-ticaret siteleri, ikinci el ve ilan siteleri, markaların kendi mağazaları
- **Yemek, market, ulaşım:** yemek siparişi, market, taksi, scooter, araç kiralama, toplu taşıma kartları
- **Seyahat:** havayolu mil programları, otel ve rezervasyon siteleri
- **Finans:** bankalar, ödeme uygulamaları, kripto borsaları, yatırım uygulamaları, sigorta
- **Sağlık ve spor:** randevu uygulamaları, spor salonu, fitness ve koşu uygulamaları, adet takibi, beslenme
- **Eğitim ve iş:** okul platformları, çevrimiçi kurslar, sertifika siteleri, iş ilanı siteleri, serbest çalışma platformları
- **Oyun:** Steam, Epic, PlayStation, Xbox, Riot, mobil oyunlar
- **Flört uygulamaları**
- **Etkinlik ve bilet:** bilet satış siteleri, kulüpler, dernekler
- **İmza kampanyaları ve bağış siteleri:** imzaladığın kampanyalarda adın herkese açık görünebilir
- **Belediye ve kurum uygulamaları, sadakat kartları, kargo uygulamaları**
- **Yapay zekâ sohbet asistanları:** sohbet geçmişleri de kişisel veridir

## 1.4 Yedek al

Yedekleri **hemen** talep et; bazıları günler içinde hazırlanır.

| Hizmet | Yedek |
|---|---|
| Google (Gmail, Fotoğraflar, Drive, YouTube) | https://takeout.google.com |
| Facebook | https://www.facebook.com/dyi |
| Instagram, Threads | Hesaplar Merkezi > Bilgilerin ve izinlerin > Bilgilerini indir |
| X (Twitter) | https://x.com/settings/download_your_data |
| LinkedIn | Ayarlar > Veri gizliliği > Verilerinin bir kopyasını al |
| WhatsApp | Her sohbeti ayrı dışa aktar; Ayarlar > Hesap > Hesap bilgilerini iste |
| Telegram | Telegram Desktop > Ayarlar > Gelişmiş > Telegram verilerini dışa aktar |
| Apple | https://privacy.apple.com |
| Microsoft | https://account.microsoft.com/privacy |
| Reddit | https://www.reddit.com/settings/data-request |
| Discord | Ayarlar > Veri ve Gizlilik > Tüm verilerimi talep et |
| Spotify | https://www.spotify.com/account/privacy/ |
| Diğerleri | Ayarlarda "verilerini indir", "data export", "download your data" ara; yoksa KVKK md. 11 / GDPR md. 15 ile iste ([Ek B](ek-b-dilekce-ornekleri.md)) |

Ne saklamak istediğine karar ver. Her şeyi saklamak zorunda değilsin: kaybolmak istiyorsan bazı anıları bırakmak da sürecin parçası olabilir.

Yedekleri nasıl saklamalı:

- **Şifreli:** VeraCrypt kapsayıcısı ya da güçlü parolalı, dosya adları da şifrelenmiş bir arşiv (`7z a -p -mhe=on yedek.7z klasor/`).
- **Çevrimdışı:** Bulutta değil, iki ayrı harici diskte, iki ayrı yerde.
- Yedek, senin hakkındaki en eksiksiz veri kümesidir. Kaybolmak istiyorsan en iyi korunması gereken şey de odur.

## Bölüm sonu kontrolü

- [ ] Yeni iz üretmeyi durdurdum
- [ ] Tüm e-posta adreslerimin, numaralarımın ve kullanıcı adlarımın listesi hazır
- [ ] Envanter tablosu en az bu bölümdeki tüm kaynaklarla dolduruldu
- [ ] Yedekler talep edildi, indirildi ve şifreli olarak saklandı
