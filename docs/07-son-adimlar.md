# 7. Son adımlar: e-posta, telefon, alan adı, cihazlar

Bunlar en sona kalır, çünkü diğer her şey bunlara bağlı.

## Alan adı ve web sitesi

1. İçeriği kaldır (`noindex` → 410, bkz. [03](03-icerik-temizligi.md)), arama motorlarından güncelleme iste.
2. WHOIS kayıtlarında kişisel bilgin görünüyorsa kayıt firmasının gizlilik hizmetini aç. Eski WHOIS kayıtları geçmiş veritabanlarında kalır; bunlar silinmez.
3. **Alan adını bırakmadan önce düşün.** Süresi dolan alan adları hemen başkaları tarafından satın alınır. Yeni sahibi:
   - Adına ve eski içeriğine benzer bir site kurabilir,
   - **O alan adındaki e-posta adreslerine gelen postaları alabilir.** O adresle açılmış ve kapanmamış tek bir hesap bile kalırsa, "şifremi unuttum" ile o hesabı ele geçirebilir.

   Ya alan adını birkaç yıl daha (MX kaydı olmadan, boş) elinde tut, ya da o alan adındaki adreslerle hiçbir hesabın kalmadığından kesinlikle emin ol.
4. Barındırma (hosting) hesabını, yedekleriyle birlikte kapat.

## E-posta adresleri

- **En son kapat.** Önce tutacağın hizmetlerdeki (banka, devlet, sağlık, iş) iletişim adresini yeni ve özel bir adrese taşı.
- Bültenlerden çık ve İYS'den ticari ileti onaylarını reddet. Silmeden önce yapmak, adresinin satılan listelerde dolaşmasını azaltır.
- Bazı sağlayıcılar uzun süre kullanılmayan adresleri geçmişte başkalarına yeniden dağıttı. Kapattığın adrese bağlı tek bir hesap kalmamalı (alan adı riskinin aynısı).
- **Gmail:** Sadece Gmail'i silmek ile tüm Google hesabını silmek farklı. Gmail adresleri başkasına verilmez; yine de bağlı hesap bırakma.
- Kapatmadan önce son bir kez: [01](01-envanter-ve-yedek.md)'deki IMAP taramasını çalıştır, `inventory overdue` ile cevap bekleyen dilekçe kalmadığını kontrol et.

## Telefon numarası

Telefon numaran e-postadan daha kalıcı bir kimliktir: WhatsApp, Telegram, bankalar, kargo, iki adımlı doğrulama hep ona bağlı.

- SMS ile iki adımlı doğrulamayı, doğrulayıcı uygulamaya (TOTP) veya güvenlik anahtarına çevir.
- Numaranı değiştireceksen eskisini kapatmadan önce tüm hesaplarda güncelle. Kapatılan numaralar bir süre sonra başkasına verilebilir; eski numarana bağlı hesap kurtarma kalmamalı.
- Rehber uygulamaları için [05](05-veri-simsarlari-ve-rehberler.md).

## Bulut depolama

Google Drive / Fotoğraflar, iCloud, OneDrive, Dropbox, Mega: içeriği sil, **çöp kutusunu boşalt**, sonra hesabı kapat. Paylaştığın klasörlerin başkalarındaki kopyaları silinmez.

Ölü adam anahtarında `command` eylemiyle bulut depolamayı otomatik temizleyebilirsin (ör. `rclone purge`), bkz. [08](08-olu-adam-anahtari.md).

## Cihazlar

- Telefon, tablet, bilgisayar: "Bul" özelliğini kapat ve cihazı hesaplardan çıkar (Apple Etkinleştirme Kilidi, Google FRP).
- Disk şifrelemesi açıkken fabrika ayarlarına dön. Şifreli bir diskin anahtarı silinince veri okunamaz hâle gelir; SSD'lerde tek tek dosya silmekten çok daha güvenilirdir.
- Akıllı saat, akıllı TV, oyun konsolu, araç multimedya sistemi: hepsinde oturum açık hesap olabilir.

## Para ve kripto

- PayPal, Papara, ininal, iyzico, banka uygulamaları: bakiyeyi çek, kapat. Kayıtlar yasal süre boyunca saklanır.
- Kripto borsaları: önce varlıkları çek. Kimlik doğrulama (KYC) belgeleri yasal süre boyunca tutulur; saklama süresinin sonunda silinmesini yazılı iste.

## Parola yöneticisi

Herkesten sonra kapanır. Kapatmadan önce envanterin son hâlini al (`inventory report`) ve şifreli yedeğinle birlikte çevrimdışı sakla ya da tamamen sil. Neyi saklayacağına sen karar ver: geri dönmek isteyebileceğin bir gün için bir harita mı, yoksa hiçbir şey mi.
