# DieDigital

İnternetten kaybolmak için adım adım bir rehber ve araç seti.

Hesaplarını bul, verini yedekle, içeriğini temizle, hesaplarını kapat, arama motorlarından ve veri simsarlarından düş, şirketlere yasal silme taleplerini gönder. Sonra bir **ölü adam anahtarı** kur: belirlediğin süre boyunca check-in yapmazsan ya da belirlediğin tarih geldiğinde kalan her şeyi siler ve en son kendini, yani bu depoyu da siler.

## Rehber

| | Bölüm | |
|---|---|---|
| 0 | [Başlarken](docs/00-baslarken.md) | Hedef, gerçekçi beklentiler, doğru sıra |
| 1 | [Envanter ve yedek](docs/01-envanter-ve-yedek.md) | Unuttuğun hesapları bul, verini indir |
| 2 | [Hesapları silmek](docs/02-hesaplari-silmek.md) | Platform platform silme yolları, Türkiye'deki hizmetler, İYS |
| 3 | [İçerik temizliği](docs/03-icerik-temizligi.md) | Hesap kapanmadan önce gönderi, yorum ve fotoğraflar |
| 4 | [Arama motorları ve arşivler](docs/04-arama-motorlari-ve-arsivler.md) | Google, Bing, Yandex, Wayback Machine, 5651 |
| 5 | [Veri simsarları ve rehberler](docs/05-veri-simsarlari-ve-rehberler.md) | Getcontact, Truecaller, kişi arama siteleri, yüz arama |
| 6 | [Hukuki haklar](docs/06-hukuki-haklar.md) | KVKK ve GDPR silme talepleri, süreler, şikâyet |
| 7 | [Son adımlar](docs/07-son-adimlar.md) | E-posta, telefon, alan adı, bulut, cihazlar |
| 8 | [Ölü adam anahtarı](docs/08-olu-adam-anahtari.md) | Zamanı gelince kendiliğinden silinmek |
| 9 | [Sonrası](docs/09-sonrasi.md) | Takip ve yeni alışkanlıklar |

## Araçlar

Python 3.10+, ek bağımlılık yok. Ayrıntılı kullanım: [docs/araclar.md](docs/araclar.md).

```bash
git clone https://github.com/gorkemguler/DieDigital.git && cd DieDigital
python3 -m diedigital --help
```

| Komut | Ne yapar |
|---|---|
| `inventory` | Hesap envanteri; parola yöneticisi CSV'sinden içe aktarma (parolalar okunmaz), Markdown kontrol listesi |
| `discover imap` | E-posta kutusundaki "hoş geldin / doğrula" mesajlarından unuttuğun hesapları bulur |
| `footprint` | Kullanıcı adının hangi sitelerde olduğu, Gravatar ve sızıntı kontrolü, arama motoru kontrol listesi |
| `catalog` | Bilinen hizmetlerin silme ve yedek bağlantıları, bekleme süreleri, tuzakları |
| `letters` | KVKK / GDPR silme dilekçeleri, hatırlatmalar, Wayback Machine kaldırma talebi; e-postayla gönderim |
| `wipe` | GitHub, Reddit ve Mastodon içeriklerini toplu siler |
| `deadman` | Ölü adam anahtarı: uyarır, tetiklenir, eylemleri sırayla çalıştırır, en son depoyu siler |

### Hızlı başlangıç

```bash
# 1. Hesaplarını topla
diedigital inventory import sifreler.csv
IMAP_PASSWORD=... diedigital discover imap --host imap.gmail.com --user sen@gmail.com --add
diedigital inventory report --out envanter.md

# 2. Ne görünüyor?
diedigital footprint dorks --name "Ad Soyad" --email sen@ornek.com --out arama.md
diedigital footprint username takma_adim

# 3. Temizle (önce deneme, sonra --execute)
diedigital wipe reddit
diedigital wipe github --scrub-profile

# 4. Silme dilekçeleri
cp examples/profile.example.json profile.json
diedigital letters bulk
diedigital letters bulk --execute

# 5. Ölü adam anahtarı
diedigital deadman init
diedigital deadman dry-run
```

## Ölü adam anahtarı kısaca

- İki mod: **check-in** (ör. 30 gün sessiz kalırsan) veya **sabit tarih** (ör. 1 Haziran 2027).
- Tetiklemeden önce `grace_days` boyunca her gün e-posta / telefon bildirimiyle uyarır.
- Tetiklenince: kalan hesaplara KVKK/GDPR dilekçeleri, GitHub/Reddit/Mastodon temizliği, istediğin komutlar, son olarak bu deponun silinmesi.
- Yarım kalan işler ertesi gün kaldığı yerden devam eder. Depoyu silme, diğer her şey bittikten sonra çalışır.
- GitHub Actions'ta günde bir çalışır; check-in GitHub mobil uygulamasından bir dokunuşla yapılır.
- `DEADMAN_ARMED=true` verilmedikçe hiçbir şey silinmez.

Kurulum: [docs/08-olu-adam-anahtari.md](docs/08-olu-adam-anahtari.md).

## Güvenlik

- Silen her komut varsayılan olarak deneme modundadır.
- `profile.json`, `accounts.json` ve CSV dışa aktarımları `.gitignore`'dadır. Ölü adam anahtarını kişisel bilgilerinle çalıştıracaksan bu depoyu fork'lama; **özel (private)** bir kopya oluştur.
- Token ve şifreler sadece ortam değişkenlerinden okunur, hiçbir dosyaya yazılmaz.
- Araçlar sadece senin kendi hesaplarında, kendi kimlik bilgilerinle çalışır.

## Katkı

Silme bağlantıları sık değişir. Eskimiş bir bağlantı ya da eksik bir hizmet görürsen [`diedigital/data/services.json`](diedigital/data/services.json)'u güncelleyen bir PR aç. Testler: `python3 -m unittest discover -s tests`.

## Uyarı

Bu rehber hukuki danışmanlık değildir. Silinen hesaplar ve veriler geri gelmez; her adımı yapmadan önce yedeğini al ve ne yaptığını oku.

Lisans: MIT
