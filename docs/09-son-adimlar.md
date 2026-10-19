# 9. Son adımlar: e-posta, telefon, alan adı, cihazlar, para

Bunlar en sona kalır, çünkü diğer her şey bunlara bağlı.

## Alan adı ve web sitesi

1. İçeriği kaldır (`noindex` → 410, bkz. [2. bölüm](02-icerik-temizligi.md)), arama motorlarından güncelleme iste.
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
- Kapatmadan önce son bir kez: [1. bölüm](01-envanter-ve-yedek.md)'deki e-posta aramalarını tekrarla (yeni hesap çıkmadığından emin ol) ve cevap bekleyen dilekçe kalmadığını kontrol et. Cevaplar bu adrese gelecekse, adresi kapatmadan önce dilekçelerdeki iletişim adresini yenisiyle güncelle.
- Otomatik yönlendirmeyi kapat; kapatılan adrese gelen postaların yeni adresine akması iki kimliği birbirine bağlar.

## Telefon numarası

Telefon numaran e-postadan daha kalıcı bir kimliktir: WhatsApp, Telegram, bankalar, kargo, iki adımlı doğrulama hep ona bağlı.

- SMS ile iki adımlı doğrulamayı, doğrulayıcı uygulamaya (TOTP) veya güvenlik anahtarına çevir.
- Numaranı değiştireceksen eskisini kapatmadan önce tüm hesaplarda güncelle. Kapatılan numaralar bir süre sonra başkasına verilebilir; eski numarana bağlı hesap kurtarma kalmamalı.
- Rehber uygulamaları için [5. bölüm](05-veri-simsarlari-ve-rehberler.md).
- Seviye 3'te (tam kopuş) yeni numarayı eski çevrene toplu duyurma; sadece kalmasını istediğin kişilere birebir ver. Yeni numaranı rehbere kaydeden herkes, rehber uygulamaları üzerinden onu eski adınla eşleştirebilir.

## Bulut depolama

Google Drive / Fotoğraflar, iCloud, OneDrive, Dropbox, Mega: içeriği sil, **çöp kutusunu boşalt**, sonra hesabı kapat. Paylaştığın klasörlerin başkalarındaki kopyaları silinmez.

Bulut depolamayı belirli bir tarihte otomatik temizletmek istiyorsan: [10. bölüm](10-olu-adam-anahtari.md).

## Cihazlar

- Telefon, tablet, bilgisayar: "Bul" özelliğini kapat ve cihazı hesaplardan çıkar (Apple Etkinleştirme Kilidi, Google FRP).
- Disk şifrelemesi açıkken fabrika ayarlarına dön. Şifreli bir diskin anahtarı silinince veri okunamaz hâle gelir; SSD'lerde tek tek dosya silmekten çok daha güvenilirdir.
- Akıllı saat, akıllı TV, oyun konsolu, araç multimedya sistemi: hepsinde oturum açık hesap olabilir.
- Satacağın ya da atacağın eski telefonlar, diskler, USB bellekler: aynı şekilde şifreleyip sıfırla; çalışmayan diskleri fiziksel olarak imha et.

## Para ve kripto

- PayPal, Papara, ininal, iyzico, banka uygulamaları: bakiyeyi çek, kapat. Kayıtlar yasal süre boyunca saklanır.
- Kripto borsaları: önce varlıkları çek. Kimlik doğrulama (KYC) belgeleri yasal süre boyunca tutulur; saklama süresinin sonunda silinmesini yazılı iste.

## Parola yöneticisi

Herkesten sonra kapanır. Kapatmadan önce envanter tablonun son hâlini al ve şifreli yedeğinle birlikte çevrimdışı sakla ya da tamamen sil. Neyi saklayacağına sen karar ver: geri dönmek isteyebileceğin bir gün için bir harita mı, yoksa hiçbir şey mi.

## Bölüm sonu kontrolü

- [ ] Alan adı için karar verildi (elde tutma veya bağlı hiçbir hesap kalmadığından emin olarak bırakma)
- [ ] Tutulan hizmetlerin iletişim adresi ve numarası yenilerine taşındı
- [ ] SMS ile iki adımlı doğrulama, doğrulayıcı uygulamaya çevrildi
- [ ] Eski e-posta adresleri ve numaralar, bağlı hesap kalmadığı doğrulanarak kapatıldı
- [ ] Bulut depolama boşaltıldı, çöp kutuları temizlendi
- [ ] Cihazlar hesaplardan çıkarıldı ve şifreli olarak sıfırlandı
- [ ] Parola yöneticisi için son karar verildi
