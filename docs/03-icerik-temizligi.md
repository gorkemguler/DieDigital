# 3. İçerik temizliği

Hesap kapanmadan önce içerik silinmeli, çünkü:

- Bazı platformlar hesabı silince içeriği bırakır (Reddit, Discord, Stack Overflow, birçok forum).
- Silme bekleme sürecinde bir şey ters giderse en azından içerik gitmiş olur.
- Platformların silme işlemi bazen yarım kalır; içerik önceden temizlenmişse önemi kalmaz.

Tüm `wipe` komutları varsayılan olarak **deneme modunda** çalışır: ne silineceğini listeler, hiçbir şeye dokunmaz. Gerçekten silmek için `--execute` eklersin; araç bir kez daha onay ister.

## Reddit

Hesabı silmek yorumlarını silmez. Araç her yorumun ve metin gönderisinin üzerine anlamsız bir metin yazar, sonra siler. Üzerine yazmak önemli: silinen içeriğin son hâli bazı üçüncü taraf arşivlerde kalabiliyor, en azından son hâli anlamsız olur.

1. https://www.reddit.com/prefs/apps > "create another app" > tür: **script**, redirect uri: `http://localhost:8080`
2. Ortam değişkenleri:

   ```bash
   export REDDIT_CLIENT_ID=...       # uygulama adının altındaki kısa kod
   export REDDIT_CLIENT_SECRET=...
   export REDDIT_USERNAME=...
   export REDDIT_PASSWORD=...
   ```

3. Deneme, sonra gerçek:

   ```bash
   diedigital wipe reddit
   diedigital wipe reddit --execute
   ```

Reddit listeleri en fazla ~1000 öğe gösterir. Daha eskileri için https://www.reddit.com/settings/data-request üzerinden verilerini iste; gelen arşivdeki dosyaları ver:

```bash
diedigital wipe reddit --ids-file comments.csv --ids-file posts.csv --execute
```

İki adımlı doğrulama açıksa script uygulamalarıyla parola girişi çalışmayabilir; işlem süresince geçici olarak kapatman gerekebilir.

## GitHub

```bash
export GH_WIPE_TOKEN=ghp_...   # klasik token: repo, delete_repo, gist, user
diedigital wipe github                         # ne silineceğini gör
diedigital wipe github --exclude 'sakla-*' --scrub-profile --execute
```

Kendi repolarını ve gist'lerini siler, `--scrub-profile` ile ad, biyografi, konum, şirket, web sitesi alanlarını boşaltır. Hesabın kendisi API ile silinemez; en son Settings > Account > Delete your account.

Silinmeyenler: başkalarının depolarına gönderdiğin commit'ler, açtığın issue ve yorumlar ("ghost" kullanıcısına devredilir). Commit'lerdeki e-posta adresin, depo sahibi geçmişi yeniden yazmadıkça kalır. Bundan sonrası için `git config --global user.email KULLANICI@users.noreply.github.com`.

## Mastodon

```bash
export MASTODON_TOKEN=...   # Tercihler > Geliştirme > Yeni uygulama (read, write:statuses)
diedigital wipe mastodon --instance https://mastodon.social --execute
```

Mastodon silmeyi yavaşlatır (varsayılan: 30 dakikada 30 gönderi). Büyük hesaplarda bu saatler sürer. Alternatif: Tercihler > Otomatik gönderi silme ile sunucuya sildir.

## X (Twitter)

Ücretsiz API ile toplu silme pratikte mümkün değil. Seçenekler:

1. **Hesabı gizle** (Ayarlar > Gizlilik > Gönderilerini koru): gönderiler hemen aramalardan ve herkese açık görünümden düşer; temizlik sürerken zaman kazandırır.
2. Hesabı devre dışı bırak: 30 gün sonra gönderiler de silinir.
3. Tek tek silmek istediğin, özellikle hassas gönderiler varsa önce onları sil; alıntılar ve ekran görüntüleri ayrıca kalır.

## Facebook ve Instagram

- **Facebook:** Profil > ⋯ > Etkinlik günlüğü > Senin etkinliğin. Gönderiler, yorumlar, beğeniler, etiketler kategorilerinde toplu seç > Çöp kutusu / Kaldır.
- **Instagram:** Profil > ☰ > Hareketlerin > Fotoğraflar ve videolar / Yorumlar / Beğeniler > Seç > Sil.
- **Etiketler:** Başkalarının fotoğraflarındaki etiketlerini kaldır. Fotoğrafın kendisi için paylaşan kişiden kaldırmasını iste; olmazsa platformun gizlilik ihlali bildirim formunu kullan.
- **Gruplar:** Grup gönderilerin ve yorumların ayrı listelenir; hesabı silmeden önce gruplardan çık.

## Google ve YouTube

- **YouTube yorumları:** https://myactivity.google.com/page?page=youtube_comments (başkalarının videolarına yazdıkların; kanal silinse de kalabilir).
- **Google Haritalar:** Haritalar > Katkıların > Yorumlar ve Fotoğraflar. Yerel Rehber yorumların adınla ve profil fotoğrafınla görünür; çok kişi unutur.
- **Blogger, Google Sites, paylaşılan Drive dosyaları:** "Bağlantıya sahip herkes" ile paylaştığın dosyalar indekslenebilir. Drive'da paylaşılanları tek tek kapat.

## Discord

Mesajların hesap silinince kalır ("Deleted User"). Kendi hesabınla otomatik silme yapan araçlar (self-bot) Discord kurallarına aykırıdır. Doğru yol:

1. Veri paketini iste (Ayarlar > Veri ve Gizlilik).
2. Paketten mesaj attığın kanal kimliklerini çıkar.
3. Discord'un gizlilik talebi formundan bu kanallardaki mesajlarının silinmesini GDPR/KVKK kapsamında iste.

Küçük ve özel sunuculardaki mesajlar için sunucu yöneticilerinden de yardım isteyebilirsin.

## Mesajlaşma uygulamaları

- **Telegram:** Özel sohbetlerde geçmişi istediğin zaman iki taraftan birden silebilirsin ("Ayrıca ... için de sil"). Gruplarda sadece kendi mesajlarını.
- **WhatsApp:** "Herkesten sil" sadece kısa bir süre için mümkün. Eski mesajlar karşı tarafta kalır; önemli olanlar için kişiden silmesini istemek dışında yol yok.

## Stack Overflow ve forumlar

- Stack Overflow içerikleri CC BY-SA lisanslıdır; profil silinince içerik isimsizleştirilir ama kalır. Kendi sorularını ve kabul edilmemiş cevaplarını silebilirsin; kalanlar için profil silme yeterli.
- **Forumlar ve Ekşi Sözlük:** Önce kendi yazdıklarını sil, sonra hesabı kapat. Forum yöneticisine yazarken KVKK/GDPR dilekçesi daha ciddiye alınır.
- **Şikâyet ve yorum siteleri:** Şikâyetlerin ve yorumların çoğu zaman ad soyadınla görünür. Hesap ayarlarından ya da destek üzerinden kaldırt.

## Kendi web siten ve blogun

Arama motorlarının sayfayı hızla bırakması için:

1. Sayfayı kaldırmadan önce `<meta name="robots" content="noindex">` ekle ve birkaç gün bekle.
2. Sonra sayfayı sil ve sunucunun **410 Gone** dönmesini sağla (404'ten hızlı düşer).
3. Google Search Console'a siteyi doğrulayıp "Kaldırmalar" aracını kullan.
4. Alan adıyla ne yapacağına [07](07-son-adimlar.md)'de karar ver: alan adını bırakmanın bir güvenlik riski var.
