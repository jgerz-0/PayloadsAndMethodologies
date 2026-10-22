# V11 – Cryptography (Rails)

> **ASVS 5.0 · Chapter V11** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V11-Cryptography.md`](../_asvs-base/V11-Cryptography.md).
> Password hashing (bcrypt), CSPRNG (`SecureRandom`), symmetric crypto
> (`MessageEncryptor`, ActiveRecord Encryption), and the `secret_key_base` /
> credentials key hierarchy that underpins sessions and tokens.

## The Rails secret hierarchy (context)

`config/master.key` (or `RAILS_MASTER_KEY`) → decrypts
`config/credentials.yml.enc` → contains `secret_key_base` + DB/API keys →
`secret_key_base` derives session-cookie keys and `MessageVerifier`/
`MessageEncryptor` keys. Recovering any upper level cascades down: a leaked
`master.key` yields everything; a leaked `secret_key_base` yields session
forgery ([V7](V07-session-management.md)) and `:marshal` RCE
([V1.5.2](V01-encoding-and-sanitization.md)). Hunting these is in
[V13 §13.3/§13.4](V13-configuration.md); their crypto strength is here.

## V11.4 Hashing

#### 11.4.2 — Password hashing function & parameters · L2
- **Mechanism (Rails):** bcrypt (Devise/`has_secure_password`), or argon2/scrypt
  via a gem. Confirm cost.
- **How to test (grey/white-box):** inspect a `password_digest` value.
- **Positive (secure):** `$2a$12$...` (bcrypt cost ≥ 10–12), or argon2id with
  sane params.
- **Negative (insecure):** `$2a$04$...` (cost 4), unsalted `SHA1`/`MD5`
  (`Digest::SHA1.hexdigest`), or a plaintext password column — critical.

#### 11.4.1 — Approved hash functions · L1
- **Negative (insecure):** MD5/SHA1 used for signatures/integrity/HMAC; SHA-1
  `OpenSSL::Digest`. Approved: SHA-256+/SHA-3.

## V11.5 Random values

#### 11.5.1 — CSPRNG for non-guessable values · L2
- **Mechanism (Rails):** `SecureRandom.hex/uuid/base58` for tokens (reset,
  invite, API, session). **`rand`/`Random`/`Time.now`-derived** values are
  predictable.
- **How to test:** collect many issued tokens (reset/invite/API); check for
  sequence, timestamp structure, or short length.
- **Positive (secure):** ≥ 128-bit, uniformly random, no structure.
- **Negative (insecure):** short/sequential/time-correlated tokens → forgeable.
  Upstream [Insecure Randomness](../../upstream/PayloadsAllTheThings/Insecure%20Randomness/README.md).

## V11.3 Encryption algorithms

#### 11.3.1 / 11.3.2 / 11.3.3 — Modes & authenticated encryption · L1/L2
- **Mechanism (Rails):** `ActiveSupport::MessageEncryptor` and ActiveRecord
  Encryption default to AES-256-GCM (authenticated). Findings arise in **custom**
  `OpenSSL::Cipher` usage: `AES-256-ECB`, CBC without a MAC (padding-oracle),
  static IV, PKCS#1 v1.5.
- **How to test (white-box / behavioural):** grep `OpenSSL::Cipher.new`; look
  for ECB/CBC-no-MAC, hardcoded IV; test ciphertext malleability / padding
  oracle on any custom-encrypted blob reflected to the user.
- **Positive (secure):** AES-GCM (or encrypt-then-MAC), random IV per message,
  keys from credentials.
- **Negative (insecure):** ECB (pattern leakage), unauthenticated CBC (padding
  oracle), reused IV.

#### Weak/leaked `MessageVerifier`/`MessageEncryptor` keys
- Signed-only cookies/tokens (`cookies.signed[...]`, `verifier.generate`) are
  **readable** by anyone (base64) and forgeable if the key is weak/leaked;
  confidential data must be *encrypted*, not just signed.

## V11.1 / V11.2 (documentation & implementation)

**11.1.x (L2/L3):** documented key-management policy, lifecycle, and crypto
inventory (incl. post-quantum migration plan). **11.2.1 (L2):** use vetted
libraries (OpenSSL/`rbnacl`), not hand-rolled crypto. **11.2.3 (L2):** ≥ 128-bit
security. **11.2.4/11.2.5 (L3):** constant-time comparisons
(`ActiveSupport::SecurityUtils.secure_compare`, not `==`) and
fail-secure (no padding-oracle leakage). **11.6/11.7 (L2/L3):** approved
public-key algs; in-use data protection.

---
*Covers ASVS V11.1–V11.7. Secret storage/rotation & leakage hunting:
[V13](V13-configuration.md).*
