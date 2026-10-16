# Araçlar

Python 3.10 veya üstü yeterli; başka bağımlılık yok.

```bash
git clone https://github.com/gorkemguler/DieDigital.git
cd DieDigital
python3 -m diedigital --help

# İstersen komut olarak kur:
pip install .
diedigital --help
```

Aşağıda `diedigital` yazan her yerde `python3 -m diedigital` de kullanabilirsin.

Silen her komut varsayılan olarak **deneme modunda** çalışır. Gerçek işlem için `--execute` (dilekçeler ve silme araçları) veya `--armed` / `DEADMAN_ARMED=true` (ölü adam anahtarı) gerekir.

## Dosyalar

| Dosya | İçerik | Git'te |
|---|---|---|
| `profile.json` | Ad, e-posta, adres, telefon; dilekçelerde kullanılır | `.gitignore` |
| `accounts.json` | Hesap envanteri | `.gitignore` (özel depoda `git add -f`) |
| `deadman.json` | Ölü adam anahtarı yapılandırması | özel depoda commit'lenir |
| `.deadman/state.json` | Son check-in, uyarılar, eylem ilerlemesi | özel depoda commit'lenir |

Örnekler: `examples/profile.example.json`, `examples/accounts.example.json`, `diedigital/data/deadman.example.json`.

Dosya yollarını değiştirmek için: `diedigital --inventory baska.json --profile baska-profil.json ...` ya da `DIEDIGITAL_INVENTORY`, `DIEDIGITAL_PROFILE` ortam değişkenleri.

## Komutlar

### catalog

```bash
diedigital catalog                 # bilinen tüm hizmetler
diedigital catalog instagram       # silme/yedek bağlantısı, bekleme süresi, notlar
diedigital catalog data-broker     # kategoriye göre
```

Katalog: `diedigital/data/services.json`. Eksik ya da eskimiş bir bağlantı görürsen burayı güncelle.

### inventory

```bash
diedigital inventory import sifreler.csv          # parola yöneticisi dışa aktarımı; parolalar okunmaz
diedigital inventory add "Hizmet" --url ... --username ... --email ... \
    --privacy-email kvkk@... --jurisdiction tr --notes ...
diedigital inventory list [--status active]
diedigital inventory set <#id|ad> <durum> [--note ...] [--privacy-email ...]
diedigital inventory report [--out envanter.md]
diedigital inventory overdue [--days 30]
```

Durumlar: `active`, `exported`, `wiped`, `requested`, `deleted`, `blocked`.

### discover

```bash
IMAP_PASSWORD=... diedigital discover imap --host imap.gmail.com --user sen@gmail.com \
    [--since 2015-01-01] [--folder INBOX] [--all] [--add]
```

E-posta başlıklarında kayıt, doğrulama ve şifre sıfırlama mesajlarını arar; gönderen alan adlarını puanlar. `--add` bulunanları envantere ekler.

### footprint

```bash
diedigital footprint username takma_adim [--all]
diedigital footprint email sen@ornek.com [--add]     # Gravatar; HIBP_API_KEY varsa sızıntılar
diedigital footprint dorks --name "Ad Soyad" --email ... --username ... --phone ... --city ... --out arama.md
```

### letters

```bash
diedigital letters list
diedigital letters render --account <id> [--template ...] [--reminder] [--out dosya.txt]
diedigital letters render --service "Şirket" --template kvkk-silme
diedigital letters render --template archive-removal --url ... --url ...
diedigital letters send --account <id> [--to adres] [--reminder] --execute
diedigital letters bulk [--status active ...] [--reminder] --execute [--yes]
```

### wipe

```bash
diedigital wipe github [--include 'glob'] [--exclude 'glob'] [--no-repos] [--no-gists] [--scrub-profile] [--execute]
diedigital wipe reddit [--no-overwrite] [--text .] [--ids-file comments.csv] [--execute]
diedigital wipe mastodon --instance https://... [--keep-pinned] [--older-than-days 90] [--execute]
```

### deadman

```bash
diedigital deadman init        # deadman.json + durum dosyası
diedigital deadman status      # kalan süre, eylemlerin durumu
diedigital deadman checkin     # sayacı sıfırla (tetiklenmişse kalan eylemleri durdurur)
diedigital deadman preflight   # token/parolaları dene
diedigital deadman dry-run     # tetiklenmiş gibi çalıştır, hiçbir şey silme
diedigital deadman run [--armed]   # cron / GitHub Actions'ın çağırdığı komut
```

Ayrıntılar: [08-olu-adam-anahtari.md](08-olu-adam-anahtari.md).

## Ortam değişkenleri

| Değişken | Kullanan |
|---|---|
| `SMTP_HOST`, `SMTP_PORT` (587), `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` | dilekçeler, bildirimler. Port 465 ise SSL, değilse STARTTLS. |
| `IMAP_PASSWORD` | `discover imap` |
| `HIBP_API_KEY` | `footprint email` |
| `GH_WIPE_TOKEN` | `wipe github`, `self_destruct` |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` | `wipe reddit` |
| `MASTODON_TOKEN` | `wipe mastodon` |
| `DIEDIGITAL_PROFILE_JSON` | `profile.json` yerine (GitHub secret) |
| `DIEDIGITAL_TEMPLATES` | Ek şablon klasörü |
| `DEADMAN_ARMED` | `true` ise ölü adam anahtarı gerçekten siler |
| `DEADMAN_WEBHOOK_URL` | Bildirim webhook'u (ntfy, Discord, Slack) |

## Testler

```bash
python3 -m unittest discover -s tests -v
```
