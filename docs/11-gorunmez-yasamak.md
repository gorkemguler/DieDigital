# 11. Görünmez yaşamak

Silmek geçmişi temizler. Görünmez kalmak ise geleceği korur. Bu bölümü erken oku: kaybolma sürecinde açman gereken her yeni hesap ve aldığın her yeni numara bu kurallarla açılmalı.

## 11.1 Kimliğini bölümlere ayır

Tek bir e-posta, tek bir numara, tek bir kullanıcı adı her şeyi birbirine bağlar. Bunun yerine üç ayrı katman kullan:

| Katman | Nerede | Kimlik |
|---|---|---|
| **Resmî** | Banka, devlet, işveren, sağlık, sigorta, kira | Gerçek adın, ayrı bir e-posta, ana numaran. Başka hiçbir yerde kullanılmaz. |
| **Gündelik** | Alışveriş, ulaşım, abonelikler, uygulamalar | Her hizmete ayrı takma ad e-posta; gerekmedikçe gerçek ad ve telefon yok. |
| **Anonim** | Forumlar, yorumlar, topluluklar | Takma ad, ayrı e-posta, gerçek kimliğinle hiçbir ortak bilgi (fotoğraf, yazım tarzı, saat dilimi, kullanıcı adı) yok. |

Katmanlar arasında hiçbir şeyi paylaşma: aynı kullanıcı adı, aynı profil fotoğrafı, aynı kurtarma e-postası, aynı telefon numarası, aynı parola.

## 11.2 E-posta

- **Resmî katman için** gizliliğe odaklanan bir sağlayıcı düşünebilirsin (Proton Mail, Tuta gibi). Kendi alan adını kullanırsan alan adını uzun süre elinde tutmayı göze al ([9. bölüm](09-son-adimlar.md)).
- **Gündelik katman için takma ad (alias) hizmetleri:** SimpleLogin, addy.io, Firefox Relay, DuckDuckGo Email Protection, Apple "E-postamı Gizle". Her hizmete ayrı bir adres verirsin; postalar ana kutuna yönlenir. Bir adres sızarsa ya da spam alırsa sadece onu kapatırsın; hesaplar birbirine bağlanamaz.
- E-postalardaki izleme piksellerini engelle: e-posta uygulamanın "uzak görselleri yükleme" ayarını kapat.

## 11.3 Telefon numarası

- Türkiye'de hatlar kimlikle kaydedilir; anonim bir hat mümkün değil. Bu yüzden numara vermemek, numarayı gizlemekten daha önemlidir.
- Numaranı sadece resmî katmanda ver. Diğer hizmetler isterse, mümkünse telefonsuz kayıt yolunu seç.
- İki adımlı doğrulamada SMS yerine doğrulayıcı uygulama veya güvenlik anahtarı kullan.
- Mesajlaşma uygulamalarında numarayı gizle (Signal kullanıcı adı, Telegram gizlilik ayarları; [5. bölüm](05-veri-simsarlari-ve-rehberler.md)).

## 11.4 Telefon ve bilgisayar ayarları

- **Konum:** Sadece gereken uygulamalara, sadece "kullanırken"; hassas konum kapalı; konum geçmişi kapalı ([7. bölüm](07-gercek-dunya-izleri.md)).
- **Rehber, fotoğraflar, mikrofon, kamera izinleri:** Uygulama başına gözden geçir. Fotoğraflar için "sadece seçilenler" seçeneğini kullan.
- **Reklam kimliği:** iOS'ta izleme izinlerini kapat, Android'de reklam kimliğini sil.
- **Wi-Fi ve Bluetooth taraması:** Konum doğruluğu için arka planda tarama yapan ayarları kapat.
- **Kilit ekranı:** Bildirim önizlemelerini kapat.
- **Klavye ve yapay zekâ özellikleri:** Yazdığını buluta gönderen klavye ve asistan özelliklerini gözden geçir.
- **Güncellemeler:** İşletim sistemini ve uygulamaları güncel tut; eski cihazlar veri sızıntısına açıktır.

## 11.5 Tarayıcı ve arama

- **Tarayıcı:** Firefox (uBlock Origin eklentisiyle), Brave ya da Mullvad Browser gibi izlemeyi varsayılan olarak engelleyen tarayıcılar.
- **Ayarlar:** Üçüncü taraf çerezleri engelle; tarayıcı kapanınca çerezleri sil; şifreleri ve formları tarayıcıya kaydetme (parola yöneticisi kullan).
- **Ayrı profiller:** Resmî, gündelik ve anonim katmanlar için ayrı tarayıcı profilleri ya da Firefox kapsayıcıları. Asla aynı profilde iki katmanın hesabıyla oturum açma.
- **Arama motoru:** DuckDuckGo, Startpage, Brave Search gibi arama geçmişini profillemeyen bir arama motoru.
- **"Google ile giriş" düğmelerini kullanma.** Her hizmete ayrı e-posta ve parola.

## 11.6 Ağ: VPN ve Tor

| | Neyi gizler | Neyi gizlemez |
|---|---|---|
| **VPN** | IP adresini sitelerden; trafiğini internet sağlayıcından | VPN sağlayıcısı trafiğini görür. Oturum açtığın hesaplar seni yine tanır. |
| **Tor Browser** | IP adresini; kimin hangi siteye girdiğini zincirdeki her noktadan | Yavaştır; bazı siteler engeller. Kendi adınla oturum açarsan anlamı kalmaz. |

- VPN seçeceksen ücretli, bağımsız denetimden geçmiş ve kayıt tutmadığını kanıtlamış bir sağlayıcı seç. Ücretsiz VPN'ler çoğu zaman verini satarak para kazanır.
- Bazı ülkelerde, Türkiye dahil, VPN ve Tor sitelerine erişim zaman zaman engellenebiliyor; Tor için "köprü" (bridge) seçenekleri bunun için var. Kullanmadan önce yaşadığın yerin kurallarını bil.
- Şifreli DNS kullan: tarayıcıda "güvenli DNS", Android'de "Özel DNS".
- Ev dışındaki açık Wi-Fi ağlarında VPN kullan.

## 11.7 Mesajlaşma

- **Signal:** Uçtan uca şifreli; kaybolan mesajlar; numara yerine kullanıcı adı.
- **WhatsApp:** Uçtan uca şifreli, ama kiminle, ne zaman konuştuğun (meta veri) şirkette kalır. Yedekleri şifrele (Ayarlar > Sohbetler > Sohbet yedeği > Uçtan uca şifreli yedekleme).
- **Telegram:** Normal sohbetler uçtan uca şifreli değildir; hassas konuşmalar için "gizli sohbet" kullan.
- Kaybolan mesajları varsayılan yap; eski sohbetleri düzenli temizle.

## 11.8 Ödemeler ve alışveriş

- **Sanal kart:** Bankaların çoğu, ayrı limitli ve kolayca iptal edilebilen sanal kartlar veriyor. Çevrimiçi alışverişte ana kartını kullanma.
- **Nakit:** Gerçek dünyada en az iz bırakan ödeme yolu.
- **Kripto para anonim değildir;** borsalar kimlik doğrulama ister ve işlemler kalıcı olarak herkese açıktır.
- **Teslimat:** Ev adresi yerine kargo şubesinden teslim, teslimat noktaları veya akıllı dolaplar.
- **Sadakat kartları ve kampanyalar:** Telefon numaranla çalışan her indirim, alışveriş geçmişini kimliğine bağlar. Gerçekten gerekli mi diye sor.

## 11.9 Paylaşım kuralları

Hâlâ bir şeyler paylaşacaksan:

- Yüzün, evin, işyerin, çocukların, araban, rutinlerin yok.
- Konumu anlık değil, sonradan ve belirsiz paylaş ("geçen ay bir sahilde").
- Fotoğrafın arka planına bak: pencere manzarası, kapı numarası, belgeler, yansımalar ([7. bölüm](07-gercek-dunya-izleri.md)).
- Fotoğraflardan konum bilgisini sil.
- Takma ad hesaplarında gerçek hayattan ayrıntı verme: meslek, şehir, okul, doğum günü, evcil hayvan adı.
- Yazım tarzın da bir parmak izidir; takma ad hesabında kendini tanıtan ifadeleri ve uzun, kişisel metinleri yazma.

## 11.10 Çevren

- Yakınlarına kurallarını bir kez, açıkça söyle: etiketleme yok, sormadan fotoğraf yok, konum yok, numaramı/adresimi kimseye verme.
- Yeni tanıştığın insanlara sosyal medya hesabı yerine telefon numarası ya da Signal kullanıcı adı ver; sosyal medyada "bulunamamak" için açıklama yapmak zorunda değilsin.
- İşyerinde: Şirketin web sitesinde, sosyal medyasında ve basın bültenlerinde yer almak istemediğini baştan söyle.

## 11.11 Yeni bir hesap açmadan önce

1. Gerçekten gerekli mi? Misafir olarak devam edilebilir mi?
2. Hangi katmana ait? O katmanın e-postasını ve tarayıcı profilini kullan.
3. Gerçek ad, telefon, doğum tarihi, adres zorunlu mu? Değilse verme.
4. Silmek ne kadar zor? ([3. bölüm](03-hesaplari-silmek.md)'deki yöntemle önceden bak.)
5. Envanter tablona ekle.

## 11.12 Seviye 3: Tam kopuş

Eski kimliğinle yeni hayatın arasında hiçbir dijital bağ kalmasın istiyorsan:

- **Yeni e-posta ve yeni numara,** eski çevrene toplu duyurmadan; sadece kalmasını istediğin kişilere birebir ver.
- **Yeni cihazlar:** Eski telefonunun yedeğini yeni telefona geri yükleme; eski hesaplarla eşleşmiş uygulamaları ve rehberi taşıma. Gerekli kişileri elle ekle.
- **Taşınma:** Yeni adresini sadece zorunlu yerlere ver; kargo için teslimat noktası kullan; posta yönlendirme hizmeti kullanacaksan eski adresle yeni adres arasında kalıcı bağ oluşturduğunu bil.
- **Eski çevreyle ortak hiçbir hesap:** Aile planları, ortak albümler, eski gruplar.
- **Rutin değişikliği:** Aynı spor salonu, aynı kafe, aynı koşu rotası; dijitalde silinen izler fiziksel rutinden yeniden kurulabilir.
- **İsim değişikliği:** En uç seçenek. Türk Medeni Kanunu md. 27'ye göre ad değişikliği haklı sebeplerle hâkimden istenebilir. Eski adın nüfus kayıtlarında kalır ama internette eski adla yapılan aramalar artık seni bulmaz. Güncel usulü bir avukata veya nüfus müdürlüğüne sor.
- **Yasal yükümlülükler:** Vergi, mahkeme, borç, resmî tebligatlar için yeni iletişim bilgilerini ilgili kurumlara bildirmek zorundasın. Kaybolmak bu yükümlülükleri kaldırmaz; bildirilmeyen adres, aleyhine sonuçlar doğurabilir.

## Bölüm sonu kontrolü

- [ ] Resmî, gündelik ve anonim katmanlar ayrıldı
- [ ] Takma ad e-posta hizmeti kuruldu
- [ ] Telefon ve bilgisayar izinleri gözden geçirildi
- [ ] Tarayıcı, arama motoru ve DNS ayarlandı
- [ ] Mesajlaşmada kaybolan mesajlar ve gizlilik ayarları açık
- [ ] Sanal kart ve teslimat noktası kullanılıyor
- [ ] Yakınlara paylaşım kuralları söylendi
