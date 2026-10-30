# Appendix C. Tools (optional)

Every step in the guide can be done by hand. The `diedigital` command-line tool in this repository only speeds up the long, repetitive parts: the account inventory, finding accounts in your mailbox, footprint checks, preparing and sending deletion requests in bulk, bulk-deleting GitHub/Reddit/Mastodon content, and the dead man's switch.

Python 3.10 or later; no other dependencies.

```bash
git clone https://github.com/gorkemguler/DieDigital.git
cd DieDigital
python3 -m diedigital --help

# Or install it as a command:
pip install .
diedigital --help
```

Wherever you see `diedigital` below, `python3 -m diedigital` works too.

> **Language:** Commands and options are in English, but the tool's messages are currently in Turkish. The letter templates include English GDPR versions (`gdpr-erasure`, `gdpr-reminder`, `archive-removal`, `data-broker-suppression`), which are chosen automatically for any account whose `jurisdiction` isn't `tr`; sales data platforms such as Apollo or ZoomInfo get `data-broker-suppression`.

Every command that deletes runs in **dry-run mode** by default. Real changes need `--execute` (requests and wipe tools) or `--armed` / `DEADMAN_ARMED=true` (dead man's switch).

## Files

| File | Contents | In git |
|---|---|---|
| `profile.json` | Name, email, address, phone; used in requests | `.gitignore` |
| `accounts.json` | Account inventory | `.gitignore` (`git add -f` in a private repository) |
| `deadman.json` | Dead man's switch configuration | committed in a private repository |
| `.deadman/state.json` | Last check-in, warnings, action progress | committed in a private repository |

Examples: `examples/profile.example.json`, `examples/accounts.example.json`, `diedigital/data/deadman.example.json`.

To change file paths: `diedigital --inventory other.json --profile other-profile.json ...` or the `DIEDIGITAL_INVENTORY` and `DIEDIGITAL_PROFILE` environment variables.

## Commands

### catalog

```bash
diedigital catalog                 # every known service
diedigital catalog instagram       # deletion/export link, waiting period, notes
diedigital catalog data-broker     # by category
```

The catalog lives in `diedigital/data/services.json`. If you spot a missing or outdated link, update it there.

### inventory

```bash
diedigital inventory import passwords.csv          # password manager export; passwords are never read
diedigital inventory add "Service" --url ... --username ... --email ... \
    --privacy-email privacy@... --jurisdiction eu --notes ...
diedigital inventory list [--status active]
diedigital inventory set <#id|name> <status> [--note ...] [--privacy-email ...]
diedigital inventory report [--out inventory.md]
diedigital inventory overdue [--days 30]
```

Statuses: `active`, `exported`, `wiped`, `requested`, `deleted`, `blocked`. Jurisdiction: `tr` (Turkish KVKK template), `eu` or `other` (English GDPR template).

### discover

```bash
IMAP_PASSWORD=... diedigital discover imap --host imap.gmail.com --user you@gmail.com \
    [--since 2015-01-01] [--folder INBOX] [--all] [--add]
```

Looks for sign-up, verification and password-reset messages in email headers and scores sender domains. `--add` adds what it finds to the inventory.

### footprint

```bash
diedigital footprint username old_handle [--all]
diedigital footprint email you@example.com [--add]     # Gravatar; breaches if HIBP_API_KEY is set
diedigital footprint dorks --name "First Last" --email ... --username ... --phone ... --city ... --out searches.md
```

### letters

```bash
diedigital letters list
diedigital letters render --account <id> [--template ...] [--reminder] [--out letter.txt]
diedigital letters render --service "Company" --template gdpr-erasure
diedigital letters render --template archive-removal --url ... --url ...
diedigital letters send --account <id> [--to address] [--reminder] --execute
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
diedigital deadman init        # deadman.json + state file
diedigital deadman status      # time remaining, status of each action
diedigital deadman checkin     # reset the timer (stops remaining actions if triggered)
diedigital deadman preflight   # test tokens and passwords
diedigital deadman dry-run     # run as if triggered, delete nothing
diedigital deadman run [--armed]   # what cron / GitHub Actions calls
```

Details: [chapter 10](10-dead-mans-switch.md).

## Getting credentials

**GitHub (`GH_WIPE_TOKEN`):** Settings > Developer settings > Personal access tokens > Tokens (classic) > Generate new token. Scopes: `repo`, `delete_repo`, `gist`, `user`. If you'll use it in the dead man's switch, give it a long expiry.

**Reddit (`REDDIT_*`):**

1. https://www.reddit.com/prefs/apps > "create another app" > type: **script**, redirect uri: `http://localhost:8080`
2. The short code under the app name is `REDDIT_CLIENT_ID`, the "secret" is `REDDIT_CLIENT_SECRET`; your username and password go in `REDDIT_USERNAME` and `REDDIT_PASSWORD`.
3. If two-factor authentication is on, password login with script apps may not work; you may need to turn it off temporarily while the wipe runs.
4. For content older than the ~1,000 most recent items, request your data at https://www.reddit.com/settings/data-request and pass `comments.csv` and `posts.csv` from the archive with `--ids-file`.

**Mastodon (`MASTODON_TOKEN`):** Preferences > Development > New application; the `read` and `write:statuses` scopes are enough. Mastodon rate-limits deletions (by default 30 posts per 30 minutes); large accounts take hours.

**SMTP:** For Gmail, turn on two-step verification and create an app password under Google Account > Security > App passwords: `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_USER=your address`, `SMTP_PASSWORD=app password`.

**IMAP:** The same app password for Gmail, with `--host imap.gmail.com`. Yandex: `imap.yandex.com` (enable IMAP under Settings > Email clients). Microsoft has largely turned off password-based IMAP login for personal accounts.

## Environment variables

| Variable | Used by |
|---|---|
| `SMTP_HOST`, `SMTP_PORT` (587), `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` | requests, notifications. Port 465 uses SSL, anything else STARTTLS. |
| `IMAP_PASSWORD` | `discover imap` |
| `HIBP_API_KEY` | `footprint email` |
| `GH_WIPE_TOKEN` | `wipe github`, `self_destruct` |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` | `wipe reddit` |
| `MASTODON_TOKEN` | `wipe mastodon` |
| `DIEDIGITAL_PROFILE_JSON` | instead of `profile.json` (as a GitHub secret) |
| `DIEDIGITAL_TEMPLATES` | an extra template folder |
| `DEADMAN_ARMED` | if `true`, the dead man's switch really deletes |
| `DEADMAN_WEBHOOK_URL` | notification webhook (ntfy, Discord, Slack) |

## Tests

```bash
python3 -m unittest discover -s tests -v
```
