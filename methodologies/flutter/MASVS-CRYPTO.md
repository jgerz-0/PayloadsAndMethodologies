# MASVS-CRYPTO – Cryptography (Flutter)

> **MASVS v2 · Cryptography** — projected onto Flutter (Android + iOS).
> Base: [`_masvs-base/MASVS-CRYPTO.md`](../_masvs-base/MASVS-CRYPTO.md).
> Dart has no batteries-included crypto, so apps pull `encrypt`, `pointycastle`,
> `cryptography`, `crypto` — and routinely misuse them (ECB, static IV, `Random`
> for keys, keys hardcoded into the snapshot).

## MASVS-CRYPTO-1 — Strong cryptography, used correctly

#### Mechanism / sink (Flutter)
- **Weak randomness:** `dart:math` `Random()` used for keys/IVs/tokens/nonces.
  It is a PRNG, **not** cryptographic. Only `Random.secure()` is CSPRNG. (Also
  native `SecureRandom` via pointycastle seeded from `Random()` — same bug.)
- **Broken algorithms/modes:** `encrypt`'s `AESMode.ecb`, or CBC with a
  **constant/zero IV**; MD5/SHA-1 via `package:crypto` for integrity/signing;
  DES/3DES.
- **Custom/rolled crypto** instead of platform primitives.

#### How to test
- **Static (Blutter + strings):** search recovered code for `Random(` vs
  `Random.secure(`, `AESMode.ecb`, `IV.fromLength(16)` / `IV.allZerosOfLength`,
  `md5`, `sha1`, hardcoded hex/base64 blobs near cipher calls.
- **Dynamic (Frida):** hook the cipher/`SecureRandom` entry points
  (pointycastle/platform) to observe algorithm, mode, key and IV at runtime;
  confirm IV varies per message.
- MASTG: [MASTG-TEST-0204](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0204.md)/[0205](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0205.md)/[0311](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0311.md) (insecure random),
  [MASTG-TEST-0221](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0221.md)/[0210](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0210.md) (broken symmetric),
  [MASTG-TEST-0232](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0232.md)/[0317](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0317.md)/[0350](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0350.md) (modes),
  [MASTG-TEST-0309](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0309.md)/[0310](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0310.md) (reused IV),
  [MASTG-TEST-0211](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0211.md) (hashing).

#### Positive evidence (secure)
AES-GCM (or CBC with a random per-message IV), keys/IVs from `Random.secure()`
or the platform KeyStore/SecKey; SHA-256+ for integrity; no ECB; ciphertext of a
repeated plaintext differs each time.

#### Negative evidence (insecure)
`Random()` seeding a key; `AESMode.ecb` (identical plaintext blocks → identical
ciphertext blocks — visible in the "ECB penguin"); constant IV across messages;
MD5/SHA-1 for a security purpose.

## MASVS-CRYPTO-2 — Key management

#### Mechanism / sink (Flutter)
- **Hardcoded keys / secrets in the snapshot:** AES keys, HMAC secrets, API
  keys, and `--dart-define` values are **compiled into `libapp.so`** and
  recoverable. A key in the binary is not a secret.
- **Keys stored alongside ciphertext** (same `shared_preferences`/DB) rather than
  the Keystore/Keychain.
- **No hardware backing:** key material in Dart memory instead of
  Android KeyStore / iOS `SecKey` (which Flutter reaches via
  `flutter_secure_storage`, platform channels, or plugins like
  `cryptography_flutter`).

#### How to test
- **Static:** `strings libapp.so`, Blutter output, and `grep -R` the decoded
  assets for key-shaped constants; check how `encrypt`/`pointycastle` key args
  are sourced (literal vs Keystore).
- Verify `--dart-define`/`.env` secrets by searching the snapshot for their
  values.
- MASTG: [MASTG-TEST-0212](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0212.md)/[0213](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0213.md)/[0214](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0214.md) (hardcoded keys),
  [MASTG-TEST-0208](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0208.md)/[0209](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0209.md) (key sizes),
  [MASTG-TEST-0307](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0307.md) (key reuse across purposes).

#### Positive evidence (secure)
Keys generated on-device and held in Keystore/Keychain (non-exportable); no key
material in `strings`/Blutter; RSA ≥2048 / AES ≥128; distinct keys per purpose.

#### Negative evidence (insecure)
`final key = Key.fromUtf8('my32characterslongsecretkey!!!');` recovered from the
snapshot; the same key decrypts data across all installs; API secret extractable
from the binary → backend abuse. Upstream
[Hardcoded secrets patterns](../../upstream/PayloadsAllTheThings/API%20Key%20Leaks/README.md).

---
*Covers MASVS-CRYPTO-1/-2. Where the key *lives* (Keystore/Keychain vs plaintext)
also → [STORAGE](MASVS-STORAGE.md). Pinning crypto → [NETWORK](MASVS-NETWORK.md).*
