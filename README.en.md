# DieDigital

**A complete guide to disappearing from the internet.**

[Türkçe](README.md) · English

From finding every account you've ever opened to closing your last email address; from dropping out of search engines to blurring your home in Street View; from photos your friends posted to the data companies hold about you: how to erase your traces step by step, and how to live without leaving new ones. If you want, you can finish by setting up a **dead man's switch** that deletes whatever is left at a time you choose.

No technical knowledge needed; every step can be done by hand. Laws and services in the EU/UK, the US and Turkey are covered, with a general method for everywhere else.

## Where to start

1. Read [**Getting started**](docs/en/00-getting-started.md): choose how far you want to disappear (invisible / accountless / clean break) and think about who you're hiding from.
2. If you're hiding from a specific person, read [**Stalking, harassment, abuse**](docs/en/12-stalking-harassment-abuse.md) first.
3. Copy the [**checklist**](docs/en/appendix-a-checklist.md) and work through the chapters in order.

## The guide

| # | Chapter | What |
|---|---|---|
| 0 | [Getting started](docs/en/00-getting-started.md) | Levels, who you're hiding from, what can't be deleted, ground rules, roadmap |
| 1 | [Inventory and backup](docs/en/01-inventory-and-backup.md) | Stop creating traces, find forgotten accounts, download your data |
| 2 | [Content cleanup](docs/en/02-content-cleanup.md) | Posts, photos, comments, reviews; platform by platform |
| 3 | [Deleting accounts](docs/en/03-deleting-accounts.md) | Major platforms, local services, marketing opt-outs, orphaned accounts |
| 4 | [Search engines and archives](docs/en/04-search-engines-and-archives.md) | What to search for, Google/Bing/Yandex removal tools, the Wayback Machine, legal routes |
| 5 | [Data brokers and lookup apps](docs/en/05-data-brokers-and-lookup-apps.md) | People-search sites, caller-ID apps, uploaded address books, face search |
| 6 | [Traces held by others](docs/en/06-traces-held-by-others.md) | Friends, family, work, school, events, news, Wikipedia, family trees |
| 7 | [Real-world traces](docs/en/07-real-world-traces.md) | Address, Street View, location, Wi-Fi, smart devices, health, DNA, plates |
| 8 | [Legal rights](docs/en/08-legal-rights.md) | GDPR, UK GDPR, US state laws, KVKK; deletion requests step by step, complaints |
| 9 | [Final steps](docs/en/09-final-steps.md) | Domain, email, phone, cloud, devices, money |
| 10 | [Dead man's switch](docs/en/10-dead-mans-switch.md) | Platforms' own switches, scheduled requests, a digital executor, an automatic switch |
| 11 | [Living invisibly](docs/en/11-living-invisibly.md) | Identity layers, email aliases, devices, browser, VPN/Tor, payments, a clean break |
| 12 | [Stalking, harassment, abuse](docs/en/12-stalking-harassment-abuse.md) | If someone is looking for you: evidence first, then safety, then deletion |
| 13 | [Monitoring and maintenance](docs/en/13-monitoring-and-maintenance.md) | Making sure deleted things stay deleted |
| A | [Checklist](docs/en/appendix-a-checklist.md) | The whole guide as a checklist |
| B | [Letter and message templates](docs/en/appendix-b-letter-templates.md) | GDPR, CCPA, complaints, search engines, news sites, polite requests |
| C | [Tools](docs/en/appendix-c-tools.md) | Optional command-line tools |

## Realistic expectations

Zero trace is not possible: public records, records with legal retention periods, what's on other people's devices, and data breaches don't get deleted. The goal of this guide is: **you don't come up in searches, you're deleted everywhere you know of, you've made a formal request wherever deletion wasn't possible, and you stop creating new traces.**

## Optional tools

The repository includes a dependency-free Python tool (Python 3.10+) to speed up the long parts. You don't need it to follow the guide.

```bash
git clone https://github.com/gorkemguler/DieDigital.git && cd DieDigital
python3 -m diedigital --help
```

| Command | What it does |
|---|---|
| `inventory` | Account inventory; import from a password manager CSV (passwords are never read); checklist report |
| `discover imap` | Finds forgotten accounts from "welcome / verify" emails in your mailbox |
| `footprint` | Username checks, Gravatar and breach checks, a search engine checklist |
| `catalog` | Deletion and export links for known services, waiting periods |
| `letters` | Fills in GDPR / KVKK requests and sends them by email; reminders |
| `wipe` | Bulk-deletes GitHub, Reddit and Mastodon content |
| `deadman` | Dead man's switch: warns you, triggers, runs actions in order, deletes its own repository last |

Every command that deletes runs in dry-run mode by default. The tool's messages are currently in Turkish. Details: [Appendix C](docs/en/appendix-c-tools.md).

## Contributing

Deletion links and menu names change often. If you spot outdated information or a missing service, open a PR updating the relevant chapter or [`diedigital/data/services.json`](diedigital/data/services.json).

## Disclaimer

This guide is not legal advice, and it is not a guide to escaping legal obligations. Deleted accounts and data don't come back; back up first and read what each step does before you take it.

License: MIT
