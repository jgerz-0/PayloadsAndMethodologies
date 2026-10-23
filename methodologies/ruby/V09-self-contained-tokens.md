# V9 – Self-contained Tokens (Rails)

> **ASVS 5.0 · Chapter V9** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V09-Self-contained-Tokens.md`](../_asvs-base/V09-Self-contained-Tokens.md).
> JWTs and similar self-contained tokens: `devise-jwt`, `knock`, `jwt` gem,
> `json-jwt`, or tokens minted via Rails' `MessageVerifier`/`MessageEncryptor`.
> **Applicability:** if the app uses opaque server-side sessions only, most of
> this chapter is N/A — state that and move on.

## V9.1 Token source & integrity

#### 9.1.1 — Signature/MAC validated before use · L1
- **Mechanism (Rails):** the `jwt` gem verifies only when you pass
  `verify: true` **and** an algorithm. `JWT.decode(token, nil, false)` (verify
  off) or a rescue that falls back to unverified decode is the bug.
- **Payload:** tamper a claim (`{"user_id":1}`→`{"user_id":2,"admin":true}`),
  re-base64 without re-signing.
- **Positive (secure):** `JWT::VerificationError` → `401`.
- **Negative (insecure):** tampered token accepted → impersonation.

#### 9.1.2 — Algorithm allowlist (alg confusion / none) · L1
- **Mechanism (Rails):** `JWT.decode(token, key, true, { algorithms: ['HS256'] })`
  must pin algorithms. Not pinning allows `alg:none` and RS256→HS256 confusion
  (verify an RS256 token as HS256 using the **public key** as the HMAC secret).
- **Payload:** set header `{"alg":"none"}` and strip the signature; or re-sign
  with HS256 using the known RSA public key.
- **Positive (secure):** `none`/unexpected alg rejected.
- **Negative (insecure):** forged token accepted. Upstream
  [JSON Web Token](../../upstream/PayloadsAllTheThings/JSON%20Web%20Token/README.md).

#### 9.1.3 — Key material from trusted sources · L1
- **Mechanism (Rails):** signing key from credentials/ENV, not from the token.
  Watch `kid`/`jku`/`x5u` header handling that fetches keys from an
  attacker-influenced location. Also: a JWT signed with **`secret_key_base`**
  means a leaked key ([V11](V11-cryptography.md)) forges tokens.
- **Payload:** `kid` path traversal / injection; `jku` pointing at your JWKS.
- **Positive (secure):** key resolved from a pre-configured trusted source only.
- **Negative (insecure):** verifier fetches/selects a key the attacker controls.

#### Weak HMAC secret (brute force)
- If HS256 with a weak secret, crack offline (`hashcat -m 16500`) — a guessable
  `secret_key_base`/JWT secret yields full forgery.

## V9.2 Token content

#### 9.2.1 — Expiry (`exp`) enforced · L1
- **Payload:** replay a token whose `exp` is in the past.
- **Positive (secure):** `JWT::ExpiredSignature` → `401`.
- **Negative (insecure):** expired token still accepted (no `exp` verification,
  or `verify_expiration: false`).

#### 9.2.2 / 9.2.3 — Type & audience (`aud`) · L2
- **Mechanism (Rails):** verify the token is the right type (access vs refresh
  vs ID) and that `aud` matches this service (allowlist).
- **Payload:** present a refresh/ID token where an access token is expected;
  present a token minted for another audience.
- **Positive (secure):** wrong type/audience rejected.
- **Negative (insecure):** cross-type or cross-audience token accepted.

**9.2.4 (L2):** if one issuer key serves multiple audiences, tokens carry a
unique audience restriction.

> `devise-jwt` adds a **denylist/allowlist revocation strategy** — check it's
> configured, or logged-out JWTs remain valid until `exp`
> (overlaps [V7.4.1](V07-session-management.md)).

---
*Covers ASVS V9.1–V9.2. OAuth/OIDC flows that issue these tokens:
[V10](V10-oauth-and-oidc.md).*
