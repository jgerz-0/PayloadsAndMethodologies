# V15 – Secure Coding and Architecture (Rails)

> **ASVS 5.0 · Chapter V15** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V15-Secure-Coding-and-Architecture.md`](../_asvs-base/V15-Secure-Coding-and-Architecture.md).
> Dependency/CVE management, SSRF, mass assignment, over-serialization, HPP,
> type confusion, and safe concurrency. This chapter also carries the
> **known-CVE** checklist for the Rails stack.

## V15.2 Security architecture & dependencies

#### 15.2.1 — Components within remediation window (known CVEs) · L1
- **Mechanism (Rails):** pin Rails/Ruby/Rack/gems ([recon](README.md)), then:
  ```sh
  bundler-audit check --update        # Gemfile.lock vs rubysec advisory DB (authoritative)
  ```
- **Positive (secure):** `No vulnerabilities found`.
- **Negative (insecure):** advisories reported. High-impact Rails-stack CVEs to
  confirm and map to a working test:

  | CVE | Impact | Page |
  |---|---|---|
  | CVE-2013-0156 | Params YAML/symbol **RCE** (unauth) | [V1.5.2](V01-encoding-and-sanitization.md) |
  | CVE-2019-5418 | `render file:` Accept-header **arbitrary file read** | [V5](V05-file-handling.md) |
  | CVE-2019-5420 | Dev-mode predictable `secret_key_base` → **RCE** | [V7](V07-session-management.md) |
  | CVE-2020-8163 | Code injection via `render` locals → **RCE** | [V1.3.7](V01-encoding-and-sanitization.md) |
  | CVE-2020-8165 | Unmarshal via cache stores → **RCE** | [V1.5.2](V01-encoding-and-sanitization.md) |
  | CVE-2022-21831 | Active Storage transform **RCE** | [V5](V05-file-handling.md) |
  | CVE-2022-32224 | YAML serialized columns **RCE** | [V1.5.2](V01-encoding-and-sanitization.md) |
  | CVE-2023-22794 | ActiveRecord comment **SQLi** | [V1.2.4](V01-encoding-and-sanitization.md) |
  | CVE-2025-27610 | `Rack::Static` **LFI/path traversal** | [V5](V05-file-handling.md) |
  | Rack 2024 trio (CVE-2024-25126/26141/26146) | ReDoS / DoS | — |

  Gems with recurring CVEs: `nokogiri` (libxml XXE), `rails-html-sanitizer`/
  `loofah` (sanitizer-bypass XSS — [V1.3.1](V01-encoding-and-sanitization.md)),
  `devise`, `image_processing`/ImageMagick, EOL `paperclip`. Upstream
  [CVE Exploits](../../upstream/PayloadsAllTheThings/CVE%20Exploits/README.md).

#### 15.2.3 — Production excludes extraneous functionality · L2
- **Payload:** `/rails/info/*`, seed/sample/test endpoints, `/letter_opener`.
- **Positive/Negative:** as [V13.4.5](V13-configuration.md).

**15.2.4 (L3) dependency confusion:** gems resolve from the expected source
(Bundler `source` blocks, private gem server) — internal gem names must not be
claimable on rubygems.org. Upstream
[Dependency Confusion](../../upstream/PayloadsAllTheThings/Dependency%20Confusion/README.md).

## V15.3 Defensive coding

#### 15.3.1 — Return only the required subset of fields (ORM leak) · L1
- **Mechanism (Rails):** `render json: @user` / `@user.to_json` dumps **every**
  column (incl. `password_digest`, tokens, internal flags). Use `only:`/a
  serializer (AMS, jbuilder, blueprinter) allowlist.
- **How to test:** inspect JSON responses for fields the UI never shows.
- **Positive (secure):** only whitelisted fields present.
- **Negative (insecure):** full model dumped → sensitive fields leak. Upstream
  [ORM Leak](../../upstream/PayloadsAllTheThings/ORM%20Leak/README.md).

#### 15.3.2 — Backend calls don't follow redirects (SSRF) · L2
> Where the backend calls external URLs, don't follow redirects unless intended.

- **Mechanism (Rails):** outbound fetch of a user-supplied URL — `open-uri`
  `open`/`URI.open` (also `|cmd` RCE and `file://` read —
  [V1.2.5](V01-encoding-and-sanitization.md)), `Net::HTTP`, HTTParty, Faraday,
  `Down`, carrierwave `remote_<attr>_url`, MiniMagick/ImageMagick.
- **How to test:** point the fetch at OOB + internal + metadata; test redirect
  bounce.
- **Payload:** `http://<collab>.oastify.com/` · `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
  · `http://127.0.0.1:6379/` · `file:///etc/passwd` · `| id` · a 302 from your
  host → `169.254.169.254`.
- **Positive (secure):** scheme+host allowlist, IP checked at connect time
  against RFC1918/link-local/loopback, redirects not followed cross-host,
  ImageMagick `policy.xml` disabling `URL`/`MSL`/`MVG`.
- **Negative (insecure):** server makes the request / returns metadata creds /
  callback fires → SSRF (→ RCE for the `open "|"` sink). Upstream
  [SSRF](../../upstream/PayloadsAllTheThings/Server%20Side%20Request%20Forgery/README.md),
  [DNS Rebinding](../../upstream/PayloadsAllTheThings/DNS%20Rebinding/README.md).

#### 15.3.3 — Mass assignment defenses · L2
> Limit allowed fields per controller/action; can't insert/update fields the user shouldn't.

- **Mechanism (Rails):** strong parameters —
  `params.require(:user).permit(:name, :email)`. Findings: `permit!` (permits
  everything); a sensitive field in the allowlist (`role`, `admin`, `*_id`,
  `type` (STI), money/status); nested `accepts_nested_attributes_for`.
- **How to test:** add privileged fields to a create/update and re-fetch to
  confirm persistence.
- **Payload:** `PATCH /account {"user":{"name":"me","admin":true,"role":"admin","account_id":1}}`
- **Positive (secure):** extra fields ignored (filtered by `permit`); values
  unchanged.
- **Negative (insecure):** `admin`/`role`/`account_id` persists → privilege
  escalation / tenant hop. Upstream
  [Mass Assignment](../../upstream/PayloadsAllTheThings/Mass%20Assignment/README.md),
  [OWASP Mass Assignment Cheat Sheet](../../upstream/CheatSheetSeries/cheatsheets/Mass_Assignment_Cheat_Sheet.md).

#### 15.3.4 — Original client IP via trusted fields · L2
- **Mechanism (Rails):** `request.remote_ip` honours `X-Forwarded-For`; trust
  only known proxies (`config.action_dispatch.trusted_proxies`). Spoofable IP
  → bypass IP throttles/allowlists. Cf. [V4.1.3](V04-api-and-web-service.md).

#### 15.3.5 — Strict type / equality · L2
- **Mechanism (Rails):** avoid type-juggling via the param type-confusion
  (`?x[]=`, hash where scalar expected — [V2.2.1](V02-validation-and-business-logic.md));
  use `ActiveSupport::SecurityUtils.secure_compare` for secret comparison (also
  constant-time, [V11](V11-cryptography.md)), not `==`.
- Upstream [Type Juggling](../../upstream/PayloadsAllTheThings/Type%20Juggling/README.md).

#### 15.3.7 — HTTP parameter pollution · L2
- **Mechanism (Rails):** Rack merges duplicate params and query/body/path
  sources; last-wins/array coercion can bypass checks or smuggle values.
- **Payload:** `?role=user&role=admin` ; mix query and body params.
- **Positive/Negative:** per [HTTP Parameter Pollution](../../upstream/PayloadsAllTheThings/HTTP%20Parameter%20Pollution/README.md).

**15.3.6 (L2) prototype pollution:** JS concern — **N/A** to server Ruby; review
the app's JavaScript bundle ([Prototype Pollution](../../upstream/PayloadsAllTheThings/Prototype%20Pollution/README.md)).

## V15.4 Safe concurrency (L3)

**15.4.1–15.4.4:** thread-safety (Puma multi-thread), TOCTOU atomicity, lock
discipline, starvation. The exploitable projection is race conditions — tested
in [V2.3.4](V02-validation-and-business-logic.md) (parallel requests on
limited-resource / check-then-act flows). Confirm shared state (class vars,
memoized caches, files) is accessed thread-safely under Puma.

**15.1.x (L1/L2/L3):** documented remediation timeframes, SBOM inventory, and
flagged risky components / dangerous functionality.

---
*Covers ASVS V15.1–V15.4. Deserialization RCE: [V1.5.2](V01-encoding-and-sanitization.md).*
