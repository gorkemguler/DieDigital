# 9. Final steps: email, phone, domain, devices, money

These come last because everything else depends on them.

## Domain and website

1. Remove the content (`noindex` → 410, see [chapter 2](02-content-cleanup.md)) and ask search engines to refresh.
2. If your personal details show in WHOIS, turn on the registrar's privacy service. Old WHOIS records stay in historical databases; those can't be deleted.
3. **Think before letting the domain go.** Expired domains are bought up quickly. A new owner could:
   - set up a site that looks like yours, under your name,
   - **receive mail sent to addresses on that domain.** If even one account registered with such an address is still open, they can take it over with "forgot password".

   Either keep the domain for a few more years (empty, with no MX records), or be absolutely sure no account is left on any address at that domain.
4. Close the hosting account, including its backups.

## Email addresses

- **Close them last.** First move the contact address on services you're keeping (bank, government, healthcare, work) to a new, private address.
- Unsubscribe from newsletters and opt out of marketing. Doing this before deleting reduces the chance of your address circulating on sold lists.
- Some providers have in the past reassigned addresses that were inactive for a long time. No account should remain tied to an address you close (the same risk as with domains).
- **Gmail:** Deleting only Gmail and deleting the whole Google account are different things. Gmail addresses aren't reassigned, but don't leave accounts tied to it anyway.
- One last time before closing: repeat the mailbox searches from [chapter 1](01-inventory-and-backup.md) (make sure no new accounts show up) and check that no deletion requests are still awaiting a reply. If replies will go to this address, update the contact address in those requests first.
- Turn off forwarding; mail flowing from a closed address to your new one links the two identities.

## Phone number

Your phone number is a more permanent identifier than your email: messaging apps, banks, deliveries and two-factor authentication all hang off it.

- Switch SMS two-factor authentication to an authenticator app (TOTP) or a security key.
- If you're changing numbers, update every account before cancelling the old one. Cancelled numbers are reissued to someone else after a while; no account recovery should depend on your old number.
- For caller-ID apps, see [chapter 5](05-data-brokers-and-lookup-apps.md).
- At level 3 (clean break), don't announce your new number to your old circle; give it only to the people you want to keep, one at a time. Anyone who saves your new number in their contacts can link it to your old name through caller-ID apps.

## Cloud storage

Google Drive / Photos, iCloud, OneDrive, Dropbox, Mega: delete the content, **empty the trash**, then close the account. Copies of folders you shared stay with the people you shared them with.

If you want cloud storage wiped automatically on a given date: [chapter 10](10-dead-mans-switch.md).

## Devices

- Phones, tablets, computers: turn off Find My / Find My Device and remove the device from your accounts (Apple Activation Lock, Google Factory Reset Protection).
- Factory-reset with disk encryption turned on. Once the key of an encrypted disk is wiped, the data is unreadable; on SSDs this is far more reliable than deleting files one by one.
- Smartwatches, smart TVs, game consoles, car infotainment systems: all may still be signed in.
- Old phones, drives and USB sticks you sell or throw away: encrypt and reset them the same way; physically destroy drives that no longer work.

## Money and crypto

- PayPal, payment apps, banking apps: withdraw the balance, then close. Records are kept for the legal retention period.
- Crypto exchanges: withdraw your assets first. Identity verification (KYC) documents are kept for the legal period; ask in writing for them to be deleted when it ends.

## Password manager

This goes last of all. Before closing it, take a final copy of your inventory list and store it offline with your encrypted backup, or delete everything. It's your call what to keep: a map for a day you might want to come back, or nothing.

## End-of-chapter checklist

- [ ] Decision made on the domain (keep it, or let it go only after confirming no account is tied to it)
- [ ] Contact email and number moved to new ones on the services I'm keeping
- [ ] SMS two-factor authentication switched to an authenticator app
- [ ] Old email addresses and numbers closed after confirming no accounts are tied to them
- [ ] Cloud storage emptied, trash cleared
- [ ] Devices removed from accounts and reset with encryption on
- [ ] Final decision made on the password manager
