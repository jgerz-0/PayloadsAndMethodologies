# V13 – Configuration (Rails)

> **ASVS 5.0 · Chapter V13** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V13-Configuration.md`](../_asvs-base/V13-Configuration.md).
> Secret management, backend-communication hardening, and (highest black-box
> yield) **unintended information leakage** — exposed `.git`, dev endpoints,
> configs, and the master-key/credentials secret hunt.

## V13.3 Secret management

#### 13.3.1 / 13.3.2 / 13.3.4 — Secret storage, least privilege, rotation · L2/L3
- **Mechanism (Rails):** secrets in `config/credentials.yml.enc` (encrypted by
  `config/master.key` / `RAILS_MASTER_KEY`), a vault, or ENV — **never in git**.
  `secret_key_base` is the crown jewel (session forgery + `:marshal` RCE — see
  [V7](V07-session-management.md)/[V11](V11-cryptography.md)).
- **How to test:**
  ```sh
  git log --all --oneline -- config/master.key config/secrets.yml .env
  git log -p --all | grep -iE 'secret_key_base|master.key|password|api_key' | head
  trufflehog git file://. ; gitleaks detect
  ```
- **Positive (secure):** keys only in deploy secrets/vault; never committed;
  rotated on exposure.
- **Negative (insecure):** `master.key`/`secret_key_base`/`.env` in git history
  or build artifacts → decrypt `credentials.yml.enc` offline
  (`RAILS_MASTER_KEY=... bin/rails credentials:show`) → DB creds, API keys,
  session forgery. Upstream
  [Insecure Source Code Management](../../upstream/PayloadsAllTheThings/Insecure%20Source%20Code%20Management/README.md),
  [API Key Leaks](../../upstream/PayloadsAllTheThings/API%20Key%20Leaks/README.md).

## V13.4 Unintended information leakage

#### 13.4.1 — No source-control metadata (.git/.svn) · L1
- **Payload:** `curl -s https://TARGET/.git/config` ; `/.git/HEAD`
- **Positive (secure):** `404`.
- **Negative (insecure):** `.git/` served → dump the repo (`git-dumper`) →
  source + secrets.

#### 13.4.2 — Debug modes off in production · L2
- **Mechanism (Rails):** `config.consider_all_requests_local = false` and
  `RAILS_ENV=production`; no `web-console`/`better_errors` in the prod bundle
  (the RCE case — [V16.5.1](V16-security-logging-and-error-handling.md)).
- **Payload:** force an exception (bad type in a path, malformed JSON body).
- **Positive (secure):** generic static 500 page.
- **Negative (insecure):** full Rails exception page (stack trace, source,
  params, env) or an interactive console.

#### 13.4.5 / 13.4.6 — Dev/monitoring endpoints & version info not exposed · L2/L3
- **Payload:** `/rails/info/routes`, `/rails/info/properties`, `/sidekiq`,
  `/blazer`, `/flipper`, `/pghero`, `/letter_opener`.
- **Positive (secure):** `404`, or mounted engines behind an `authenticate`/
  `constraints` block.
- **Negative (insecure):** route map / exact Rails+Ruby version / unauth admin
  engine exposed. Upstream
  [Insecure Management Interface](../../upstream/PayloadsAllTheThings/Insecure%20Management%20Interface/README.md).

**13.4.3 (L2)** no directory listing; **13.4.4 (L2)** HTTP TRACE disabled;
**13.4.7 (L3)** serve only specific file extensions (no `.rb`/`.yml`/`.erb`
source leak).

## V13.2 Backend communication

- **13.2.3 (L2) no default credentials:** DB/Redis/service accounts not
  `root/root`, `admin/admin`, or blank (`config/database.yml`,
  `postgres`/`redis` with no password).
- **13.2.4 / 13.2.5 (L2) outbound allowlist:** the app/server restricts which
  external hosts it may call (anti-SSRF defence in depth — see
  [V15 §15.3.2](V15-secure-coding-and-architecture.md)).
- **13.2.1 / 13.2.2 (L2):** backend components use least-privilege accounts and
  authenticated channels.

## Host authorization (`config.hosts`)

- **Mechanism (Rails):** `ActionDispatch::HostAuthorization` blocks requests
  whose `Host` isn't in `config.hosts` — defends host-header poisoning and DNS
  rebinding. **`config.hosts.clear`** disables it.
- **Payload:** `-H 'Host: evil.example'` / `-H 'X-Forwarded-Host: evil.example'`
- **Positive (secure):** `403 Blocked hosts` for an arbitrary Host.
- **Negative (insecure):** `200` with the arbitrary Host reflected into
  generated URLs/emails → poisoning (reset links — [V6.4.3](V06-authentication.md)),
  cache poisoning, rebinding SSRF.

**13.1.x (L2/L3):** documentation of communication needs, connection/resource
limits, and secret-rotation schedule.

---
*Covers ASVS V13.1–V13.4. Crypto strength of the secrets: [V11](V11-cryptography.md).*
