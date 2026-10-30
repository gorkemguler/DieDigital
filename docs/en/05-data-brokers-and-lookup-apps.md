# 5. Data brokers, lookup apps and face search engines

This chapter is about places that collect data about you even though you never opened an account with them: caller-ID apps, people-search sites, sales and recruiting data platforms, face search engines.

## 5.1 Caller-ID and contact lookup apps

Apps such as Truecaller and Getcontact upload their users' address books and match your number with the names other people saved you under ("John Accountant", "Anna ex-landlord"). You're in there even if you've never used the app.

**Truecaller**

1. If you use the app: Settings > Privacy > Deactivate account.
2. Unlist your number at https://www.truecaller.com/unlisting.

**Getcontact**

1. If you use the app, turn off tag visibility in the privacy settings, then delete your account.
2. Send a data deletion request asking for all tags and records linked to your number to be deleted ([Appendix B](appendix-b-letter-templates.md)). Find the contact address in the app's privacy policy.

**Address books you uploaded**

You uploaded other people's numbers too. Delete your uploaded contacts before deleting your accounts:

- **Facebook / Messenger / Instagram:** Accounts Center > Your information and permissions > Upload contacts: turn off (uploaded contacts are deleted).
- **LinkedIn:** Settings > Data privacy > Sync contacts > delete uploaded contacts.
- **WhatsApp, Telegram, Signal:** These match your address book against their servers; it goes when the account is deleted. In Telegram: Settings > Privacy and Security > Data Settings > "Delete Synced Contacts".
- **Google:** https://contacts.google.com; if your phone backed up its contacts to Google, they're there.

**Visibility in messaging apps** (if you keep the account):

- WhatsApp: Settings > Privacy > Profile photo, About, Last seen, Status: My contacts or Nobody.
- Telegram: Settings > Privacy and Security > Phone number: Nobody; "Who can find me by my number": My contacts.
- Signal: Create a username and hide your number (Settings > Privacy > Phone number).

## 5.2 People-search sites and data brokers (US)

If you've lived in the US, or your address or phone number was ever recorded there, you probably have profiles on people-search sites:

| Site | Removal |
|---|---|
| Spokeo | https://www.spokeo.com/optout |
| Intelius, TruthFinder, Instant Checkmate | https://suppression.peopleconnect.us/login |
| TruePeopleSearch | https://www.truepeoplesearch.com/removal |
| FastPeopleSearch | https://www.fastpeoplesearch.com/removal |
| Whitepages, BeenVerified, Radaris, MyLife | the site's opt-out / suppression page |

- Use an email alias for removal confirmations ([chapter 11](11-living-invisibly.md)) so you don't hand your real address to yet another broker.
- These sites rebuild profiles from other sources. Check again every 3-6 months.
- **California residents:** the state's DROP platform (Delete Request and Opt-out Platform) sends a single deletion request to every registered data broker.
- **Other US states:** a growing number of states have privacy laws that give residents a right to delete; several also require data brokers to register, which gives you a list to work through.
- Paid services (such as Incogni, DeleteMe, Optery) send these requests on your behalf regularly. Remember that you're giving data to them too.

## 5.3 Data brokers and ad networks in Europe and the UK

Large marketing data companies, the marketing arms of credit reference agencies, and advertising networks are all covered by the GDPR (and UK GDPR). Send a GDPR deletion request to the contact listed in their privacy notice ([Appendix B](appendix-b-letter-templates.md)). The template asks both for deletion and for an end to marketing and profiling (GDPR art. 21), and asks where they got your data, which lets you dry up the original source.

## 5.4 Sales and recruiting data platforms (Apollo, Snov.io, ZoomInfo...)

These platforms sell contact databases to sales, marketing and recruiting teams: your name, job title, employer, work email and often your mobile number. You're in them even if you've never signed up. They build profiles by scraping LinkedIn and company websites, from email signatures in their users' inboxes, through browser extensions, and from data partners. Once your work email and phone are in, they keep resurfacing in cold emails and sales calls from companies you've never heard of.

The main ones: **Apollo.io, Snov.io, ZoomInfo, Lusha, RocketReach, Hunter.io, ContactOut, SignalHire, Seamless.AI, Kaspr, Cognism, UpLead.**

**Are you in there?**

- Try a search engine: `"First Last" (site:zoominfo.com OR site:rocketreach.co OR site:apollo.io OR site:signalhire.com OR site:contactout.com OR site:lusha.com)`. Some publish public profile pages.
- Opening an account on these platforms to look yourself up gives them fresh data. Send an access and deletion request instead and let them tell you what they hold. If you really need to look, use a free trial with an email alias and delete the account afterwards.

**How to get removed**

1. Look in the site footer for "Privacy", "Do Not Sell or Share My Personal Information", "Opt-out" or "Remove my profile". Most have a removal or privacy request form.
2. If there's no form, email the address in their privacy policy (usually `privacy@...`) using template 11 in [Appendix B](appendix-b-letter-templates.md). It covers GDPR and US state laws together.
3. **Ask for suppression, not just deletion.** If they only delete, their next crawl will collect you again. Ask for your email addresses and phone numbers to be added to a suppression (do-not-contact) list as well. They may need to keep a minimal record for that, such as a hashed email.
4. **Ask for the source:** Where did they get your data, and who did they sell it to? The answer points to the real leak: a contact who uses a browser extension, an event attendee list, an old employer's website.
5. **Cover every identifier:** These platforms may keep your work and personal emails, and old and new numbers, as separate records. List all of them in the request.
6. Check again in 3-6 months; these databases are constantly refreshed.

**Dry up the source**

- On LinkedIn, set your email and phone visibility to "Only you" and turn off your public profile ([chapter 2](02-content-cleanup.md)).
- Remove your mobile number from your email signature. The signature on every email you send can end up in these databases through the extensions your recipients use.
- Team pages on your company's website and conference attendee lists ([chapter 6](06-traces-held-by-others.md)).
- Tools like Hunter.io guess your company's email format (first.last@company.com). You can't stop that, but you can object to being kept as an individual contact record.
- When you leave a job your work email is closed, but the records in these databases stay; send the request anyway.

> **With the tool:** `diedigital catalog b2b` lists these platforms; when you add one to your inventory, `letters` automatically uses the deletion-and-suppression template (`data-broker-suppression`) for it.

## 5.5 Credit reference agencies

Credit files (Experian, Equifax, TransUnion and national credit bureaus) are kept on a legal basis and can't be deleted. You can request a copy, have errors corrected, and opt out of their marketing use.

## 5.6 Leaked-data lookup services

In several countries, illegal panels and messaging-app bots let people look up names, national ID numbers, addresses and family details from leaked databases. You can't get data deleted from them. What you can do:

- Make the leaked information worthless: change passwords, turn on two-factor authentication for government and bank accounts, and change your phone number and email if you can.
- Report such sites and bots to your data protection authority or the police.
- Be wary of "your bank is calling" or "your parcel" scams: a caller who knows your name, address and ID number is not proof that they're from that institution.

## 5.7 Face search engines

Services that find your photos online with facial recognition:

- **PimEyes:** use https://pimeyes.com/en/opt-out-request-form to have your face excluded from results. The photos stay on the source sites; get those removed through chapters [2](02-content-cleanup.md), [4](04-search-engines-and-archives.md) and [6](06-traces-held-by-others.md).
- **Others:** send a GDPR or equivalent request. Several of these services have been fined by European data protection authorities, so requests tend to be taken seriously.

Try one yourself first: searching a face search engine with your photo is the fastest way to see where you appear. But remember that the photo you upload goes to that service too; choose one that reveals as little as possible.

## 5.8 Advertising IDs and tracking

These don't make you disappear, but they slow down new profiles being built about you:

- **iOS:** Settings > Privacy & Security > Tracking > "Allow Apps to Request to Track": off.
- **Android:** Settings > Privacy > Ads > Delete advertising ID.
- **Google:** https://myadcenter.google.com > Personalised ads: off.
- **Meta:** Accounts Center > Ad preferences > "Ads based on activity information from ad partners": off.
- **Marketing opt-outs:** [chapter 3](03-deleting-accounts.md).

## End-of-chapter checklist

- [ ] Unlisted from Truecaller; deletion request sent to Getcontact
- [ ] Uploaded address books deleted from every platform
- [ ] Two-factor authentication on for government and bank accounts
- [ ] (If relevant) removal requested from US people-search sites
- [ ] Deletion and suppression requested from sales data platforms like Apollo, Snov.io and ZoomInfo
- [ ] Face search engines checked; opt-out requests sent
- [ ] Advertising IDs and personalised ads turned off
