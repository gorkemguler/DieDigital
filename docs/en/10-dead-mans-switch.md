# 10. Dead man's switch: deleted automatically when the time comes

A dead man's switch carries out the remaining deletions for you if you don't say "I'm still here" (check in) for a set period, or when a date you chose arrives. It's useful for three things:

- **Planned disappearance:** deciding "everything goes on this date" and getting on with your life until then.
- **Death or serious illness:** preventing your accounts from staying open for years, being taken over, or being used by others while you're gone.
- **A safety net:** making sure legal requests still go out to the places you couldn't delete by hand, forgot, or that never answered.

Set it up in layers; if one fails, the others still work. None of them requires coding; only the third layer needs some setup at a computer.

## Layer 1: The platforms' own switches

These run on the companies' own servers, need no setup beyond a setting, and keep working even if the other layers fail.

| Service | Setting | What it does |
|---|---|---|
| Google | [Inactive Account Manager](https://myaccount.google.com/inactive) | After 3-18 months of inactivity, notifies people you choose and, if you want, deletes the account entirely. |
| Telegram | Settings > Privacy and Security > "If away for" | Deletes the account with all messages if you don't log in for the period you set. |
| Facebook | Settings > Memorialisation settings | You can choose to have the account deleted rather than memorialised when your death is reported. |
| Mastodon | Preferences > Automated post deletion | Continuously deletes posts older than a set age. |
| Apple | Settings > [your name] > Sign-In & Security > Legacy Contact | Doesn't delete; gives a person you choose access to your data after your death. That person can then close the account. |

Google and Microsoft may also delete personal accounts that haven't been used for two years, under their own policies. Treat that as an extra possibility, not a guarantee.

## Layer 2: Methods without tools

### Scheduled emails (fixed date)

Gmail's "Schedule send" and Outlook's "Delay delivery" let you schedule emails for a future date.

1. Fill in the deletion request from [Appendix B](appendix-b-letter-templates.md) for every company you haven't been able to delete yet, or whose deletion you're leaving until that date.
2. Schedule each one from the registered email address for the same future date.
3. Schedule messages to people you trust as well (goodbyes, instructions).

Limits: there's no check-in, so if you change your mind you must cancel the scheduled emails yourself. If your email account is deleted before that date (for example because Inactive Account Manager triggers earlier), the emails won't go out; order things accordingly: scheduled emails first, then the deletion of the account.

### A person you trust (digital executor)

Leave a sealed envelope or an encrypted document with someone:

- The list of accounts you want deleted and how to delete them (the relevant chapters of this guide)
- When to act (your death, a specific date, not hearing from you for a set period)
- Rather than handing over passwords, ask them to use the platforms' **deceased user** processes. Google, Facebook, Instagram, LinkedIn, X and Apple all have forms that let family members request closure of an account with a death certificate; search the help pages for "deceased".
- Password managers' **emergency access** features (Bitwarden Emergency Access, for example) give a trusted person access after a waiting period you set, unless you decline within that period. That is a dead man's switch in itself.

### Third-party dead man's switch services

There are online services that send pre-written emails if you stop checking in. If you use one, don't put passwords or identity details in it, only instructions and request texts, and remember that the service itself might shut down.

## Layer 3: The DieDigital dead man's switch

The tool in this repository is a switch that runs daily on GitHub Actions or your own server, triggers on a missed check-in or a fixed date, and as its last act deletes its own repository.

> The tool's messages and the warning emails it sends are currently in Turkish. Commands, options and the configuration file are in English, and the English GDPR templates work as-is.

### What it can do

| Action | What it does |
|---|---|
| `send_letters` | Sends a deletion request to every still-open account in your inventory that has a `privacy_email` (a reminder to those you've already written to). This is the real power for anything without an API, like Facebook: it starts the company's legal deletion obligation. |
| `github_wipe` | Deletes GitHub repositories and gists, clears your profile. |
| `reddit_wipe` | Overwrites and deletes Reddit comments and posts. |
| `mastodon_wipe` | Deletes Mastodon posts. |
| `email` | A free-form email: a note to someone you trust, instructions to a lawyer, and so on. |
| `command` | Any command: `rclone purge`, your own script, another API. |
| `self_destruct` | Deletes this repository, last of all. |

**What it can't do:** Closing accounts on services like Facebook, Instagram or LinkedIn requires a browser login, verification codes and captchas; there's no reliable way to automate that. Either close those accounts **beforehand** yourself, or make sure `send_letters` sends a legal request when the switch triggers.

### Timeline

```
last check-in ──── checkin_interval_days ────▶ warnings ── grace_days ──▶ TRIGGER
                                               (every warn_every_hours)     │
                                                                            ├─▶ actions in order
                                                                            │   (unfinished ones resume next day)
                                                                            └─▶ self_destruct after delay_days
```

- **Check-in mode:** `checkin_interval_days: 30, grace_days: 7` → if you don't check in for 30 days the warnings start; 7 more days without a check-in and it triggers.
- **Fixed-date mode:** `"trigger_at": "2027-06-01T09:00:00Z"` → triggers on that date; warnings start 7 days before. Checking in doesn't postpone a fixed date; edit the file to postpone it.
- If you use both, whichever comes first triggers.

### Safety locks

- **Nothing is deleted unless armed.** Without `DEADMAN_ARMED=true` (a repository variable on GitHub) or `--armed`, a trigger only reports what it would do and notifies you.
- **Warning period:** For `grace_days` before the trigger you get a daily email (and a phone notification if you set one up).
- **You can stop it even after it triggers:** A check-in stops the actions that haven't run yet. Completed ones can't be undone.
- **If the state file is lost** the timer starts over; it never triggers early.
- **`self_destruct`** only runs after every other action has finished (or been retried `max_attempts` times and given up).
- **Weekly preflight:** Every week it tests all tokens and passwords and warns you if something has expired. No "invalid token" surprise on the day.

## Setup: GitHub Actions

The easiest way to have it run while your computer is off.

### 1. Create a private copy

**Don't fork**: a fork of a public repository is public, and scheduled workflows are disabled on forks.

```bash
# Create a new PRIVATE repository on GitHub (e.g. vanish), then:
git clone https://github.com/gorkemguler/DieDigital.git vanish
cd vanish
git remote set-url origin https://github.com/YOUR_USERNAME/vanish.git
git push -u origin HEAD:main
```

Tip: If you keep this repository in a separate GitHub account rather than your main one, deleting your main account by hand at the very end won't break the switch. The token `github_wipe` uses should belong to your main account.

### 2. Configure

```bash
python3 -m diedigital deadman init      # creates deadman.json and .deadman/state.json
```

Edit `deadman.json`: periods, your notification address, actions. Set `"enabled": false` on actions you don't use.

If you use `send_letters`, add your inventory to the repository (`.gitignore` normally blocks it; we force it because the repository is private):

```bash
git add -f accounts.json
```

### 3. Add secrets

Repository > Settings > Secrets and variables > Actions > **New repository secret**:

| Secret | Required? | Value |
|---|---|---|
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` | Yes, for notifications and requests | Gmail: `smtp.gmail.com`, `587`, your address, an app password |
| `DIEDIGITAL_PROFILE_JSON` | For `send_letters` | The full contents of `profile.json` |
| `GH_WIPE_TOKEN` | For `github_wipe` / `self_destruct` | Classic token with `repo`, `delete_repo`, `gist`, `user` scopes. Give it a long expiry; preflight warns you before it runs out. |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USERNAME`, `REDDIT_PASSWORD` | For `reddit_wipe` | [Appendix C](appendix-c-tools.md) |
| `MASTODON_TOKEN` | For `mastodon_wipe` | [Appendix C](appendix-c-tools.md) |
| `DEADMAN_WEBHOOK_URL` | Optional | Phone notification, e.g. `https://ntfy.sh/a-long-random-topic-name` (subscribe to the same topic in the ntfy app) |

Requests should come from the email address registered with each service ([chapter 8](08-legal-rights.md)). If different services were opened with different addresses, give the SMTP details of the one used most.

### 4. Push and test

```bash
git add deadman.json .deadman/state.json
git commit -m "dead man's switch"
git push
```

On GitHub: **Actions > deadman > Run workflow**

1. `preflight` → every line should say OK ("tamam").
2. `dry-run` → runs every action as if triggered without deleting anything; the log shows what would be deleted.
3. `status` → time remaining.

### 5. Arm it

Settings > Secrets and variables > Actions > **Variables** > New repository variable: `DEADMAN_ARMED` = `true`

From now on, a trigger really deletes.

### 6. Check in

**Actions > deadman > Run workflow > checkin.** You can do it from the GitHub mobile app too (repository > Actions > deadman > ⋯ > Run workflow). Put a reminder in your calendar.

From a computer: `python3 -m diedigital deadman checkin`, then commit and push `.deadman/state.json`.

### Things to know

- **The 60-day rule:** GitHub disables scheduled workflows in public repositories after 60 days without activity. The switch normally creates activity by recording its weekly preflight in the repository, but check the Actions tab now and then, and consider keeping `checkin_interval_days + grace_days` under 60 days.
- **Minutes quota:** Private repositories on the free plan have a monthly Actions minutes limit. The daily check takes under a minute; long jobs on trigger day are capped by `max_runtime_minutes` (default 120) and the rest carries over to the next day.
- **Anyone with write access** can run workflows that use the secrets. Don't add collaborators.
- A deleted repository can be restored by its owner for up to 90 days; secrets are deleted with it.
- **Illness, accident, a long trip:** The switch can't tell "dead" from "unreachable". Choose the periods with that in mind.

## Setup: your own server (cron)

If you'd rather not use GitHub, on a VPS or an always-on machine:

```bash
# /opt/vanish/.env  (chmod 600)
DEADMAN_ARMED=true
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=you@example.com
SMTP_PASSWORD=...
GH_WIPE_TOKEN=...
```

```cron
23 6 * * * cd /opt/vanish && set -a && . ./.env && set +a && python3 -m diedigital deadman run >> deadman.log 2>&1
```

Check in: `ssh server 'cd /opt/vanish && python3 -m diedigital deadman checkin'`

Here `self_destruct` may not make sense (there's no GitHub repository to delete); drop it and use a `command` action that deletes the files on the server instead.

## Configuration reference

| Field | Default | Description |
|---|---|---|
| `checkin_interval_days` | - | Days allowed without a check-in |
| `trigger_at` | - | Fixed trigger time (ISO 8601, UTC) |
| `grace_days` | 7 | Warning period before the trigger |
| `warn_every_hours` | 24 | Warning frequency |
| `preflight_every_days` | 7 | Preflight frequency |
| `max_runtime_minutes` | 120 | Time budget for actions in one run |
| `notify.emails` | [] | Where warnings go |
| `notify.webhook_env` | `DEADMAN_WEBHOOK_URL` | Environment variable holding the webhook URL |
| `notify.webhook_format` | `text` | `text` (ntfy), `discord`, `slack` |
| `state_file` | `.deadman/state.json` | State file |

Fields common to every action:

| Field | Description |
|---|---|
| `id` | A unique name. Set it, so progress isn't lost if you reorder actions. |
| `type` | Action type |
| `enabled` | Ignored if `false` |
| `delay_days` | How many days after the trigger to run (e.g. delete email 40 days later so replies to requests can arrive) |
| `max_attempts` | How many days to retry on failure (default 7) |
| `stop_on_error` | Don't continue to later actions if this one fails |
| `force` | `self_destruct` only: don't wait for the others |

Action-specific fields:

```jsonc
{"type": "send_letters", "inventory": "accounts.json", "template": null,
 "statuses": ["active", "exported", "wiped", "requested"], "profile": "profile.json"}

{"type": "github_wipe", "include": ["*"], "exclude": ["keep-*"], "repos": true, "gists": true,
 "scrub_profile": true, "token_env": "GH_WIPE_TOKEN"}

{"type": "reddit_wipe", "kinds": ["comments", "submitted"], "overwrite": true, "overwrite_text": ".",
 "ids_files": [{"path": "reddit/comments.csv", "kind": "comment"}], "pause_seconds": 1}

{"type": "mastodon_wipe", "instance": "https://mastodon.social", "keep_pinned": false,
 "older_than_days": null, "token_env": "MASTODON_TOKEN"}

{"type": "email", "to": ["someone@example.com"], "subject": "...", "body": "...", "body_file": null}

{"type": "command", "argv": ["rclone", "purge", "gdrive:"], "timeout_minutes": 60}

{"type": "self_destruct", "repo": null, "delay_days": 1, "token_env": "GH_WIPE_TOKEN"}
```

To set the language of the requests `send_letters` sends, give each account in `accounts.json` a `jurisdiction`: `tr` uses the Turkish KVKK template, anything else the English GDPR template. You can also force one with `"template": "gdpr-erasure"`.

If you use `ids_files` for `reddit_wipe`, add the CSV files from your Reddit data export with `git add -f`.
