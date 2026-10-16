# 1. Envanter ve yedek

Bilmediğin hesabı silemezsin. İlk iş, nerede hesabın olduğunu çıkarmak.

## 1.1 Hesaplarını bul

Aşağıdaki kaynakların hepsini tara. Her biri diğerlerinin kaçırdığı hesapları bulur.

### Parola yöneticisi ve tarayıcı

Kayıtlı şifreler en iyi listedir. Dışa aktar:

- **Chrome:** Ayarlar > Otomatik doldurma ve şifreler > Google Şifre Yöneticisi > Ayarlar > Şifreleri dışa aktar
- **Firefox:** `about:logins` > ⋯ > Girişleri dışa aktar
- **Safari / iCloud Anahtar Zinciri:** macOS'ta Şifreler uygulaması > Dosya > Tüm şifreleri dışa aktar
- **Bitwarden:** Araçlar > Kasayı dışa aktar > `.csv`
- **1Password, KeePass:** Dosya > Dışa aktar > CSV

Sonra envantere aktar:

```bash
diedigital inventory import sifreler.csv
```

Araç parolaları **okumaz ve kaydetmez**; sadece site adresini ve kullanıcı adını alır. İş bitince CSV'yi güvenle sil (Linux: `shred -u sifreler.csv`).

### E-posta kutusu

Her hesap açılışında bir "hoş geldin" ya da "e-postanı doğrula" mesajı gelir. Araç bunları başlıklara bakarak bulur (mesaj içerikleri indirilmez, posta kutusu salt okunur açılır):

```bash
export IMAP_PASSWORD='uygulama-sifresi'
diedigital discover imap --host imap.gmail.com --user sen@gmail.com --add
```

- **Gmail:** IMAP için iki adımlı doğrulama açık olmalı; Google Hesabı > Güvenlik > Uygulama şifreleri ile ayrı bir şifre oluştur. Araç "Tüm Postalar" klasörünü kendisi bulur.
- **Yandex:** `imap.yandex.com`; Ayarlar > E-posta programları bölümünden IMAP'i aç.
- **Outlook / Hotmail:** Microsoft kişisel hesaplarda parola ile IMAP girişini büyük ölçüde kapattı. Çalışmazsa arama kutusunda elle ara.

Elle arama için Gmail sorgusu:

```
subject:(welcome OR verify OR "confirm your" OR "hoş geldiniz" OR doğrula OR üyeliğiniz OR "hesabınız")
```

Kullandığın **her** e-posta adresi için tekrarla: eski Hotmail'in, okul ve iş adreslerin dahil.

### "Google ile giriş yap" hesapları

Şifresiz açtığın hesaplar parola yöneticisinde görünmez:

- **Google:** https://myaccount.google.com/connections
- **Apple:** Ayarlar > [Adın] > Apple ile Giriş
- **Facebook:** Ayarlar > Uygulamalar ve web siteleri
- **GitHub, Microsoft, X:** Ayarlar > Bağlı uygulamalar / Uygulamalar

Her bağlantıyı listeye ekle, sonra bağlantıyı kaldır.

### Veri sızıntıları

https://haveibeenpwned.com adresinde e-postanı ara. Her sızıntı, orada bir hesabın olduğu anlamına gelir; çoğunu çoktan unutmuşsundur. API anahtarın varsa:

```bash
export HIBP_API_KEY=...
diedigital footprint email sen@ornek.com --add
```

### Kullanıcı adların

```bash
diedigital footprint username eski_takma_adim
```

Hangi sitelerde aynı kullanıcı adıyla profil olduğunu kontrol eder. Bazı siteler (Instagram, Facebook, X, TikTok) otomatik kontrole izin vermez; bunlar "elle bak" diye listelenir.

### Ödemeler ve telefon

- App Store ve Google Play abonelik listeleri
- Kredi kartı ekstrelerindeki tekrarlayan ödemeler
- Telefondaki yüklü uygulamalar
- SMS'lerde doğrulama kodu gönderen gönderici adları

### Hafızan

Listeyi bir de şunlar için düşünerek tamamla: forumlar, okul ve kurs platformları, iş başvuru siteleri (CV yüklediğin her yer), oyun hesapları, flört uygulamaları, eski bloglar, yorum yaptığın haber siteleri, şikâyet siteleri.

## 1.2 Envanteri yönet

```bash
diedigital inventory add "Eski Forum" --url https://forum.ornek.com --username ben
diedigital inventory list
diedigital inventory set 12 requested --note "silme formu gönderildi"
diedigital inventory report --out envanter.md
```

Durumlar: `active` → `exported` (yedek alındı) → `wiped` (içerik temizlendi) → `requested` (silme talep edildi) → `deleted`. Silinemeyenler için `blocked`.

`report` her hesabın yanına, bilinen hizmetlerde silme ve yedek bağlantılarını, bekleme süresini ve dikkat edilecekleri ekler. Katalogda ne olduğunu görmek için: `diedigital catalog` veya `diedigital catalog instagram`.

Envanter (`accounts.json`) hassas bir dosyadır: hangi hizmeti hangi kullanıcı adıyla kullandığını gösterir. `.gitignore`'dadır; herkese açık bir yere koyma.

## 1.3 Yedek al

Yedekleri **hemen** talep et; bazıları günler içinde hazırlanır.

| Hizmet | Yedek |
|---|---|
| Google (Gmail, Fotoğraflar, Drive, YouTube) | https://takeout.google.com |
| Facebook | https://www.facebook.com/dyi |
| Instagram, Threads | Hesaplar Merkezi > Bilgilerin ve izinlerin > Bilgilerini indir |
| X (Twitter) | https://x.com/settings/download_your_data |
| LinkedIn | Ayarlar > Veri gizliliği > Verilerinin bir kopyasını al |
| WhatsApp | Sohbeti dışa aktar (her sohbet ayrı) ve Ayarlar > Hesap > Hesap bilgilerini iste |
| Telegram | Telegram Desktop > Ayarlar > Gelişmiş > Telegram verilerini dışa aktar |
| Apple | https://privacy.apple.com |
| Microsoft | https://account.microsoft.com/privacy |
| Reddit | https://www.reddit.com/settings/data-request (içerik temizliği için de gerekli) |
| Discord | Ayarlar > Veri ve Gizlilik > Tüm verilerimi talep et |
| Spotify | https://www.spotify.com/account/privacy/ |

Yedekleri nasıl saklamalı:

- **Şifreli:** VeraCrypt kapsayıcısı ya da `7z a -p -mhe=on yedek.7z klasor/`
- **Çevrimdışı:** Bulutta değil, iki ayrı harici diskte.
- Yedeğin kendisi senin hakkındaki en eksiksiz veri kümesidir. Kaybolmak istiyorsan, en iyi korunması gereken şey de odur.
