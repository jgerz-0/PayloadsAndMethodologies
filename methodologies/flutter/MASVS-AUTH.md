# MASVS-AUTH – Authentication and Authorization (Flutter)

> **MASVS v2 · Authentication & Authorization** — projected onto Flutter.
> Base: [`_masvs-base/MASVS-AUTH.md`](../_masvs-base/MASVS-AUTH.md).
> **Most of real auth/authz lives on the backend** — test it against
> [ASVS V6](../_asvs-base/V06-Authentication.md) / [V8](../_asvs-base/V08-Authorization.md) /
> [V9](../_asvs-base/V09-Self-contained-Tokens.md). This page is the *client*
> half: how the Flutter app handles tokens and local (biometric/PIN) auth.

## MASVS-AUTH-1 — Secure auth/authz protocols & best practices

#### Mechanism / sink (Flutter)
- **Token handling:** where the session/JWT/refresh token is stored (→ must be
  `flutter_secure_storage`, not `shared_preferences` — [STORAGE](MASVS-STORAGE.md))
  and how it's attached (`Authorization` header via a `dio`/`http`
  interceptor).
- **Client-side trust of auth decisions:** the app gating a screen/feature in
  Dart (`if (user.isAdmin)`) while the **backend** doesn't re-check — a classic
  "the server must enforce it" gap. The client control is bypassable by design.
- **OAuth/OIDC:** via `flutter_appauth`/`oauth2`/`AppAuth` — redirect handling,
  PKCE, token storage (→ [ASVS V10](../_asvs-base/V10-OAuth-and-OIDC.md)).

#### How to test
- Pull the token from storage after login (sandbox dump) and from the wire
  (intercept); confirm it's a backend-verifiable credential, stored encrypted.
- With the token, hit the API directly (Burp/curl) to confirm the **server**
  enforces authz — flip IDs/roles (this is ASVS V8 work, driven from the token
  you recovered).
- Static: Blutter for role/feature checks done only in Dart.

#### Positive evidence (secure)
Token in Keychain/Keystore; every privileged action re-authorized server-side;
PKCE + `state` on OAuth; logout invalidates server-side.

#### Negative evidence (insecure)
Admin feature unlocked purely by a Dart flag while the API accepts the call from
a normal user (→ server authz finding); refresh token in plaintext prefs; OAuth
without PKCE.

## MASVS-AUTH-2 — Local authentication done securely

#### Mechanism / sink (Flutter)
`local_auth` plugin (`authenticate(...)`) bridges to BiometricPrompt (Android) /
`LocalAuthentication` (iOS). The **danger**: local auth is an *event* ("user
passed biometric") the Dart code trusts — it does **not** by itself unlock a
key. If success merely sets a boolean / returns `true`, it's bypassable.

#### How to test
- **Frida bypass:** hook `local_auth`'s result to force success, or on iOS hook
  `LAContext evaluatePolicy` callback / Android `BiometricPrompt` callback
  (Objection `ios ui biometrics_bypass`). If the gated content then appears,
  biometrics are decorative.
- Check whether unlock is **crypto-bound**: does success decrypt a
  Keystore/Keychain key (`setUserAuthenticationRequired(true)` /
  `kSecAccessControlBiometryCurrentSet`) or just flip a flag?
- MASTG: [MASTG-TEST-0267](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0267.md)/[0269](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0269.md) (event-bound / fallback, iOS),
  [MASTG-TEST-0327](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0327.md)/[0329](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0329.md) (event-bound / no explicit action, Android),
  [MASTG-TEST-0270](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0270.md)/[0328](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0328.md) (enrollment-change detection).

#### Positive evidence (secure)
Biometric success gates on **decrypting a hardware key** bound to the current
biometric set; a Frida hook that forces `true` still can't produce the
protected data (the key stays locked). Enrollment changes invalidate the key.

#### Negative evidence (insecure)
Forcing the `authenticate()` result to success reveals the protected
screen/data; unlock is "event-bound" (boolean), not key-bound; fallback to
device PIN silently permitted where policy forbids.

## MASVS-AUTH-3 — Additional auth for sensitive operations

#### Mechanism / sink (Flutter)
Step-up auth (re-enter PIN/biometric/MFA) before high-risk actions (payment,
change email, export). The step-up must be **enforced server-side**, not just a
Dart re-prompt.

#### How to test
Perform the sensitive action while intercepting; replay the API call without the
step-up token/flag. If the server completes it, the step-up is client-only.

#### Positive / negative evidence
**Secure:** API rejects the sensitive call lacking a fresh step-up proof.
**Insecure:** the step-up is a Dart dialog only; the raw API call succeeds
without it.

---
*Covers MASVS-AUTH-1/-2/-3. Backend authentication/session/token/authorization is
ASVS — [V6](../_asvs-base/V06-Authentication.md) · [V7](../_asvs-base/V07-Session-Management.md) ·
[V8](../_asvs-base/V08-Authorization.md) · [V9](../_asvs-base/V09-Self-contained-Tokens.md).*
