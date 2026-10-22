# V4 – API and Web Service (Rails)

> **ASVS 5.0 · Chapter V4** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V04-API-and-Web-Service.md`](../_asvs-base/V04-API-and-Web-Service.md).
> `ActionController::API`, Grape, `graphql-ruby`, and ActionCable (WebSocket).

## V4.1 Generic web service security

#### 4.1.1 — Correct `Content-Type` + charset · L1
- **Mechanism (Rails):** `render json:` sets `application/json`; hand-built
  responses or `send_data` without a type can mismatch, enabling sniffing.
- **Test:** `curl -sD- https://TARGET/api/x -o /dev/null | grep -i content-type`
- **Positive:** `Content-Type: application/json; charset=utf-8` matching the body.
- **Negative:** `text/html` for JSON, or missing charset → MIME-sniff XSS (pair
  with `nosniff`, [V3](V03-web-frontend-security.md)).

#### 4.1.3 — Intermediary headers not client-overridable · L1→L2
- **Mechanism (Rails):** the app must not trust client-supplied
  `X-Forwarded-For`/`X-Forwarded-Host`/`X-Forwarded-Proto` except from known
  proxies (`config.action_dispatch.trusted_proxies`). Overridable forwarded
  headers skew rate-limiting, IP allowlists, and URL generation.
- **Payload:** `-H 'X-Forwarded-For: 127.0.0.1'` (bypass IP throttle) /
  `-H 'X-Forwarded-Host: evil.example'` (poison generated URLs — see
  [V6 reset](V06-authentication.md), [V13 hosts](V13-configuration.md)).
- **Positive:** spoofed values ignored; real client IP/host used.
- **Negative:** spoofed value reflected in behaviour/URLs/logs.

**4.1.2 (L2):** only user-facing endpoints auto-redirect HTTP→HTTPS; pure APIs
shouldn't transparently redirect (hides downgrade). **4.1.4 (L3)** block unused
HTTP methods; **4.1.5 (L3)** per-message signatures for high-value requests.

## V4.2 HTTP message structure (request smuggling)

**4.2.1–4.2.5 (L2/L3):** primarily front-end/proxy + server framing concerns
(Puma, nginx, load balancers) — CL.TE/TE.CL desync, CRLF in HTTP/2. Test with
the upstream [Request Smuggling](../../upstream/PayloadsAllTheThings/Request%20Smuggling/README.md)
and [CRLF Injection](../../upstream/PayloadsAllTheThings/CRLF%20Injection/README.md)
methods; largely infrastructure rather than Rails code, but Rack has had header/
ReDoS CVEs ([V15](V15-secure-coding-and-architecture.md)).

## V4.3 GraphQL

#### 4.3.2 — Introspection disabled in prod · L2
- **Mechanism (Rails):** `graphql-ruby` — `disable_introspection_entry_points`
  / schema `disable_introspection`. On by default.
- **Payload:** `{"query":"{__schema{types{name fields{name}}}}"}`
- **Positive (secure):** introspection blocked (error / empty).
- **Negative (insecure):** full schema returned → maps hidden types/mutations.

#### 4.3.1 — Query depth / complexity / cost limits · L2
- **Mechanism (Rails):** `max_depth`, `max_complexity`, or a query allowlist in
  the schema. Missing → DoS via deep nesting and **aliasing/batching**
  (hundreds of aliased mutations in one request → brute-force past rate limits).
- **Payload:** deeply nested recursive query; or aliased `a: login b: login ...`.
- **Positive (secure):** request rejected over the depth/complexity cap.
- **Negative (insecure):** processed → resource exhaustion / rate-limit bypass.
- Tooling: `graphql-cop`, graphql-threat-matrix (see [graphql pointer](../graphql/README.md));
  upstream [GraphQL Injection](../../upstream/PayloadsAllTheThings/GraphQL%20Injection/README.md).

> IDOR/BOLA and field-level authz in GraphQL resolvers are
> [V8](V08-authorization.md); mass assignment via mutation inputs is
> [V15.3.3](V15-secure-coding-and-architecture.md).

## V4.4 WebSocket (ActionCable)

- **4.4.1 (L1) WSS:** the `/cable` endpoint must be `wss://`. Test for `ws://`.
- **4.4.2 (L2) Origin check:** ActionCable validates the handshake `Origin`
  against `config.action_cable.allowed_request_origins`. **Finding:**
  `allowed_request_origins` set to a permissive regex or
  `disable_request_forgery_protection = true` → cross-origin WS hijack.
  - **Payload:** complete the WS handshake with `Origin: https://evil.example`.
  - **Positive:** handshake rejected (`404`/`403`).
  - **Negative:** connection upgraded from an untrusted origin.
- **4.4.3 / 4.4.4 (L2):** ActionCable auth derives identity from the session
  cookie via `identified_by`/`verified_user`; verify it isn't accepting
  unauthenticated connections or static tokens.
- Upstream [Web Sockets](../../upstream/PayloadsAllTheThings/Web%20Sockets/README.md).

---
*Covers ASVS V4.1–V4.4. JWT/bearer specifics: [V9](V09-self-contained-tokens.md).*
