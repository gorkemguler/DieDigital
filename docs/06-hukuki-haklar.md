# 6. Hukuki haklar: KVKK ve GDPR

> Bu bölüm genel bilgidir, hukuki danışmanlık değildir. Önemli bir uyuşmazlıkta avukata danış.

Silme seçeneği sunmayan, "silemiyoruz" diyen ya da hiç cevap vermeyen şirketlere karşı en güçlü aracın yasal silme hakkındır. Bir dilekçe gönderdiğinde şirketin artık yasal bir süresi ve kayıtlı bir yükümlülüğü olur.

## KVKK (Türkiye)

6698 sayılı Kişisel Verilerin Korunması Kanunu.

### Hakların (md. 11)

Veri sorumlusuna başvurarak şunları isteyebilirsin: verinin işlenip işlenmediğini ve hangi amaçla işlendiğini öğrenmek, yurt içinde veya yurt dışında kimlere aktarıldığını öğrenmek, eksik veya yanlışsa düzeltilmesi, **silinmesi veya yok edilmesi** (md. 7 şartları çerçevesinde), bu işlemlerin verinin aktarıldığı üçüncü kişilere bildirilmesi, otomatik analizle aleyhine çıkan bir sonuca itiraz ve kanuna aykırı işleme nedeniyle zararın giderilmesi.

**md. 7:** İşlenme şartları ortadan kalkan veri, talep üzerine silinir. Şirket bir kanuni yükümlülüğe dayanarak saklamaya devam edebilir, ama bunu ve süresini açıklamalıdır.

**Anayasa md. 20/3:** Herkesin kendisiyle ilgili kişisel verilerin korunmasını isteme hakkı vardır; bu hak verilerin düzeltilmesini veya silinmesini talep etmeyi de kapsar. Unutulma hakkı ayrıca Anayasa Mahkemesi (N.B.B. başvurusu, 2013/5653, 3.3.2016) ve Yargıtay Hukuk Genel Kurulu (E. 2014/4-56, K. 2015/1679) kararlarıyla tanındı.

### Nasıl başvurulur?

Veri Sorumlusuna Başvuru Usul ve Esasları Hakkında Tebliğ'e göre başvuru şu yollardan biriyle yapılır:

- Yazılı olarak (ıslak imzalı dilekçe; elden, iadeli taahhütlü posta veya noter),
- **Kayıtlı elektronik posta (KEP)**,
- Güvenli elektronik imza veya mobil imza ile,
- **Veri sorumlusuna daha önce bildirdiğin ve sistemde kayıtlı olan e-posta adresinden**,
- Veri sorumlusunun bu amaçla sunduğu bir başvuru formu veya uygulama üzerinden.

Araç dilekçeyi e-postayla gönderir: o hizmete kayıtlı olduğun adresin SMTP bilgileriyle gönderirsen dördüncü yolu kullanmış olursun. Önemli veya cevapsız kalan başvurularda KEP kullan; ispatı en güçlü yol odur.

Dilekçede bulunması gerekenler: ad soyad, (yazılıysa) imza, T.C. kimlik numarası (yabancılar için uyruk ve pasaport/kimlik numarası), tebligata esas adres, bildirime esas e-posta, telefon ve talep konusu.

> **T.C. kimlik numarası hakkında:** Tebliğ bunu istiyor; ama numaranı hiç bilmeyen bir şirkete göndermek yeni bir veri paylaşımı demek. Kayıtlı e-postandan başvuruyorsan çoğu şirket seni e-postayla tanımlar. Pratik yol: `profile.json`'da `national_id`'yi boş bırak (şablondaki satır kendiliğinden düşer); şirket isterse ver.

### Başvuru adresini bulmak

1. Sitenin **Aydınlatma Metni** veya **KVKK** sayfası; genelde altbilgide.
2. **VERBİS** (https://verbis.kvkk.gov.tr): Veri sorumlusu sorgulama ile şirketin kayıtlı adresini ve irtibat kişisini bul.
3. Şirketin **KEP adresi**: Ticaret sicili ve resmî yazışma sayfalarında genelde yazılıdır.

### Süreler

- **md. 13:** Şirket başvuruyu en kısa sürede ve **en geç 30 gün** içinde, kural olarak ücretsiz sonuçlandırır.
- **md. 14:** Başvurun reddedilirse, cevap yetersizse ya da süresinde cevap verilmezse, cevabı öğrendiğin tarihten itibaren 30 gün, her hâlde başvuru tarihinden itibaren **60 gün** içinde Kişisel Verileri Koruma Kurulu'na şikâyet edebilirsin (https://www.kvkk.gov.tr).

Şikâyet için doğrudan Kurul'a gidemezsin; önce veri sorumlusuna başvurmuş olman gerekir. O yüzden ilk dilekçeyi erken gönder.

## GDPR (AB ve AEA)

Avrupa Birliği Genel Veri Koruma Tüzüğü. Şirket AB'de kuruluysa ya da AB'de yaşayanlara hizmet veriyorsa uygulanır. Türkiye'de yaşıyorsan küresel şirketlere karşı GDPR'ın sana doğrudan uygulanıp uygulanmadığı tartışmalı olabilir; ama büyük şirketlerin çoğu silme taleplerini dünya genelinde aynı süreçle işler. Dilekçe yine işe yarar.

| Madde | Hak |
|---|---|
| 15 | Erişim: hangi verin tutuluyor, nereden geldi, kime verildi |
| 16 | Düzeltme |
| **17** | **Silme ("unutulma hakkı")** |
| 18 | İşlemenin kısıtlanması |
| 19 | Silme ve düzeltmenin alıcılara bildirilmesi |
| 20 | Veri taşınabilirliği |
| 21 | İtiraz; doğrudan pazarlamaya itiraz mutlaktır |
| 12(3) | Cevap süresi: 1 ay (gerekçeli olarak +2 ay) |
| 12(5) | Ücretsiz |
| 12(6) | Kimlik doğrulama: makul ölçüde |
| 77 | Denetim otoritesine şikâyet |

Silme hakkının istisnaları (md. 17/3): ifade ve haber alma özgürlüğü, kanuni yükümlülük, kamu yararı, hukuki taleplerin kurulması veya savunulması.

## Dilekçe araçları

Şablonlar:

| Şablon | Ne için |
|---|---|
| `kvkk-silme` | Türkiye'deki şirketler: silme, üçüncü kişilere bildirim, pazarlamanın durdurulması, saklanan verinin açıklanması |
| `kvkk-hatirlatma` | 30 gün içinde cevap gelmeyenler |
| `gdpr-erasure` | Yurt dışındaki şirketler (İngilizce) |
| `gdpr-reminder` | GDPR hatırlatması |
| `archive-removal` | Wayback Machine'den kaldırma |

Envanterdeki hesabın `jurisdiction` alanı `tr` ise `kvkk-silme`, değilse `gdpr-erasure` otomatik seçilir. Kendi şablonunu `templates/` klasörüne aynı adla koyarsan o kullanılır.

```bash
cp examples/profile.example.json profile.json     # bilgilerini doldur

# Tek bir hizmet
diedigital letters render --account 7                 # ekranda oku
diedigital letters send --account 7 --execute         # gönder (sana da kopya gelir)

# Envanterdeki tüm uygun hesaplar
diedigital letters bulk                              # kime gideceğini gör
diedigital letters bulk --execute

# 30 günü geçenler
diedigital inventory overdue
diedigital letters bulk --reminder --execute
```

SMTP ayarları ortam değişkenlerinden okunur:

```bash
export SMTP_HOST=smtp.gmail.com SMTP_PORT=587
export SMTP_USER=sen@gmail.com SMTP_PASSWORD='uygulama-sifresi'
```

Gönderilen her dilekçenin bir kopyası kendi adresine de gider; bu senin kanıtın. Gönderimden sonra hesap otomatik olarak `requested` durumuna geçer ve tarih kaydedilir.

## Cevap gelince

- **"Silindi":** Teyit e-postasını sakla, `inventory set <id> deleted`.
- **"Kimlik doğrulaması gerekli":** Ölçülü olanı ver ([00](00-baslarken.md)'daki kimlik doğrulama tuzağına bak).
- **"Yasal saklama nedeniyle bazı veriler tutulacak":** Hangi verinin, hangi dayanakla, ne kadar süre tutulacağını yazılı iste. Bu sürede başka amaçla işlenmemeli.
- **Ret veya cevapsızlık:** Hatırlatma gönder; yine olmazsa süreler içinde KVKK Kurulu'na (Türkiye) veya şirketin bağlı olduğu AB ülkesinin veri koruma otoritesine şikâyet et. Şikâyete şunları ekle: ilk başvuru ve tarihi, varsa cevap, neden yetersiz olduğu, hatırlatma.
