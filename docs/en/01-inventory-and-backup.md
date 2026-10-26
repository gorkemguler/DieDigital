# 1. Inventory and backup

You can't delete an account you don't know about, and most people have far more online accounts than they remember. By the end of this chapter you'll have three things: a complete list of your accounts, a backup of your data, and a habit of no longer creating new traces.

## 1.1 Stop creating traces first

Starting today, before you delete anything:

- No new posts, comments or photo uploads.
- No new accounts. If you have to open one, use an email alias ([chapter 11](11-living-invisibly.md)).
- Turn off location services, location history and location tagging on photos.
- Revoke apps' access to your contacts (Settings > Privacy > Contacts).
- Stop using "Sign in with Google / Facebook / Apple" buttons.

## 1.2 The inventory spreadsheet

Start a spreadsheet, offline, or use paper. Don't put it in a cloud document: this list will be one of the most sensitive documents about you.

| Service | URL | Username / email | Phone linked | Payment details | Backup | Content removed | Deletion requested | Waiting period ends | Deleted | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Example Forum | forum.example.com | old_handle | no | no | – | ✓ 12 Mar | 12 Mar | – | ✓ 15 Mar | |

Every account goes through the same stages: **found → backed up → content removed → deletion requested → waiting period over → deletion confirmed.** Mark the ones you can't delete as "cannot delete" and write down why (legal retention, company not responding, lost access).

> **With the tool:** `diedigital inventory` keeps the same list, adds deletion links for known services and produces a checklist report ([Appendix C](appendix-c-tools.md)).

## 1.3 Find your accounts

Go through every source below. Each one finds accounts the others miss.

### All your email addresses and phone numbers

First list your identifiers, because your accounts hang off them:

- **Every** email address you use or have used: old Hotmail/Yahoo addresses, school and work addresses, addresses on your own domain.
- Your current and **past phone numbers**.
- Every **username and nickname** you've used.

If you've lost access to an old email address, try to recover it now. You'll need it to delete the accounts registered with it.

### Password manager and browser

Saved passwords are the best list you'll get. Go through them or export them:

- **Chrome:** Settings > Autofill and passwords > Google Password Manager
- **Firefox:** type `about:logins` in the address bar
- **Safari / iCloud Keychain:** the Passwords app on macOS and iOS
- **Bitwarden, 1Password, KeePass:** every entry in the vault

If you exported a file, delete it securely when you're done; it contains all your passwords.

> **With the tool:** `diedigital inventory import passwords.csv` reads only the site and username columns, never the passwords.

### Your mailbox

Almost every sign-up sends a "welcome" or "verify your email" message. Run these searches in every mailbox:

**Gmail** (paste into the search box):

```
subject:(welcome OR verify OR "confirm your" OR "your account" OR "activate" OR "registration" OR "password reset")
```

**Outlook / Hotmail:** search one at a time for `welcome`, `verify`, `confirm your`, `your account`

Also search for:

- `unsubscribe`: any brand sending you newsletters probably holds an account for you.
- `receipt`, `order`, `invoice`: shops you've bought from.
- `new sign-in`, `login`, `security alert`: accounts you actively use.

Group the results by sender domain and add them to your list.

> **With the tool:** `diedigital discover imap` opens the mailbox read-only, looks only at message headers and lists likely accounts with a score.

### "Sign in with Google / Apple / Facebook" accounts

Accounts you opened without a password don't show up in a password manager:

- **Google:** https://myaccount.google.com/connections
- **Apple:** Settings > [your name] > Sign in with Apple
- **Facebook:** Settings > Apps and websites
- **Microsoft, GitHub, X, LinkedIn:** Settings > Connected apps / Authorized applications

Add each one to your list. Removing the connection doesn't delete the account; it only cuts off that way of logging in. Delete the account first, then remove the connection.

### Data breaches

Search every email address and phone number on https://haveibeenpwned.com. Every breach means you had an account there, and you've probably forgotten most of them. Mozilla Monitor (https://monitor.mozilla.org) runs a similar check.

### The "forgot password" test

If you're not sure whether you have an account somewhere, request a password reset with your email. If it doesn't say "no account with this email" and a reset email arrives, you have an account. Some sites show the same message either way to protect privacy; in that case, check your inbox.

### Your usernames

Search every username in quotes on a search engine: `"old_handle"`. Then try the big sites directly: `instagram.com/old_handle`, `x.com/...`, `tiktok.com/@...`, `github.com/...`, `reddit.com/user/...`, `youtube.com/@...`, `pinterest.com/...`, `twitch.tv/...`, `medium.com/@...`, `t.me/...`

> **With the tool:** `diedigital footprint username old_handle` checks more than 30 sites at once.

### Your phone, old phones and app stores

- The apps on your phone.
- **App Store:** Account > Purchased. Apps you installed years ago and deleted are listed here.
- **Google Play:** Profile > Manage apps & device > Manage > "Not installed".
- Sender names of verification codes in your text messages.

### Payments

- Recurring charges on card and bank statements.
- App Store and Google Play subscriptions.
- "Automatic payments" in PayPal and similar services.

### Browser history and bookmarks

If you've used the same browser for years, frequently visited sites and old bookmarks will remind you of forgotten accounts.

### Memory checklist

Go category by category:

- **Social and content:** social networks, blogs, video, music, photo sites, forums, Q&A sites
- **Messaging:** WhatsApp, Telegram, Signal, Discord, Skype, old messenger accounts
- **Shopping:** online stores, second-hand and classifieds sites, brands' own shops
- **Food, groceries, transport:** delivery apps, ride-hailing, scooters, car rental, transit cards
- **Travel:** airline loyalty programmes, hotel chains, booking sites
- **Finance:** banks, payment apps, crypto exchanges, investment apps, insurance
- **Health and fitness:** appointment apps, gyms, fitness and running apps, period trackers, nutrition and sleep apps
- **Education and work:** school platforms, online courses, certificate sites, job boards, freelancing platforms
- **Gaming:** Steam, Epic, PlayStation, Xbox, Riot, mobile games
- **Dating apps**
- **Events and tickets:** ticketing sites, clubs, associations
- **Petitions and donations:** your name may be publicly visible on petitions you signed
- **Local government and utility apps, loyalty cards, parcel delivery apps**
- **AI chat assistants:** your chat history is personal data too

## 1.4 Back up your data

Request exports **now**; some take days to prepare.

| Service | Export |
|---|---|
| Google (Gmail, Photos, Drive, YouTube) | https://takeout.google.com |
| Facebook | https://www.facebook.com/dyi |
| Instagram, Threads | Accounts Center > Your information and permissions > Download your information |
| X (Twitter) | https://x.com/settings/download_your_data |
| LinkedIn | Settings > Data privacy > Get a copy of your data |
| WhatsApp | Export each chat separately; Settings > Account > Request account info |
| Telegram | Telegram Desktop > Settings > Advanced > Export Telegram data |
| Apple | https://privacy.apple.com |
| Microsoft | https://account.microsoft.com/privacy |
| Reddit | https://www.reddit.com/settings/data-request |
| Discord | Settings > Data & Privacy > Request all of my data |
| Spotify | https://www.spotify.com/account/privacy/ |
| Everything else | Look for "download your data" or "data export" in settings; if there isn't one, request it with a data access request (GDPR art. 15 / CCPA "right to know"; [Appendix B](appendix-b-letter-templates.md)) |

Decide what you actually want to keep. You don't have to keep everything; if you want to disappear, letting go of some memories can be part of the process.

How to store backups:

- **Encrypted:** a VeraCrypt container, or an archive with a strong password and encrypted file names (`7z a -p -mhe=on backup.7z folder/`).
- **Offline:** not in the cloud, but on two separate external drives kept in two different places.
- Your backup is the most complete dataset about you that exists. If you want to disappear, it's the thing that needs the best protection.

## End-of-chapter checklist

- [ ] I've stopped creating new traces
- [ ] I have a list of all my email addresses, phone numbers and usernames
- [ ] The inventory covers every source in this chapter
- [ ] Exports were requested, downloaded and stored encrypted
