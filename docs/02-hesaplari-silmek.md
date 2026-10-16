# 2. Hesapları silmek

> Bu bölüme gelmeden önce [03 İçerik temizliği](03-icerik-temizligi.md)'ni yap. Bazı platformlarda hesap silinince içerik kalır ve artık silemezsin.

## Her hesap için aynı yöntem

1. **Giriş yap**, iki adımlı doğrulamanın çalıştığından emin ol.
2. **Parayı çek:** abonelikleri iptal et, bakiyeyi ve hediye kartlarını kullan, kayıtlı kartları sil.
3. **Profili boşalt:** ad, fotoğraf, biyografi, telefon, doğum tarihi. Silme bir şekilde başarısız olursa geride boş bir kabuk kalır.
4. **İçeriği temizle** ([03](03-icerik-temizligi.md)).
5. **Silme talebini başlat.** Onay e-postasını ve ekran görüntüsünü sakla.
6. Envanteri güncelle: `diedigital inventory set <id> requested`
7. **Bekleme süresi boyunca giriş yapma.** Uygulamayı kaldır, tarayıcı oturumunu kapat, çerezleri temizle. Çoğu platformda bir giriş silmeyi iptal eder.
8. Süre dolunca "şifremi unuttum" ile dene: "böyle bir hesap yok" cevabı silindiğini gösterir. Sonra: `diedigital inventory set <id> deleted`

Bir hizmetin bağlantısını ve püf noktalarını görmek için:

```bash
diedigital catalog linkedin
```

## Silme seçeneği yoksa

- **Uygulamaya bak.** Apple 2022'den beri, Google Play 2024'ten beri hesap açtıran uygulamaların uygulama içinden hesap silme sunmasını şart koşuyor. Web sitesinde bulamadığın seçenek çoğu zaman uygulamanın ayarlarındadır.
- **Destek formu veya e-posta.** "Hesabımı ve tüm verilerimi silin" demek yeterli.
- **KVKK / GDPR dilekçesi.** Cevap gelmezse ya da "silemiyoruz" denirse yasal yola geç ([06](06-hukuki-haklar.md)):

```bash
diedigital inventory set <id> --privacy-email kvkk@sirket.com.tr
diedigital letters send --account <id>            # önce oku
diedigital letters send --account <id> --execute  # sonra gönder
```

## Büyük platformlar

| Platform | Nereden | Bekleme | Dikkat |
|---|---|---|---|
| Google | https://myaccount.google.com/delete-services-or-account | kısa | En sona bırak; diğer hesapların kurtarma adresi büyük ihtimalle burası. Gmail ve YouTube tek tek silinebilir. |
| Facebook | Hesaplar Merkezi > Kişisel bilgiler > Hesap sahipliği ve kontrolü | 30 gün | Messenger mesajların karşı tarafta kalır. |
| Instagram | Hesaplar Merkezi > aynı yol | 30 gün | Facebook'tan bağımsız silinir. |
| Threads | Threads > Ayarlar > Hesap | 30 gün | Instagram'dan bağımsız silinebilir. |
| WhatsApp | Ayarlar > Hesap > Hesabımı sil | 90 güne kadar | Google Drive / iCloud'daki sohbet yedeğini ayrıca sil. |
| X (Twitter) | https://x.com/settings/deactivate | 30 gün | |
| LinkedIn | Ayarlar > Hesap tercihleri > Hesap yönetimi > Hesabı kapat | 14 gün | Premium'u önce iptal et. |
| TikTok | Ayarlar ve gizlilik > Hesap > Devre dışı bırak veya sil | 30 gün | |
| Snapchat | https://accounts.snapchat.com/accounts/delete_account | 30 gün | |
| Reddit | https://www.reddit.com/settings/account | yok | Yorumlar silinmez! Önce `diedigital wipe reddit`. |
| Discord | Ayarlar > Hesabım > Hesabı Sil | var | Mesajlar kalır. Sahibi olduğun sunucuları önce devret. |
| Telegram | https://my.telegram.org/auth?to=deactivate | yok | Anında ve geri dönüşsüz. |
| Microsoft | https://account.live.com/closeaccount.aspx | 30 / 60 gün | Outlook, Skype, Xbox, OneDrive birlikte gider. |
| Apple | https://privacy.apple.com | birkaç gün | Önce cihazlarda "Bul"u kapat, yoksa cihaz kilitli kalır. |
| Amazon | Hesap ve Giriş / Gizlilik > Hesabını kapat | var | Audible, Kindle kitapları da gider. Bölgesel mağazaları (amazon.com.tr, .de) ayrı kontrol et. |
| GitHub | https://github.com/settings/admin | yok | Önce `diedigital wipe github`. |

Tam liste: `diedigital catalog`. Bağlantılar zamanla değişir; çalışmayan bir bağlantıda notlardaki menü yolunu izle.

## Türkiye'deki hizmetler

E-ticaret (Trendyol, Hepsiburada, n11, Amazon.com.tr), yemek ve market (Yemeksepeti, Getir, Migros), ilan siteleri (sahibinden.com, Dolap, letgo), kargo uygulamaları, sadakat kartları:

1. Uygulamanın hesap ayarlarında "hesabı sil / üyeliği sonlandır" seçeneğini ara.
2. İlan sitelerinde önce **ilanlarını** kaldır: eski ilanlarda telefon numaran ve fotoğrafların durur.
3. Kayıtlı adresleri ve kartları sil.
4. Seçenek yoksa ya da verilerinin gerçekten silindiğinden emin olmak istiyorsan, sitenin **Aydınlatma Metni**'ndeki KVKK başvuru adresine dilekçe gönder. Adresi bulamazsan VERBİS'te şirketi ara ([06](06-hukuki-haklar.md)).

Fatura ve sipariş kayıtları vergi mevzuatı gereği bir süre saklanır. Bu normaldir; dilekçede saklanan verilerin ve sürenin sana bildirilmesini iste (şablon bunu zaten istiyor).

### Ticari ileti onayları: İYS

Türkiye'de markalara verdiğin SMS, arama ve e-posta izinlerinin hepsi **İleti Yönetim Sistemi**'nde (İYS) toplanır. iys.org.tr veya e-Devlet üzerinden tüm markalara verdiğin onayları tek yerden görüp reddedebilirsin. Hesapları silmeden önce yap: bazı şirketler hesap silinse bile pazarlama listesinde tutar.

### Bankalar, operatörler, devlet

- **Bankalar ve ödeme kuruluşları:** Müşteri olduğun sürece hesap silinmez. Kullanmadığın bankalardaki hesapları ve kartları kapat; kayıtlar yasal süre boyunca saklanır.
- **GSM operatörleri:** Hat kapanınca abonelik kayıtları da yasal süre boyunca saklanır. Kampanya ve pazarlama izinlerini kapat.
- **e-Devlet:** Silinemez, silinmesi de gerekmez. Ama e-Devlet şifreni değiştir ve iki adımlı doğrulamayı aç: sızıntı panellerinde dolaşan bilgilerin çoğunu korumanın yolu bu.

## Diğer tuzaklar

- **Flört uygulamaları:** Uygulamayı silmek hesabı silmez. Aboneliği App Store / Google Play'den iptal et, sonra uygulama içinden hesabı sil.
- **Oyun hesapları:** Steam, Epic, PlayStation, Xbox, Riot... Satın aldıkların gider; kullanıcı adın oyun içi sıralamalarda ve maç kayıtlarında kalabilir.
- **İş başvuru siteleri:** Kariyer.net, Yenibiris, LinkedIn, şirketlerin kendi kariyer portalları. Önce CV'ni sil, sonra üyeliği. Başvurduğun şirketlerin İK veritabanlarında da CV'n var; onlar için KVKK dilekçesi gönder.
- **Okul ve kurs platformları:** Mezun portalları, uzaktan eğitim sistemleri, sertifika sayfaları (sertifika doğrulama sayfaları adınla indekslenir).
- **Haber sitelerindeki yorumlar:** Çoğu Disqus ya da kendi üyelik sistemini kullanır; yorumları silip hesabı kapat.
