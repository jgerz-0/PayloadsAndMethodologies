# V7 – Session Management (Rails)

> **ASVS 5.0 · Chapter V7** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V07-Session-Management.md`](../_asvs-base/V07-Session-Management.md).
> Rails' default store is the **encrypted cookie store**: session data lives
> client-side, protected only by `secret_key_base`. That makes key secrecy,
> regeneration, timeout, and termination the core tests.

## How the Rails cookie session works (context)

The session hash is serialized (`:json` default since 4.1; `:marshal` legacy),
then signed+encrypted (AES-GCM) with keys derived from `secret_key_base`.
Anyone with `secret_key_base` can **decrypt and forge any session**; with the
`:marshal` serializer that is also **RCE** ([V1.5.2](V01-encoding-and-sanitization.md)).
Recovering `secret_key_base` ([V11](V11-cryptography.md)) is therefore critical.

## V7.2 Fundamental session security

#### 7.2.4 — New session token on authentication (fixation) · L1
- **Mechanism (Rails):** Devise/`reset_session` regenerate the session on
  login; hand-rolled auth often just sets `session[:user_id]` on the existing
  session.
- **How to test:** record the session cookie pre-login, authenticate, compare.
- **Positive (secure):** cookie value changes on login (old one invalid).
- **Negative (insecure):** same cookie, now authenticated → fixation: an
  attacker-fixed session is adopted.

#### 7.2.2 / 7.2.3 — Dynamic, high-entropy tokens · L1
- **Mechanism (Rails):** sessions are dynamic per login; any auth relying on a
  **static API key/secret** as a session fails 7.2.2. Reference tokens
  (remember-me, API) must be CSPRNG-generated (`SecureRandom`,
  [V11](V11-cryptography.md)) with sufficient entropy.
- **Negative (insecure):** predictable/static session or remember tokens.

**7.2.1 (L1):** verification happens server-side (trusted backend) — for the
cookie store, integrity is the HMAC/encryption, verified server-side each
request.

## V7.3 Session timeout

#### 7.3.1 / 7.3.2 — Inactivity & absolute timeout · L2
- **Mechanism (Rails):** `config.session_store ..., expire_after: 30.minutes`
  and/or Devise `:timeoutable` (`config.timeout_in`). Absent = session cookie
  with no server-enforced idle/absolute limit.
- **How to test:** leave a session idle past the policy; attempt use after the
  absolute lifetime.
- **Positive (secure):** re-authentication forced after inactivity/absolute
  limit.
- **Negative (insecure):** session valid indefinitely.

## V7.4 Session termination

#### 7.4.1 — Termination disallows further use · L1
- **Mechanism (Rails):** because the cookie store is **stateless**, "logout"
  only deletes the browser cookie — a **captured cookie stays valid until
  expiry** unless the app tracks server-side invalidation (Devise
  `:timeoutable`, a per-user `session_token`, or a server-side store like
  `:active_record_store`/Redis).
- **How to test:** capture the cookie, log out, replay the captured cookie.
- **Positive (secure):** replayed cookie rejected (server-side revocation).
- **Negative (insecure):** replayed cookie still authenticates → no real
  termination.

#### 7.4.2 / 7.4.3 / 7.4.5 — Terminate on disable; on credential change; by admin · L1/L2
- **How to test:** with two active sessions, change the password (or disable the
  account) in one; check the other.
- **Positive (secure):** other sessions invalidated after password change /
  account disable; admin can terminate sessions.
- **Negative (insecure):** other sessions survive a password reset — a captured
  session outlives the credential it was born from.

**7.4.4 (L2):** visible logout on authenticated pages.

## V7.5 Defenses against session abuse

#### 7.5.1 — Re-authentication before sensitive attribute change · L2
- **How to test:** change email/phone/MFA settings using only an existing
  session (no password re-entry).
- **Positive (secure):** step-up re-auth required.
- **Negative (insecure):** sensitive attribute changed from a riding session
  (chains with CSRF/XSS to full ATO).

**7.5.2 (L2):** users can view/terminate active sessions; **7.5.3 (L3):**
step-up before highly sensitive transactions. **7.1.x** documentation of
timeouts/concurrent sessions. **7.6.x (L2)** federated (SSO) session lifetime
and consent-to-create.

> **Cookie tampering / forgery:** with a recovered/weak/default
> `secret_key_base`, decrypt and re-sign the session to impersonate any user
> (and RCE if `:marshal`). Metasploit `rails_secret_deserialization`. See
> [V11](V11-cryptography.md) and [V1.5.2](V01-encoding-and-sanitization.md).

---
*Covers ASVS V7.1–V7.6.*
