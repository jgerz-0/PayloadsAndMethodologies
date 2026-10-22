# V6 – Authentication (Rails)

> **ASVS 5.0 · Chapter V6** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V06-Authentication.md`](../_asvs-base/V06-Authentication.md).
> Mostly **Devise** (warden) or `has_secure_password` (bcrypt). Password
> policy, enumeration, brute force, reset flows, MFA.

## V6.2 Password security

#### 6.2.1 — Minimum length ≥ 8 (15 recommended) · L1
- **Mechanism (Rails):** Devise `config.password_length = 6..128` by **default
  (6)** — below ASVS's 8. `has_secure_password` sets no minimum unless you add
  `validates :password, length: {minimum: 8}`.
- **Payload:** register with `user[password]=aaaaaa` (6 chars).
- **Positive (secure):** rejected; minimum ≥ 8 enforced.
- **Negative (insecure):** 6-char password accepted → 6.2.1 fail.

#### 6.2.5 / 6.2.7 / 6.2.8 / 6.2.9 — Composition, paste, exact verification, ≥64 chars · L1/L2
- **Mechanism (Rails):** no forced composition rules; allow paste/managers
  (frontend); verify the password exactly. **bcrypt truncates at 72 bytes** —
  Devise/`has_secure_password` therefore effectively ignore characters past 72,
  which interacts with 6.2.8 (no silent modification) and 6.2.9 (allow ≥64).
- **How to test:** set a 64+ char password; try composition-restricted inputs.
- **Positive (secure):** long passwords accepted and verified; no composition
  rule rejects valid passphrases.
- **Negative (insecure):** password truncated/case-folded (two different long
  passwords sharing a 72-byte prefix both authenticate), or arbitrary
  composition rules imposed.

#### 6.2.4 / 6.2.12 — Breached / common password check · L1/L2
- **Mechanism (Rails):** `devise-pwned_password` gem or a custom HIBP
  range-API validator. Absent = no check.
- **Payload:** set password to `Password1!` / `123456`.
- **Positive (secure):** `422`, "this password has appeared in a data breach";
  not accepted.
- **Negative (insecure):** `302` to dashboard; breached password accepted.

#### 6.2.2 / 6.2.3 — Change password; requires current + new · L1
- **Payload:** call the change-password endpoint **without** the current
  password field.
- **Positive (secure):** rejected — current password required.
- **Negative (insecure):** password changed without proving the current one
  (also enables session-riding takeover).

**6.2.6 (L1)** `type=password` masking; **6.2.10 (L2)** no forced periodic
rotation; **6.2.11 (L2)** context-word blocklist; **6.1.x** documentation of
rate-limiting/password policy/multiple auth pathways.

## V6.3 General authentication security

#### 6.3.8 — No user enumeration (messages / codes / timing) · L3 (test always)
- **Mechanism (Rails):** Devise default login error is generic ("Invalid Email
  or password"); `config.paranoid = true` makes reset/confirmation responses
  identical for known vs unknown emails. **Timing:** bcrypt runs only when the
  user exists → timing oracle.
- **How to test:** compare login/reset responses (text, status, redirect) and
  **timing** for a known vs random email.
- **Payload:** `for e in victim@target.com rand@x.com; do curl -s -o /dev/null -w "$e %{time_total}\n" -d "user[email]=$e&user[password]=x" .../users/sign_in; done`
- **Positive (secure):** identical message/status and near-identical timing
  (dummy-hash compare for missing users); registration/reset don't disclose
  existence.
- **Negative (insecure):** distinct "no account"/"already taken" message, or a
  consistent ~100 ms delta for valid users → enumeration. Upstream
  [Account Takeover](../../upstream/PayloadsAllTheThings/Account%20Takeover/README.md).

#### 6.3.1 — Brute-force / credential-stuffing controls · L1
- **Mechanism (Rails):** Devise `:lockable` (default off), `rack-attack`, or
  7.2+ `rate_limit`. Absence = unlimited guessing.
- **Payload:** 50 sequential wrong logins for one account.
- **Positive (secure):** lockout or `429` after a threshold.
- **Negative (insecure):** all attempts processed, no lockout/throttle.

#### 6.3.2 — No default accounts · L1 · 6.3.3 MFA · L2
- Test seeded/default creds (`admin/admin`, `root`); for L2, that an MFA (or
  combined single-factor) path exists and is enforced.

**6.3.5 / 6.3.7 (L3):** notify users of suspicious attempts and of credential/
email changes. **6.3.6 (L3):** email not used as an auth factor.

## V6.4 Factor lifecycle & recovery

#### 6.4.3 — Secure password reset (doesn't bypass MFA) · L2
- **Mechanism (Rails):** Devise `:recoverable` stores a **hashed**
  `reset_password_token`, emails the raw token, expires per
  `reset_password_within` (default 6 h). Risks: no expiry, reusable token, or
  the reset URL built from the request `Host`/`X-Forwarded-Host` (poisonable).
- **Payload:** `POST /users/password` with `Host: attacker.com` /
  `X-Forwarded-Host: attacker.com` for `user[email]=victim@target.com`.
- **Positive (secure):** reset link uses a fixed `default_url_options` host;
  token single-use and expiring; reset re-prompts MFA.
- **Negative (insecure):** email links to `https://attacker.com/users/password/edit?reset_password_token=...`
  → one-click ATO; or token reusable/never expires. Cross-ref
  [V4.1.3](V04-api-and-web-service.md), [V13 hosts](V13-configuration.md).

#### 6.4.1 — Secure random initial passwords / activation codes · L1 · 6.4.2 no secret questions
- **Mechanism (Rails):** initial/activation codes via `SecureRandom`
  ([V11](V11-cryptography.md)), short-lived, single-use; no knowledge-based
  "secret questions".
- **Negative (insecure):** predictable (`rand`, sequential, timestamp-derived)
  codes, or security-question recovery present.

**6.4.4–6.4.6 (L2/L3):** MFA-loss identity proofing; renewal timing; admin can
*initiate* but not *choose* a user's password.

## V6.5 / V6.6 Multi-factor

If MFA is present (`devise-two-factor`, `rotp`, WebAuthn), test:
- **6.5.1 (L2):** TOTP/OTP/lookup secrets usable **once** — replay a consumed
  code (positive: rejected; negative: accepted again).
- **6.5.3 (L2):** seeds/codes from a CSPRNG; **6.5.4** ≥ 20 bits entropy;
  **6.5.5** defined OTP lifetime; **6.5.8 (L3)** TOTP checked against trusted
  time.
- **6.6.3 (L2):** code-based OOB protected by rate limiting (race the OTP
  endpoint — overlaps [V2.4](V02-validation-and-business-logic.md)); **6.6.4
  (L3)** push-bombing rate limits.
- **2FA bypass:** hit authenticated endpoints with the post-password/pre-OTP
  session cookie — many implementations set a full session before the OTP gate.

## V6.8 Identity provider / assertions

If the app consumes SAML/JWT assertions (omniauth-saml, etc.):
- **6.8.2 (L2):** signature presence **and** integrity validated — reject
  unsigned/`alg:none`/tampered assertions (full JWT set in
  [V9](V09-self-contained-tokens.md); SAML in
  [SAML Injection](../../upstream/PayloadsAllTheThings/SAML%20Injection/README.md)).
- **6.8.3 (L2):** SAML assertions single-use within validity (replay).
- **6.8.1 (L2):** can't spoof identity across multiple IdPs via the same
  identifier.

---
*Covers ASVS V6.1–V6.8. Session lifecycle after login: [V7](V07-session-management.md).*
