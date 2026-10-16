# 8. Ölü adam anahtarı: belirlediğin zamanda kendiliğinden silinmek

Ölü adam anahtarı, belirli bir süre boyunca "hâlâ buradayım" demezsen (check-in) ya da belirlediğin bir tarih geldiğinde, kalan silme işlerini senin yerine yapan bir zamanlayıcıdır. Son iş olarak kendini, yani bu depoyu da siler.

İki katman kur. Biri bozulursa diğeri çalışır.

## Katman 1: Platformların kendi anahtarları

Bunlar şirketlerin kendi sunucularında çalışır; bu araç bozulsa da işler.

| Hizmet | Ayar | Ne yapar |
|---|---|---|
| Google | [Etkin Olmayan Hesap Yöneticisi](https://myaccount.google.com/inactive) | 3-18 ay hareketsizlikten sonra seçtiğin kişilere haber verir ve istersen hesabı tamamen siler. |
| Telegram | Ayarlar > Gizlilik ve Güvenlik > "Şu süre boyunca uzaktaysam" | Belirlediğin süre boyunca giriş yapmazsan hesabı tüm mesajlarıyla siler. |
| Facebook | Ayarlar > Anma ayarları | Vefat bildirildiğinde hesabın anma hesabına dönüşmek yerine silinmesini seçebilirsin. |
| Mastodon | Tercihler > Otomatik gönderi silme | Belirli yaştan eski gönderileri sürekli siler. |

Ayrıca Google ve Microsoft, iki yıl boyunca kullanılmayan kişisel hesapları politika gereği silebiliyor. Bunu bir güvence olarak değil, ek bir olasılık olarak gör.

## Katman 2: DieDigital ölü adam anahtarı

### Ne yapabilir?

| Eylem | Ne yapar |
|---|---|
| `send_letters` | Envanterde `privacy_email` alanı dolu ve hâlâ açık her hesaba KVKK/GDPR silme dilekçesi gönderir (daha önce talep gönderdiklerine hatırlatma). Facebook gibi API'si olmayan her yer için asıl güç budur: şirketin yasal silme yükümlülüğü başlar. |
| `github_wipe` | GitHub repolarını, gist'leri siler, profili boşaltır. |
| `reddit_wipe` | Reddit yorum ve gönderilerinin üzerine yazar, siler. |
| `mastodon_wipe` | Mastodon gönderilerini siler. |
| `email` | Serbest e-posta: güvendiğin birine haber, avukatına talimat, vb. |
| `command` | Herhangi bir komut: `rclone purge`, kendi betiğin, başka bir API. |
| `self_destruct` | En sonda bu depoyu siler. |

**Yapamayacakları:** Facebook, Instagram, LinkedIn gibi hizmetlerde hesap kapatmak tarayıcıda giriş, doğrulama kodu ve captcha ister; bunu güvenilir şekilde otomatikleştirmenin yolu yok. O yüzden bu hesapları ya **önceden** kendin kapat ya da tetiklemede `send_letters` ile yasal talep gönderilmesini sağla.

### Zaman çizelgesi

```
son check-in ──── checkin_interval_days ────▶ uyarılar ── grace_days ──▶ TETİKLEME
                                              (her warn_every_hours)        │
                                                                            ├─▶ eylemler sırayla
                                                                            │   (yarım kalan ertesi gün devam eder)
                                                                            └─▶ delay_days sonra self_destruct
```

- **Check-in modu:** `checkin_interval_days: 30, grace_days: 7` → 30 gün check-in yapmazsan uyarılar başlar, 7 gün daha yapmazsan tetiklenir.
- **Sabit tarih modu:** `"trigger_at": "2027-06-01T09:00:00Z"` → o tarihte tetiklenir; uyarılar 7 gün önceden başlar. Check-in sabit tarihi ertelemez; ertelemek için dosyayı düzenle.
- İkisini birlikte kullanırsan hangisi önce gelirse o tetikler.

### Güvenlik kilitleri

- **Kurulmadıkça hiçbir şey silinmez.** `DEADMAN_ARMED=true` (GitHub'da depo değişkeni) veya `--armed` yoksa tetiklendiğinde sadece ne yapacağını yazar ve sana haber verir.
- **Uyarı dönemi:** Tetiklemeden önce `grace_days` boyunca her gün e-posta (ve istersen telefon bildirimi) alırsın.
- **Tetiklendikten sonra da durdurabilirsin:** Check-in yaparsan henüz çalışmamış eylemler durur. Tamamlanmış olanlar geri alınamaz.
- **Durum dosyası kaybolursa** sayaç baştan başlar; erken tetiklenmez.
- **`self_destruct`** ancak diğer tüm eylemler bittikten (veya `max_attempts` kez denenip bırakıldıktan) sonra çalışır.
- **Haftalık ön kontrol:** Her hafta tüm token ve parolaları dener; süresi dolan bir şey varsa haber verir. Tetikleme günü "token geçersiz" sürprizi olmaz.

## Kurulum: GitHub Actions ile

Bilgisayarın kapalıyken de çalışması için en kolay yol.

### 1. Özel (private) bir kopya oluştur

**Fork yapma**: herkese açık bir deponun fork'u da herkese açıktır ve fork'larda zamanlanmış iş akışları kapalı gelir.

```bash
# GitHub'da yeni bir PRIVATE depo oluştur (ör. kaybolus), sonra:
git clone https://github.com/gorkemguler/DieDigital.git kaybolus
cd kaybolus
git remote set-url origin https://github.com/KULLANICI_ADIN/kaybolus.git
git push -u origin HEAD:main
```

İpucu: Bu depoyu ana GitHub hesabında değil, ayrı bir hesapta tutarsan, ana hesabını en sonda elle silmen anahtarı bozmaz. `github_wipe`'ın kullandığı token ana hesabına ait olmalı.

### 2. Yapılandır

```bash
python3 -m diedigital deadman init      # deadman.json ve .deadman/state.json oluşur
```

`deadman.json`'u düzenle: süreler, bildirim adresin, eylemler. Kullanmadığın eylemlerde `"enabled": false` bırak.

`send_letters` kullanacaksan envanteri depoya ekle (`.gitignore` bunu normalde engeller, depo özel olduğu için zorla ekliyoruz):

```bash
git add -f accounts.json
```

### 3. Secret'ları ekle

Depo > Settings > Secrets and variables > Actions > **New repository secret**:

| Secret | Gerekli mi | Değer |
|---|---|---|
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` | Bildirim ve dilekçe için evet | Gmail: `smtp.gmail.com`, `587`, adresin, uygulama şifresi |
| `DIEDIGITAL_PROFILE_JSON` | `send_letters` için | `profile.json`'un tüm içeriği |
| `GH_WIPE_TOKEN` | `github_wipe` / `self_destruct` için | Klasik token: `repo`, `delete_repo`, `gist`, `user` kapsamları. Süresini uzun tut; dolmadan önce ön kontrol uyarır. |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` | `reddit_wipe` için | [03](03-icerik-temizligi.md) |
| `MASTODON_TOKEN` | `mastodon_wipe` için | [03](03-icerik-temizligi.md) |
| `DEADMAN_WEBHOOK_URL` | İsteğe bağlı | Telefon bildirimi, ör. `https://ntfy.sh/uzun-rastgele-bir-konu-adi` (ntfy uygulamasında aynı konuya abone ol) |

Dilekçeler, hizmetlere kayıtlı olduğun e-posta adresinden gitmeli ([06](06-hukuki-haklar.md)). Farklı hizmetler farklı adreslerle açıldıysa en çok kullanılanın SMTP'sini ver.

### 4. Gönder ve dene

```bash
git add deadman.json .deadman/state.json
git commit -m "ölü adam anahtarı"
git push
```

GitHub'da: **Actions > deadman > Run workflow**

1. `preflight` → tüm satırlar "tamam" olmalı.
2. `dry-run` → tetiklenmiş gibi her eylemi çalıştırır, hiçbir şey silmez; neyin silineceğini log'da görürsün.
3. `status` → kalan süre.

### 5. Kur (arm)

Settings > Secrets and variables > Actions > **Variables** > New repository variable: `DEADMAN_ARMED` = `true`

Bundan sonra tetiklemede gerçekten silinir.

### 6. Check-in

**Actions > deadman > Run workflow > checkin.** GitHub mobil uygulamasından da yapabilirsin (depo > Actions > deadman > ⋯ > Run workflow). Takvimine bir hatırlatıcı koy.

Bilgisayardan: `python3 -m diedigital deadman checkin`, sonra `.deadman/state.json`'u commit'leyip push'la.

### Bilmen gerekenler

- **60 gün kuralı:** GitHub, herkese açık depolarda 60 gün boyunca hiçbir etkinlik olmazsa zamanlanmış iş akışlarını kapatır. Anahtar her hafta ön kontrol sonucunu depoya kaydettiği için normalde etkinlik oluşur; yine de Actions sekmesine ara sıra bak ve `checkin_interval_days + grace_days` toplamını 60 günün altında tutmayı düşün.
- **Dakika kotası:** Ücretsiz planda özel depolar için aylık Actions dakikası sınırlıdır. Günlük kontrol bir dakikadan az sürer; tetikleme günündeki uzun işler `max_runtime_minutes` (varsayılan 120) ile sınırlanır, kalanı ertesi güne kalır.
- **Erişimi olan herkes** secret'ları kullanan iş akışlarını çalıştırabilir. Depoya kimseyi ortak ekleme.
- Silinen bir depo, sahibi tarafından 90 güne kadar geri yüklenebilir; secret'lar ise depoyla birlikte silinir.
- **Hastalık, kaza, uzun tatil:** Anahtar "öldün" ile "ulaşılamıyorsun" arasındaki farkı bilmez. Süreleri buna göre seç.

## Kurulum: kendi sunucunda (cron)

GitHub kullanmak istemiyorsan bir VPS veya her zaman açık bir makinede:

```bash
# /opt/kaybolus/.env  (chmod 600)
DEADMAN_ARMED=true
SMTP_HOST=smtp.ornek.com
SMTP_PORT=587
SMTP_USER=sen@ornek.com
SMTP_PASSWORD=...
GH_WIPE_TOKEN=...
```

```cron
23 6 * * * cd /opt/kaybolus && set -a && . ./.env && set +a && python3 -m diedigital deadman run >> deadman.log 2>&1
```

Check-in: `ssh sunucu 'cd /opt/kaybolus && python3 -m diedigital deadman checkin'`

Burada `self_destruct` GitHub deposu silmek için anlamlı değilse çıkar; yerine sunucudaki dosyaları silen bir `command` eylemi koyabilirsin.

## Yapılandırma referansı

| Alan | Varsayılan | Açıklama |
|---|---|---|
| `checkin_interval_days` | - | Check-in yapmadan geçebilecek gün |
| `trigger_at` | - | Sabit tetikleme zamanı (ISO 8601, UTC) |
| `grace_days` | 7 | Tetiklemeden önceki uyarı süresi |
| `warn_every_hours` | 24 | Uyarı sıklığı |
| `preflight_every_days` | 7 | Ön kontrol sıklığı |
| `max_runtime_minutes` | 120 | Bir çalıştırmada eylemlere ayrılan süre |
| `notify.emails` | [] | Uyarıların gideceği adresler |
| `notify.webhook_env` | `DEADMAN_WEBHOOK_URL` | Webhook adresini tutan ortam değişkeni |
| `notify.webhook_format` | `text` | `text` (ntfy), `discord`, `slack` |
| `state_file` | `.deadman/state.json` | Durum dosyası |

Her eylemde ortak alanlar:

| Alan | Açıklama |
|---|---|
| `id` | Benzersiz ad. Ver: eylem sırasını değiştirdiğinde ilerleme kaybolmaz. |
| `type` | Eylem tipi |
| `enabled` | `false` ise yok sayılır |
| `delay_days` | Tetiklemeden kaç gün sonra çalışsın (ör. dilekçelere cevap gelsin diye e-posta silmeyi 40 gün sonraya koymak) |
| `max_attempts` | Hata verirse kaç gün denensin (varsayılan 7) |
| `stop_on_error` | Hata verirse sonraki eylemlere geçme |
| `force` | Sadece `self_destruct`: diğerlerini bekleme |

Eyleme özel alanlar:

```jsonc
{"type": "send_letters", "inventory": "accounts.json", "template": null,
 "statuses": ["active", "exported", "wiped", "requested"], "profile": "profile.json"}

{"type": "github_wipe", "include": ["*"], "exclude": ["sakla-*"], "repos": true, "gists": true,
 "scrub_profile": true, "token_env": "GH_WIPE_TOKEN"}

{"type": "reddit_wipe", "kinds": ["comments", "submitted"], "overwrite": true, "overwrite_text": ".",
 "ids_files": [{"path": "reddit/comments.csv", "kind": "comment"}], "pause_seconds": 1}

{"type": "mastodon_wipe", "instance": "https://mastodon.social", "keep_pinned": false,
 "older_than_days": null, "token_env": "MASTODON_TOKEN"}

{"type": "email", "to": ["kisi@ornek.com"], "subject": "...", "body": "...", "body_file": null}

{"type": "command", "argv": ["rclone", "purge", "gdrive:"], "timeout_minutes": 60}

{"type": "self_destruct", "repo": null, "delay_days": 1, "token_env": "GH_WIPE_TOKEN"}
```

`reddit_wipe` için `ids_files` kullanacaksan Reddit veri arşivindeki CSV'leri depoya `git add -f` ile ekle.
