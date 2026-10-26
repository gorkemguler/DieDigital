# 11. Living invisibly

Deleting cleans up the past. Staying invisible protects the future. Read this chapter early: every new account you have to open and every new number you get during the process should follow these rules.

## 11.1 Split your identity into layers

One email address, one phone number and one username tie everything together. Use three separate layers instead:

| Layer | Where | Identity |
|---|---|---|
| **Official** | Bank, government, employer, healthcare, insurance, landlord | Your real name, a dedicated email, your main number. Used nowhere else. |
| **Everyday** | Shopping, transport, subscriptions, apps | A separate email alias for each service; no real name or phone number unless required. |
| **Anonymous** | Forums, comments, communities | A pseudonym, a separate email, and nothing in common with your real identity (photo, writing style, time zone, username). |

Share nothing between layers: no shared username, profile photo, recovery email, phone number or password.

## 11.2 Email

- **For the official layer,** consider a privacy-focused provider (such as Proton Mail or Tuta). If you use your own domain, be prepared to keep the domain for a long time ([chapter 9](09-final-steps.md)).
- **For the everyday layer, use alias services:** SimpleLogin, addy.io, Firefox Relay, DuckDuckGo Email Protection, Apple's Hide My Email. You give each service a different address and the mail is forwarded to your real inbox. If one address leaks or gets spam, you close just that one, and your accounts can't be linked to each other.
- Block tracking pixels in emails: turn off "load remote images" in your mail app.

## 11.3 Phone number

- In many countries, SIM cards must be registered with ID, so an anonymous number may not be an option. Not giving your number out matters more than hiding it.
- Give your number only in the official layer. If other services ask, choose a sign-up method without a phone number where you can.
- For two-factor authentication, use an authenticator app or a security key rather than SMS.
- Hide your number in messaging apps (Signal usernames, Telegram privacy settings; [chapter 5](05-data-brokers-and-lookup-apps.md)).

## 11.4 Phone and computer settings

- **Location:** Only for the apps that need it, only "while using", precise location off, location history off ([chapter 7](07-real-world-traces.md)).
- **Contacts, photos, microphone, camera permissions:** Review app by app. For photos, use "selected photos only".
- **Advertising ID:** Turn off tracking requests on iOS; delete the advertising ID on Android.
- **Wi-Fi and Bluetooth scanning:** Turn off background scanning used for location accuracy.
- **Lock screen:** Turn off notification previews.
- **Keyboard and AI features:** Review keyboard and assistant features that send what you type to the cloud.
- **Updates:** Keep the operating system and apps up to date; old devices leak.

## 11.5 Browser and search

- **Browser:** One that blocks tracking by default, such as Firefox (with uBlock Origin), Brave or Mullvad Browser.
- **Settings:** Block third-party cookies; clear cookies when the browser closes; don't save passwords or forms in the browser (use a password manager). Turn on Global Privacy Control where your browser supports it; in several US states, businesses must treat it as an opt-out of selling or sharing your data.
- **Separate profiles:** Separate browser profiles or Firefox containers for the official, everyday and anonymous layers. Never be logged in to accounts from two layers in the same profile.
- **Search engine:** One that doesn't profile your search history, such as DuckDuckGo, Startpage or Brave Search.
- **Don't use "Sign in with Google" buttons.** A separate email and password for each service.

## 11.6 Network: VPN and Tor

| | What it hides | What it doesn't |
|---|---|---|
| **VPN** | Your IP address from websites; your traffic from your internet provider | The VPN provider sees your traffic. Accounts you log in to still know who you are. |
| **Tor Browser** | Your IP address; who is visiting which site, from every point in the chain | It's slow, and some sites block it. If you log in under your own name, the point is lost. |

- If you choose a VPN, pick a paid provider that has been independently audited and has shown it doesn't keep logs. Free VPNs often make money by selling your data.
- Some countries block access to VPN and Tor sites from time to time; Tor's "bridges" exist for that. Know the rules where you live before you use them.
- Use encrypted DNS: "secure DNS" in your browser, "Private DNS" on Android.
- Use a VPN on public Wi-Fi.

## 11.7 Messaging

- **Signal:** End-to-end encrypted; disappearing messages; a username instead of your number.
- **WhatsApp:** End-to-end encrypted, but who you talk to and when (metadata) stays with the company. Encrypt backups (Settings > Chats > Chat backup > End-to-end encrypted backup).
- **Telegram:** Regular chats are not end-to-end encrypted; use "secret chats" for sensitive conversations.
- Make disappearing messages the default; clear old chats regularly.

## 11.8 Payments and shopping

- **Virtual cards:** Many banks and some services issue separate, limited, easily cancelled virtual card numbers. Don't use your main card online.
- **Cash:** Still the way to pay that leaves the least trace in the physical world.
- **Cryptocurrency is not anonymous:** exchanges require ID, and transactions are permanently public.
- **Deliveries:** Pickup points, parcel lockers or collection from the depot instead of your home address.
- **Loyalty cards and offers:** Every discount tied to your phone number links your shopping history to your identity. Ask whether it's really worth it.

## 11.9 Rules for sharing

If you still share things:

- No face, home, workplace, children, car or routines.
- Share locations later and vaguely ("at a beach last month"), never live.
- Look at the background: window views, door numbers, documents, reflections ([chapter 7](07-real-world-traces.md)).
- Strip location data from photos.
- On pseudonymous accounts, give no real-life details: job, city, school, birthday, pet's name.
- Your writing style is a fingerprint too; on a pseudonymous account, avoid phrases that identify you and long, personal texts.

## 11.10 The people around you

- Tell the people close to you your rules once, clearly: no tagging, no photos without asking, no locations, don't give my number or address to anyone.
- Give new acquaintances a phone number or Signal username instead of a social media handle; you don't owe anyone an explanation for not being findable on social media.
- At work: say up front that you don't want to appear on the company's website, social media or press releases.

## 11.11 Before opening a new account

1. Is it really necessary? Can you continue as a guest?
2. Which layer does it belong to? Use that layer's email and browser profile.
3. Are real name, phone, date of birth and address mandatory? If not, don't give them.
4. How hard is it to delete? (Check beforehand using the method in [chapter 3](03-deleting-accounts.md).)
5. Add it to your inventory.

## 11.12 Level 3: Clean break

If you want no digital link at all between your old identity and your new life:

- **New email and new number,** without a group announcement to your old circle; give them only to the people you want to keep, one at a time.
- **New devices:** Don't restore your old phone's backup onto the new one; don't carry over apps paired with old accounts or your whole address book. Add the contacts you need by hand.
- **Moving:** Give your new address only where required; use pickup points for parcels. If you use mail forwarding, know that it creates a lasting link between the old and new address.
- **No accounts shared with your old circle:** family plans, shared albums, old groups.
- **Change your routines:** The same gym, the same café, the same running route: traces deleted online can be rebuilt from your physical routine.
- **Name change:** The most extreme option. Most countries allow a change of name through a court or civil registry procedure; the rules and costs vary. Your old name stays in official records, but online searches for it will no longer find you. Ask a lawyer or your civil registry about the procedure where you live.
- **Legal obligations:** You still have to give your new contact details to the tax office, courts, creditors and other authorities that are entitled to them. Disappearing doesn't remove those obligations, and an address you fail to report can work against you.

## End-of-chapter checklist

- [ ] Official, everyday and anonymous layers separated
- [ ] An email alias service set up
- [ ] Phone and computer permissions reviewed
- [ ] Browser, search engine and DNS configured
- [ ] Disappearing messages and privacy settings on in messaging apps
- [ ] Using virtual cards and pickup points
- [ ] Sharing rules explained to the people close to me
