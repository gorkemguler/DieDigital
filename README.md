# DieDigital

**İnternetten tamamen kaybolma rehberi.**

Türkçe · [English](README.en.md)

Hesaplarını bulmaktan son e-posta adresini kapatmaya, arama motorlarından düşmekten sokak görüntülerinde evini bulanıklaştırmaya, arkadaşlarının paylaştığı fotoğraflardan şirketlerin elindeki veriye kadar internetteki izlerini adım adım silmenin ve bundan sonra iz bırakmadan yaşamanın yolu. İstersen sonunda, belirlediğin bir zamanda geri kalan her şeyi kendiliğinden silen bir **ölü adam anahtarı** da kurarsın.

Teknik bilgi gerekmez; her adım elle yapılabilir. Türkiye'deki hizmetler, KVKK ve Türk hukuku ayrıca ele alınır.

## Nereden başlamalı?

1. [**Başlarken**](docs/00-baslarken.md)'i oku: ne kadar kaybolmak istediğini (görünmez / hesapsız / tam kopuş) ve kimden saklandığını seç.
2. Belirli bir kişiden saklanıyorsan önce [**Takip, taciz, şiddet**](docs/12-takip-taciz-siddet.md) bölümünü oku.
3. [**Kontrol listesini**](docs/ek-a-kontrol-listesi.md) kendine kopyala ve bölümleri sırayla izle.

## Rehber

| # | Bölüm | Ne |
|---|---|---|
| 0 | [Başlarken](docs/00-baslarken.md) | Seviyeler, kimden saklandığın, neler silinmez, altın kurallar, yol haritası |
| 1 | [Envanter ve yedek](docs/01-envanter-ve-yedek.md) | İz üretmeyi durdur, unuttuğun hesapları bul, verini indir |
| 2 | [İçerik temizliği](docs/02-icerik-temizligi.md) | Gönderiler, fotoğraflar, yorumlar, değerlendirmeler; platform platform |
| 3 | [Hesapları silmek](docs/03-hesaplari-silmek.md) | Büyük platformlar, Türkiye'deki hizmetler, İYS, sahipsiz hesaplar |
| 4 | [Arama motorları ve arşivler](docs/04-arama-motorlari-ve-arsivler.md) | Ne aranır, Google/Bing/Yandex kaldırma araçları, Wayback Machine, 5651 |
| 5 | [Veri simsarları ve rehberler](docs/05-veri-simsarlari-ve-rehberler.md) | Getcontact, Truecaller, yüklenen rehberler, sızıntı panelleri, yüz arama |
| 6 | [Başkalarının elindeki izler](docs/06-baskalarinin-elindeki-izler.md) | Arkadaşlar, aile, işyeri, okul, etkinlikler, haberler, Vikipedi, soy ağacı |
| 7 | [Gerçek dünyaya bağlı izler](docs/07-gercek-dunya-izleri.md) | Adres, Street View, konum, Wi-Fi, akıllı cihazlar, sağlık, DNA, plaka |
| 8 | [Hukuki haklar](docs/08-hukuki-haklar.md) | KVKK, GDPR, 5651; adım adım silme talebi ve şikâyet |
| 9 | [Son adımlar](docs/09-son-adimlar.md) | Alan adı, e-posta, telefon, bulut, cihazlar, para |
| 10 | [Ölü adam anahtarı](docs/10-olu-adam-anahtari.md) | Platformların kendi anahtarları, zamanlanmış dilekçeler, dijital vasi, otomatik anahtar |
| 11 | [Görünmez yaşamak](docs/11-gorunmez-yasamak.md) | Kimlik katmanları, takma ad e-posta, cihaz, tarayıcı, VPN/Tor, ödeme, tam kopuş |
| 12 | [Takip, taciz, şiddet](docs/12-takip-taciz-siddet.md) | Biri seni arıyorsa: önce kanıt, sonra güvenlik, en son silme |
| 13 | [Takip ve bakım](docs/13-takip-ve-bakim.md) | Silinenlerin silinmiş kalması |
| A | [Kontrol listesi](docs/ek-a-kontrol-listesi.md) | Tüm rehberin işaretlenebilir özeti |
| B | [Dilekçe ve mesaj örnekleri](docs/ek-b-dilekce-ornekleri.md) | KVKK, GDPR, arama motoru, KVKK Kurulu şikâyeti, haber sitesi, rica mesajları |
| C | [Araçlar](docs/ek-c-araclar.md) | İsteğe bağlı komut satırı araçları |

## Gerçekçi beklenti

Sıfır iz mümkün değil: resmî kayıtlar, yasal saklama süresi olan kayıtlar, başkalarının cihazlarındakiler ve sızıntılar silinmez. Bu rehberin hedefi şu: **aranınca çıkmamak, bilinen her yerde silinmiş olmak, silinemeyen yerlerde yasal talebini iletmiş olmak ve yeni iz üretmemek.**

## İsteğe bağlı araçlar

Uzun işleri hızlandırmak için depoda bağımlılıksız bir Python aracı var (Python 3.10+). Rehberi izlemek için gerekli değildir.

```bash
git clone https://github.com/gorkemguler/DieDigital.git && cd DieDigital
python3 -m diedigital --help
```

| Komut | Ne yapar |
|---|---|
| `inventory` | Hesap envanteri; parola yöneticisi CSV'sinden içe aktarma (parolalar okunmaz), işaretlenebilir rapor |
| `discover imap` | E-posta kutusundaki "hoş geldin / doğrula" mesajlarından unuttuğun hesapları bulur |
| `footprint` | Kullanıcı adı taraması, Gravatar ve sızıntı kontrolü, arama motoru kontrol listesi |
| `catalog` | Bilinen hizmetlerin silme ve yedek bağlantıları, bekleme süreleri |
| `letters` | KVKK / GDPR dilekçelerini doldurur ve e-postayla gönderir; hatırlatmalar |
| `wipe` | GitHub, Reddit ve Mastodon içeriklerini toplu siler |
| `deadman` | Ölü adam anahtarı: uyarır, tetiklenir, eylemleri sırayla çalıştırır, en son kendi deposunu siler |

Silen her komut varsayılan olarak deneme modundadır. Ayrıntılar: [Ek C](docs/ek-c-araclar.md).

## Katkı

Silme bağlantıları ve menü adları sık değişir. Eskimiş bir bilgi ya da eksik bir hizmet görürsen ilgili bölümü veya [`diedigital/data/services.json`](diedigital/data/services.json)'u güncelleyen bir PR aç.

## Uyarı

Bu rehber hukuki danışmanlık değildir ve yasal yükümlülüklerden kaçmanın rehberi değildir. Silinen hesaplar ve veriler geri gelmez; her adımdan önce yedeğini al ve ne yaptığını oku.

Lisans: MIT
