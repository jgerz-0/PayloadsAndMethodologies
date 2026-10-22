# Ruby on Rails Testing Methodology (ASVS 5.0-aligned)

> Offensive testing methodology for **Ruby on Rails**, structured 1:1 against
> the [ASVS 5.0 base](../_asvs-base/README.md). One page per ASVS chapter
> (V01–V17); within each, requirements are projected onto Rails with the
> concrete sink/mechanism, how to test, payloads, and **positive (secure) vs
> negative (insecure) response examples**.
>
> Generated via the [`create-methodology`](../../.claude/skills/create-methodology/SKILL.md)
> skill from the ASVS base, so coverage tracks the standard. For generic
> payload lists it links the upstream
> [PayloadsAllTheThings](../../upstream/PayloadsAllTheThings/README.md) library
> and focuses on what is *specific to Rails*.

## How to use

1. Start with **Fingerprinting** below to confirm Rails and pin
   Rails/Ruby/gem versions (drives [V15](V15-secure-coding-and-architecture.md)
   CVE checks).
2. Scope by **ASVS level** (L1 baseline / L2 standard / L3 high-assurance) and
   walk the chapters. Each requirement block states the Rails control, the
   test, and what secure vs insecure looks like on the wire.
3. Rails is **secure-by-default, broken-by-override** — the highest-yield move
   is finding the explicit opt-out of a default protection (`html_safe`/`raw`,
   `permit!`, `skip_before_action :verify_authenticity_token`,
   `where("...#{}")`, `allow_other_host: true`, `YAML.load`,
   `config.hosts.clear`, `:marshal` cookie serializer).

## Chapters

| ASVS | Rails page | Dominant Rails concerns |
|---|---|---|
| V1 Encoding & Sanitization | [V01](V01-encoding-and-sanitization.md) | ERB escaping, SQLi, command injection, SSTI, deserialization, XXE, CSV injection |
| V2 Validation & Business Logic | [V02](V02-validation-and-business-logic.md) | Strong params validation, business-logic sequencing, locking, anti-automation |
| V3 Web Frontend Security | [V03](V03-web-frontend-security.md) | Cookie flags, CSP/HSTS/headers, CORS, open redirect, MIME sniffing |
| V4 API & Web Service | [V04](V04-api-and-web-service.md) | API mode, GraphQL, WebSocket/ActionCable, HTTP method handling |
| V5 File Handling | [V05](V05-file-handling.md) | Uploads, `send_file`/`render file:`, path traversal, zip slip |
| V6 Authentication | [V06](V06-authentication.md) | Devise, passwords, MFA, reset flows, enumeration |
| V7 Session Management | [V07](V07-session-management.md) | Cookie store, `secret_key_base`, regeneration, timeout, termination |
| V8 Authorization | [V08](V08-authorization.md) | IDOR/BOLA, Pundit/CanCanCan, multi-tenant, admin interfaces |
| V9 Self-contained Tokens | [V09](V09-self-contained-tokens.md) | JWT (devise-jwt/knock): signature, alg, aud, exp |
| V10 OAuth & OIDC | [V10](V10-oauth-and-oidc.md) | omniauth/doorkeeper: redirect_uri, PKCE, state, token handling |
| V11 Cryptography | [V11](V11-cryptography.md) | bcrypt, `SecureRandom`, AR encryption, MessageEncryptor, modes |
| V12 Secure Communication | [V12](V12-secure-communication.md) | `force_ssl`, TLS, cert validation on outbound calls |
| V13 Configuration | [V13](V13-configuration.md) | `config.hosts`, secrets, debug/env leakage, `.git`, dir listing |
| V14 Data Protection | [V14](V14-data-protection.md) | Caching of sensitive data, PII in URLs/logs, client storage |
| V15 Secure Coding & Architecture | [V15](V15-secure-coding-and-architecture.md) | Deserialization, SSRF, mass assignment, deps/CVEs, race conditions |
| V16 Logging & Error Handling | [V16](V16-security-logging-and-error-handling.md) | `web-console`/`better_errors` RCE, stack traces, `filter_parameters`, log injection |
| V17 WebRTC | [V17](V17-webrtc.md) | N/A for typical Rails (see page) |

## Fingerprinting (quick ref)

| Signal | Tell |
|---|---|
| Session cookie | `Set-Cookie: _<app>_session=...--<hmac>` (signed/encrypted Rails cookie store) |
| CSRF | `<meta name="csrf-token">`, hidden `authenticity_token`, **HTTP 422** on bad token |
| Headers | `X-Runtime: 0.0x`; weak ETags `W/"..."` |
| Errors | static `public/404.html` / `500.html`; `/rails/info/routes`, `/rails/info/properties` in dev |
| Assets | `/assets/application-<40hex>.js` (Sprockets) / Propshaft / vite |
| Engines | `/cable` (ActionCable), `/rails/active_storage/...`, `/sidekiq`, `/blazer`, `/flipper` |
| Version | gem paths in stack traces (`gems/actionpack-7.1.3.2/...`); `Gemfile.lock` if leaked → `bundler-audit` |

Devise routes (`/users/sign_in`, `/users/password/new`, …) pin the auth stack.

## Tooling

* **`brakeman -A`** — static analysis (each page notes the relevant warning).
* **`bundler-audit check --update`** — `Gemfile.lock` vs the rubysec advisory DB.
* **`rails-sqli.org`** — injectable ActiveRecord methods by version.
* **Burp Suite** — Collaborator for blind SSRF/SSTI/injection OOB; Autorize for IDOR.

## References

* [ASVS 5.0 base](../_asvs-base/README.md) · [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
* [Rails Security Guide](https://guides.rubyonrails.org/security.html)
* [OWASP Rails Cheat Sheet](../../upstream/CheatSheetSeries/cheatsheets/Ruby_on_Rails_Cheat_Sheet.md)
* Upstream: [PayloadsAllTheThings](../../upstream/PayloadsAllTheThings/README.md)
