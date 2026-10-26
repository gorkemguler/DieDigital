# 4. Search engines and archives

Search engines don't host content; they only point to it. So the order is always the same:

1. Get the **source** removed or changed: delete it yourself ([chapter 2](02-content-cleanup.md)), ask the site owner ([chapter 6](06-traces-held-by-others.md)), or use the law ([chapter 8](08-legal-rights.md)).
2. Then ask the search engine to **refresh** or **remove** the result.

As long as the source exists, a result you got removed from a search engine will come back. The exception is when you can't reach the source (the owner doesn't answer, it's abroad, the site is abandoned); then you go straight to the search engine.

## 4.1 See what comes up first

**How to search:**

- Use a private window, logged out of every account. Personalised results are misleading.
- Search Google, Bing, Yandex and DuckDuckGo separately; their results differ.
- Look at at least five pages of results, not just the first two.
- Record every hit in a table: URL, what's there (name, photo, phone...), who owns the source, what to do.

**Queries to run** (fill in your own details):

| What | Query |
|---|---|
| Your name | `"First Last"` |
| Name and city | `"First Last" "City"` |
| Name and work/school | `"First Last" "Company"` · `"First Last" "University"` |
| Spelling variants | `"First Last"` · `"Last First"` · `"F. Last"` · without accents or special characters |
| On social media | `"First Last" site:linkedin.com` · `site:facebook.com` · `site:instagram.com` · `site:x.com` · `site:tiktok.com` |
| In documents (CVs, lists, results) | `"First Last" filetype:pdf` · `filetype:docx` · `filetype:xlsx` |
| On forums | `"First Last" site:reddit.com` · local forums |
| In official notices | `"First Last" site:gov` · your country's government domain (e.g. `site:gov.uk`, `site:gov.tr`) |
| In archives | `"First Last" site:web.archive.org` |
| Your email address | `"you@example.com"` · `"you"` (just the part before the @) |
| Your username | `"old_handle"` |
| Your phone number | every format: `"+1 555 123 4567"` · `"(555) 123-4567"` · `"5551234567"` · with and without country code |
| Your address | `"Street name" "number"` · with your town |
| Your licence plate | `"ABC 1234"` |

**Images:** Run reverse image searches with your profile photos and frequently used photos on Google Lens, Bing Visual Search and Yandex Images. Yandex is often the most "successful" at matching faces. For face search engines, see [chapter 5](05-data-brokers-and-lookup-apps.md).

**Set up alerts:** Create Google Alerts (https://www.google.com/alerts) for your name, email and usernames so you hear about new results ([chapter 13](13-monitoring-and-maintenance.md)).

> **With the tool:** `diedigital footprint dorks --name ... --email ... --phone ...` turns all of these into a checklist with ready-made links for four search engines.

## 4.2 Google

| Tool | What for |
|---|---|
| [Results about you](https://myactivity.google.com/results-about-you) | Removing results that contain your phone number, home address or email; alerts when new ones appear. May not be available in your region yet. |
| [Remove personal information](https://support.google.com/websearch/troubleshooter/9685456) | Doxxing, ID numbers, bank/card details, signatures, medical records, non-consensual intimate images, images of minors. |
| [Remove outdated content](https://search.google.com/search-console/remove-outdated-content) | The source page was deleted or changed but Google still shows the old version. This is the tool you'll use most. |
| [Right to be forgotten (EU/UK)](https://reportcontent.google.com/forms/rtbf) | If you live in the EU, EEA or UK: removing the "your name + this URL" pairing. |
| [Legal removal requests](https://support.google.com/legal/answer/3110420) | Other legal grounds, by country. |

**Using the "outdated content" tool:**

1. Once the source page is deleted, or your details have been removed from it, copy the URL of the Google result.
2. Paste it into the tool. If the page is gone entirely, Google checks and drops the result.
3. If the page still exists but your name has been removed, enter your name as "a word that no longer appears on the page"; Google refreshes the cached snippet.

**Images:** The same tools work for Google Images. If the image is on your own site, remove it first, then use the outdated content tool.

## 4.3 Bing, DuckDuckGo, Yahoo

Most DuckDuckGo and Yahoo results come from Bing, so a removal at Bing carries over.

- [Bing Content Removal Tool](https://www.bing.com/webmasters/tools/contentremoval): removes outdated results and cached copies when the source page has been deleted or changed.
- If you live in Europe, Bing has a separate form for requests to block search results in Europe (on its privacy and support pages).

## 4.4 Yandex

Widely used in some regions, and results removed from Google can linger on Yandex. If you own the site, use the page removal tool in Yandex Webmaster. If not, request removal through Yandex support; once the source page is gone, the result usually drops out on its own after a while.

## 4.5 Legal routes

- **EU, EEA, UK:** The right to be forgotten (GDPR art. 17, following the 2014 *Google Spain* ruling of the EU Court of Justice) lets you ask search engines to stop showing results for your name that are inaccurate, inadequate, irrelevant or excessive. If refused, complain to your data protection authority. Text: [Appendix B](appendix-b-letter-templates.md).
- **United States:** There is no general right to be forgotten in search results. Use Google's personal information removal tools, and deal with the source directly (site owner, platform, data broker).
- **Turkey:** The Personal Data Protection Board (KVKK) decided on 23 June 2020 (decision 2020/481) that you can ask search engines to delist results for your name, and complain to the Board if they refuse. Under Law No. 5651, art. 9 lets a criminal judgeship of peace order content removed, blocked, and de-linked from your name in search engines when it violates your personality rights; art. 9/A provides an urgent route to the telecom authority for violations of private life. Details: [the Turkish chapter](../04-arama-motorlari-ve-arsivler.md).
- **Elsewhere:** Many countries have a data protection law with a deletion right, and defamation or privacy laws that allow removal orders. A local lawyer will know which applies.

For old news articles, ask the site itself first to remove your name, shorten it to initials, or blur your photo ([Appendix B](appendix-b-letter-templates.md)). Many publishers agree to reasonable requests.

## 4.6 Archives

### The Wayback Machine (archive.org)

To see what's archived: `https://web.archive.org/web/*/yourdomain.com/*` (your own site, old profiles, about pages).

The Internet Archive removes archived pages containing personal data on request. Email info@archive.org with the list of URLs (text: [Appendix B](appendix-b-letter-templates.md)). Say if you own the site; if you don't, explain that the pages contain your name and personal details.

### archive.today (archive.ph, archive.is)

Removal requests are rarely granted. Try anyway through the site's feedback/abuse link, citing personal data, and keep a record.

### Google cache

Google removed cached page links in 2024. If an old snippet still shows in results, the outdated content tool is enough.

### Web crawl datasets and AI

Removing data from old crawls already in datasets such as Common Crawl is practically impossible. Some AI companies (for example OpenAI: https://privacy.openai.com) offer forms to object to or remove personal information their models produce about you; for others, send a GDPR or equivalent request. Asking an AI assistant about yourself is also a way to check what it says.

## End-of-chapter checklist

- [ ] All queries run on four search engines and in reverse image search; results recorded
- [ ] For every result, the source removed or removal requested
- [ ] For removed sources, refresh requests sent to Google and Bing
- [ ] For sources that can't be removed, the search engine / legal route started
- [ ] Removal requested for Wayback Machine captures
- [ ] Google Alerts set up
