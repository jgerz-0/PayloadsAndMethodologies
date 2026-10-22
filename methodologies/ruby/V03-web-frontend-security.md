# V3 – Web Frontend Security (Rails)

> **ASVS 5.0 · Chapter V3** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V03-Web-Frontend-Security.md`](../_asvs-base/V03-Web-Frontend-Security.md).
> Cookie attributes, browser security headers (HSTS/CSP/CORS/nosniff/frame),
> origin separation, and safe redirects. Most are observable directly on the
> wire: `curl -sD- https://TARGET/ -o /dev/null`.

## V3.3 Cookie setup

#### 3.3.1 Secure · 3.3.4 HttpOnly · 3.3.2 SameSite · 3.3.3 `__Host-` prefix
- **Mechanism (Rails):** session cookie flags come from
  `config.force_ssl` (sets `Secure`), the cookie store (`HttpOnly` on by
  default), and `config.action_dispatch.cookies_same_site_protection` (`:lax`
  default since 6.1). Rails does not use `__Host-`/`__Secure-` name prefixes by
  default.
- **How to test:** `curl -sD- https://TARGET/ -o /dev/null | grep -i set-cookie`
- **Positive (secure):** `Set-Cookie: _app_session=...; path=/; secure; HttpOnly; SameSite=Lax`
- **Negative (insecure):** missing `Secure` (session rides plaintext on
  downgrade), missing `HttpOnly` (JS-readable → XSS theft), or `SameSite=None`
  without cause (CSRF exposure — see the CSRF block in
  [V3.5](#v35-browser-origin-separation) below).

**3.3.5 (L3):** combined cookie name+value > 4096 bytes won't be stored by the
browser (silent session loss) — check large signed/encrypted cookies.

## V3.4 Browser security headers

#### 3.4.1 — HSTS · L1
- **Mechanism:** `config.force_ssl = true` emits `Strict-Transport-Security`.
- **Test:** `curl -sD- https://TARGET/ -o /dev/null | grep -i strict-transport`
- **Positive:** `Strict-Transport-Security: max-age=31536000; includeSubDomains`
  (≥ 1 year).
- **Negative:** header absent, or `max-age` short/zero.

#### 3.4.2 — CORS ACAO fixed / validated · L1
- **Mechanism (Rails):** `rack-cors` (`config/initializers/cors.rb`). Dangerous:
  a block that **reflects** the request `Origin` while setting
  `Access-Control-Allow-Credentials: true`.
- **Payload:** `-H 'Origin: https://evil.example'`
- **Positive (secure):** `Access-Control-Allow-Origin` is a fixed allowlisted
  value (or the request Origin is rejected).
- **Negative (insecure):** `Access-Control-Allow-Origin: https://evil.example`
  + `...-Credentials: true` → cross-origin credentialed read. Upstream
  [CORS Misconfiguration](../../upstream/PayloadsAllTheThings/CORS%20Misconfiguration/README.md).

#### 3.4.3 — Content-Security-Policy · L2 · 3.4.6 frame-ancestors · 3.4.7 report-uri · 3.4.8 COOP
- **Mechanism (Rails):** `config/initializers/content_security_policy.rb`
  (`policy.default_src`, per-request nonce via
  `content_security_policy_nonce_generator`). `frame-ancestors`/
  `X-Frame-Options` → clickjacking defence.
- **Test:** `curl -sD- https://TARGET/ -o /dev/null | grep -iE 'content-security|x-frame'`
- **Positive:** strict CSP with nonces, no `unsafe-inline`/`unsafe-eval`;
  `frame-ancestors 'self'` (or `X-Frame-Options: SAMEORIGIN`).
- **Negative:** no CSP (no XSS defence-in-depth), `unsafe-inline` present, or no
  framing control → clickjacking. Upstream
  [Clickjacking](../../upstream/PayloadsAllTheThings/Clickjacking/README.md).

#### 3.4.4 — `X-Content-Type-Options: nosniff` · L2 · 3.4.5 Referrer-Policy
- **Test:** `curl -sD- ... | grep -iE 'x-content-type-options|referrer-policy'`
- **Positive:** `X-Content-Type-Options: nosniff` on all responses;
  `Referrer-Policy: strict-origin-when-cross-origin` or tighter.
- **Negative:** missing `nosniff` (MIME-sniffing → stored XSS on uploads, cf.
  [V5](V05-file-handling.md)); permissive/absent referrer policy leaks URLs.

## V3.2 Unintended content interpretation

#### 3.2.1 — Response context / MIME · L1
- **Mechanism (Rails):** correct `Content-Type` on API/JSON and user-file
  responses + `nosniff` so a browser doesn't render an API/upload as HTML.
- **Payload:** request a stored user string with `Accept: text/html`; upload an
  HTML/SVG file and fetch it.
- **Positive (secure):** served as `application/json`/`text/plain` or
  `Content-Disposition: attachment`; not rendered as HTML.
- **Negative (insecure):** `text/html` + inline rendering → stored XSS.

**3.2.2 / 3.2.3 (client-side JS, DOM clobbering, L1/L3):** frontend-JS concerns
(use `textContent` not `innerHTML`; explicit var declarations). Relevant to the
app's JS/Turbo/Stimulus/React code, not Rails server rendering — review the
asset bundle; see upstream [DOM Clobbering](../../upstream/PayloadsAllTheThings/DOM%20Clobbering/README.md).

## V3.5 Browser origin separation

- **3.5.3 (L1) safe HTTP methods:** state-changing actions must use
  POST/PUT/PATCH/DELETE, not GET. Test for `GET /account/delete`-style
  state-changing GETs (also defeats CSRF tokens).
#### 3.5.1 / 3.5.2 — CSRF / cross-origin request forgery · L1
> Cross-origin requests to sensitive functionality are validated (not possible without a valid token/preflight).

- **Mechanism (Rails):** `protect_from_forgery with: :exception` (default in
  `ApplicationController`) validates `authenticity_token` on every non-GET; a
  bad/missing token → **HTTP 422**. `SameSite=Lax` (default) is a second layer.
  Findings: `skip_before_action :verify_authenticity_token` on a
  cookie-authenticated controller; `protect_from_forgery with: :null_session`
  where the action still works; `ActionController::API` (no CSRF) that also
  accepts the session cookie.
- **How to test:** replay a state-changing request with the session cookie but
  **no** `authenticity_token`/`X-CSRF-Token`.
- **Payload:** `curl -b "$COOKIE" -X POST -d "user[email]=attacker@evil.com" https://TARGET/account`
- **Positive (secure):** `422 Unprocessable Entity` (`InvalidAuthenticityToken`);
  change not applied.
- **Negative (insecure):** `2xx`/`302` and the change persists → CSRF. Then
  confirm cross-site (cookie must be sent cross-site; check `SameSite`).
  Upstream [Cross-Site Request Forgery](../../upstream/PayloadsAllTheThings/Cross-Site%20Request%20Forgery/README.md).
- **3.5.4 (L2):** separate apps on separate hostnames (user-content domain,
  admin domain) for same-origin isolation.
- **3.5.5 (L2) postMessage:** if the app's JS uses `postMessage`, verify
  `event.origin` is checked.
- **3.5.6 / 3.5.7 (L3) JSONP/XSSI:** no JSONP endpoints; authorized data not in
  JS resource responses.
- **3.5.8 (L3):** authenticated images/scripts embeddable only when intended.

## V3.7 Other / redirects

#### 3.7.2 — Open-redirect allowlist · L2
- **Mechanism (Rails):** Rails ≥ 7.0 blocks cross-host `redirect_to` by default
  (raises unless `allow_other_host: true`). Finding: pre-7.0, or
  `redirect_to params[:url], allow_other_host: true`, or `redirect_back`.
- **Payload:** `?return_to=//evil.example` · `?next=https://evil.example` ·
  `?url=/\evil.example`
- **Positive (secure):** redirect stays on-host, or `ActionController::Redirecting::UnsafeRedirectError`.
- **Negative (insecure):** `Location: https://evil.example` → open redirect.
  Upstream [Open Redirect](../../upstream/PayloadsAllTheThings/Open%20Redirect/README.md).

**3.6.1 SRI (L3):** externally-hosted JS/CSS carry `integrity=`+`crossorigin`.
**3.7.1 (L2):** no dead/insecure client tech (Flash/Silverlight). **3.7.3–3.7.5
(L3):** external-redirect notice, HSTS preload-list membership, graceful
behaviour on unsupported browsers. **3.1.1 (L3):** documentation of required
browser security features.

---
*Covers ASVS V3.1–V3.7. Full CSRF mechanics: [V13](V13-configuration.md).*
