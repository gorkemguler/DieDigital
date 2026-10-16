# 9. Sonrası: takip ve yeni alışkanlıklar

Silmek bir kerelik iş değil. Veri simsarları yeniden toplar, eski sayfalar yeniden indekslenir, unuttuğun bir hesap bir sızıntıda ortaya çıkar.

## Üç ayda bir

```bash
diedigital footprint dorks --name "Ad Soyad" --email sen@ornek.com --out arama.md
diedigital footprint username takma_adim
diedigital footprint email sen@ornek.com
diedigital inventory overdue
```

- Google'ın "Seninle ilgili sonuçlar" uyarılarını açık tut.
- [haveibeenpwned.com](https://haveibeenpwned.com)'da bildirim kaydı oluştur (bunun için de bir takma ad e-posta kullan).
- Veri simsarı sitelerini yeniden kontrol et ([05](05-veri-simsarlari-ve-rehberler.md)).
- Cevapsız dilekçeler için hatırlatma, gerekirse şikâyet ([06](06-hukuki-haklar.md)).

## Tamamen kaybolmadıysan: yeni alışkanlıklar

Bazı hesaplar zorunlu kalır (banka, devlet, iş). Bundan sonra iz bırakmamak için:

- **Her hizmete ayrı takma ad e-posta.** SimpleLogin, addy.io, Firefox Relay, Apple "E-postamı Gizle" gibi servisler bunu kolaylaştırır. Bir adres sızarsa ya da spam alırsa sadece onu kapatırsın; hesaplar birbirine bağlanamaz.
- **Telefon numaranı verme.** Gerekiyorsa sadece zorunlu hizmetlerde.
- **Sanal veya tek kullanımlık kart** ile çevrimiçi alışveriş.
- **Gerçek adın yerine takma ad**, gerçek ad gerekmeyen her yerde.
- **Fotoğraflarda konum bilgisi (EXIF) kapalı.** Telefonun kamera ayarlarından konum etiketini kapat; paylaşmadan önce konum bilgisini kaldır.
- **Arkadaşlarından** seni etiketlememelerini, fotoğraflarını sormadan paylaşmamalarını iste. İzinin önemli bir kısmı başkalarının paylaşımlarından gelir.
- **Konum geçmişi kapalı:** Google Haritalar Zaman Çizelgesi, Apple Önemli Konumlar.
- **Tuttuğun hesaplarda arama motoru görünürlüğü kapalı:** Facebook'ta "Arama motorlarının profiline bağlantı vermesine izin ver: Hayır"; LinkedIn'de herkese açık profil görünürlüğü kapalı; Instagram ve X'te gizli hesap.
- **Yeni bir hesap açmadan önce sor:** Gerçekten gerekli mi? Misafir olarak devam edilebilir mi? Silmek ne kadar zor olacak?

## Ölü adam anahtarının bakımı

Kurduysan:

- Takvimindeki check-in hatırlatıcısını kaçırma.
- Ön kontrol uyarısı gelirse (süresi dolan token, değişen şifre) hemen düzelt.
- Yeni hesap açtıysan ya da yeni bir dilekçe adresi bulduysan `accounts.json`'u güncelle ve push'la.
- Yılda bir `dry-run` ile planın hâlâ istediğin şey olduğunu kontrol et.
