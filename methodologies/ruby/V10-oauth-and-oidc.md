# V10 – OAuth and OIDC (Rails)

> **ASVS 5.0 · Chapter V10** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V10-OAuth-and-OIDC.md`](../_asvs-base/V10-OAuth-and-OIDC.md).
> Rails acts as an **OAuth client / OIDC relying party** via `omniauth`
> (+ strategy gems), or as an **authorization server** via `doorkeeper`.
> **Applicability:** skip if the app has no OAuth/OIDC; state that.

## V10.2 / V10.5 — OAuth client / OIDC relying party (omniauth)

#### 10.2.1 — CSRF on the authorization request (state) · L2
- **Mechanism (Rails):** omniauth sets/verifies a `state` param (and since
  omniauth 2.x, request phase is POST-only by default — don't re-enable GET).
- **How to test:** start a flow, complete the callback with a missing/altered
  `state`.
- **Positive (secure):** callback rejected on `state` mismatch
  (`csrf_detected`).
- **Negative (insecure):** callback accepted without a valid `state` → login
  CSRF / account-injection. Upstream
  [OAuth Misconfiguration](../../upstream/PayloadsAllTheThings/OAuth%20Misconfiguration/README.md).

#### 10.1.2 — Callback values bound to an initiated flow · L2 · 10.5.1 nonce
- **How to test:** replay an authorization `code`/ID token into a session that
  didn't initiate the flow; for OIDC, alter/omit `nonce`.
- **Positive (secure):** code/ID token only accepted for the matching initiated
  flow; `nonce` in the ID token matches the request.
- **Negative (insecure):** code/ID token injectable → takeover.

#### 10.5.2 / 10.5.4 — Identify user by stable claim; validate `aud` · L2
- **Mechanism (Rails):** map the account from `sub` (not email, which is
  reassignable/unverified); verify ID token `aud == client_id`.
- **Negative (insecure):** user matched on unverified `email` → spoof via a
  second IdP with the same email (10.8/6.8.1 overlap); `aud` unchecked.

## V10.4 — Authorization server (doorkeeper)

#### 10.4.1 — redirect_uri exact-match allowlist · L1
- **Mechanism (Rails):** Doorkeeper matches registered `redirect_uri`; avoid
  wildcard/substring matching.
- **Payload:** `redirect_uri=https://TARGET.evil.com`,
  `redirect_uri=https://legit%2f@evil.com`, open-redirect on a registered host
  used to bounce the code out.
- **Positive (secure):** non-exact `redirect_uri` rejected (`invalid_redirect_uri`).
- **Negative (insecure):** attacker URI accepted → authorization code/token
  exfiltration.

#### 10.4.2 / 10.4.3 — Code single-use & short-lived · L1
- **Payload:** exchange the same authorization `code` twice; exchange a code
  older than its lifetime (≤ 10 min L1/L2).
- **Positive (secure):** second exchange fails and (per spec) prior tokens are
  revoked; expired code rejected.
- **Negative (insecure):** code reusable or long-lived.

#### 10.4.6 — PKCE for the code flow · L2 · 10.4.4 restrict grants
- **How to test:** run the code flow without `code_challenge`/`code_verifier`;
  attempt implicit (`response_type=token`) or password grant.
- **Positive (secure):** PKCE required; implicit/password grants disabled.
- **Negative (insecure):** flow completes without PKCE, or legacy grants allowed.

**10.3.x (L2) resource server:** validate access-token `aud`, enforce `scope`,
identify the user from a stable claim. **10.4.5/10.4.8/10.4.9 (L2):** refresh
token replay protection, absolute expiry, revocation. **10.7.x (L2):** consent
shown per request and revocable. **10.4.10 (L2):** confidential clients
authenticated on backchannel.

---
*Covers ASVS V10.1–V10.7. Token signature/claim validation details:
[V9](V09-self-contained-tokens.md).*
