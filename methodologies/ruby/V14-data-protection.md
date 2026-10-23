# V14 – Data Protection (Rails)

> **ASVS 5.0 · Chapter V14** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V14-Data-Protection.md`](../_asvs-base/V14-Data-Protection.md).
> Where sensitive data flows, gets cached, and gets logged.

## V14.2 General data protection

#### 14.2.1 — No sensitive data in URL / query string · L1
- **Mechanism (Rails):** URLs/query strings land in `production.log`, proxy
  logs, Referer, and browser history. Tokens/PII belong in the body or headers.
- **How to test:** look for session tokens, reset tokens, API keys, PII in URL
  paths/query (`?token=...`, `?api_key=...`, `/reset/<token>`).
- **Positive (secure):** such data sent in POST body / `Authorization` header.
- **Negative (insecure):** sensitive value in the URL → logged/leaked (and, for
  reset tokens, cf. [V6.4.3](V06-authentication.md)).

#### 14.2.2 / 14.2.5 — No caching of sensitive data server-side · L2/L3
- **Mechanism (Rails):** fragment/action/HTTP caching (`caches_action`,
  `Rails.cache`, CDN) must not cache per-user sensitive responses. A shared
  cache keyed without the user → one user served another's cached page.
- **How to test:** request a sensitive authenticated page; inspect
  `Cache-Control`/`Age`/CDN hit headers; try fetching as another user.
- **Positive (secure):** `Cache-Control: private, no-store` on sensitive
  responses; cache keys include the user.
- **Negative (insecure):** sensitive response cached/shared (web cache
  deception also possible — [Web Cache Deception](../../upstream/PayloadsAllTheThings/Web%20Cache%20Deception/README.md)).

#### 14.2.6 — Return only minimum sensitive data · L3
- **Mechanism (Rails):** serializers mask/omit (last-4 of a card, no full
  SSN/`password_digest`). Overlaps over-serialization
  ([V15 §15.3.1](V15-secure-coding-and-architecture.md)).
- **Negative (insecure):** full PAN/SSN/token returned where a masked value
  suffices.

**14.2.3 (L2):** sensitive data not sent to third-party trackers/analytics.
**14.2.4 (L2):** sensitive-data logging controls (→ `filter_parameters`,
[V16.2.5](V16-security-logging-and-error-handling.md)). **14.2.7/14.2.8 (L3):**
retention/auto-deletion; strip metadata (EXIF/geo) from user files.

## V14.3 Client-side data protection

#### 14.3.2 — Anti-caching headers for sensitive responses · L2
- **Test:** `curl -sD- -b "$COOKIE" https://TARGET/account -o /dev/null | grep -i cache-control`
- **Positive (secure):** `Cache-Control: no-store` (or `no-cache, private`) on
  sensitive pages.
- **Negative (insecure):** cacheable → sensitive data persists in the browser/
  shared caches.

#### 14.3.3 — No sensitive data in browser storage · L2
- **Mechanism (Rails/JS):** the app's JS must not stash PII/tokens in
  `localStorage`/`IndexedDB` (session tokens excepted). Inspect client storage
  in the app's SPA/Turbo code.
- **Negative (insecure):** JWTs/PII in `localStorage` (XSS-exfiltratable).

**14.3.1 (L1):** authenticated data cleared from client storage on logout
(`Clear-Site-Data` header). **14.1.x (L2):** documented data classification and
per-level protection requirements.

---
*Covers ASVS V14.1–V14.3. Logging specifics: [V16](V16-security-logging-and-error-handling.md).*
