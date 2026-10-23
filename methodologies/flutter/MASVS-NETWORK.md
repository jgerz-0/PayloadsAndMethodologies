# MASVS-NETWORK – Network Communication (Flutter)

> **MASVS v2 · Network** — projected onto Flutter (Android + iOS).
> Base: [`_masvs-base/MASVS-NETWORK.md`](../_masvs-base/MASVS-NETWORK.md).
> The defining Flutter trait: Dart traffic rides the engine's own **BoringSSL**,
> bypassing the system proxy and the OS user-CA trust store — so interception
> and pinning both work differently from native apps.

> **Interception prerequisite.** Before testing anything on the wire, stand up
> Dart-level capture (see [README](README.md#what-makes-flutter-different-read-first)):
> **reFlutter** (patched engine) or **Frida** hooking
> `ssl_crypto_x509_session_verify_cert_chain` in `libflutter.so` + a transparent
> proxy route. A plain Burp CA + WiFi proxy only captures WebView/native-plugin
> traffic, not `dart:io`/`dio`/`http`.

## MASVS-NETWORK-1 — Secure all network traffic

#### Mechanism / sink (Flutter)
- **Cleartext HTTP:** `http://` URLs via `package:http`/`dio`/`HttpClient`. On
  Android, Flutter's `dart:io` generally honours the **Network Security Config**
  `cleartextTrafficPermitted`; on iOS, ATS governs `NSURLSession`-based plugins,
  but a custom socket can ignore both.
- **Disabled/weak TLS validation:**
  `HttpClient()..badCertificateCallback = (cert, host, port) => true` — the
  single most common Flutter TLS kill-switch (accepts **any** cert).
  Also `SecurityContext` loaded with an attacker-trustable CA, or a custom
  `badCertificateCallback` that only checks the host.
- **Low-level sockets** (`Socket`/`SecureSocket`) with no/!custom verification.

#### How to test
- **Static (Blutter):** grep recovered code for `badCertificateCallback`,
  `http://`, `SecurityContext`, `onBadCertificate`, `allowLegacyUnsafe...`.
  Check `AndroidManifest.xml` → `networkSecurityConfig` and
  `usesCleartextTraffic`; iOS `Info.plist` → `NSAppTransportSecurity`
  (`NSAllowsArbitraryLoads`).
- **Dynamic:** with interception up, confirm whether the app talks plain HTTP,
  and whether a self-signed cert is accepted *before* any pinning bypass (if it
  is, `badCertificateCallback` is returning true).
- MASTG: [MASTG-TEST-0237](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0237.md) (**cross-platform/Flutter cleartext config**),
  [MASTG-TEST-0236](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0236.md)/[0238](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0238.md) (cleartext observed),
  [MASTG-TEST-0233](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0233.md)/[0321](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0321.md) (hardcoded HTTP),
  [MASTG-TEST-0218](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0218.md)/[0348](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0348.md) (insecure TLS versions),
  [MASTG-TEST-0282](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0282.md) (unsafe custom trust eval).

#### Positive evidence (secure)
All endpoints `https://` with TLS1.2+; a self-signed/forged cert is **rejected**
(connection fails) with no `badCertificateCallback` override; NSC/ATS do not
permit cleartext or arbitrary loads.

#### Negative evidence (insecure)
`badCertificateCallback => true` recovered from the snapshot; app accepts your
Burp CA cert with no engine patch (TLS validation off); plaintext API traffic in
the proxy; `NSAllowsArbitraryLoads=true`. Upstream
[MITM / traffic interception context](../../upstream/CheatSheetSeries/cheatsheets/Mobile_Application_Security_Cheat_Sheet.md).

## MASVS-NETWORK-2 — Identity pinning for developer-controlled endpoints

#### Mechanism / sink (Flutter)
Pinning in Flutter is done at the Dart layer (the engine does **not** read
Android NSC `<pin-set>` for Dart sockets):
- `SecurityContext` seeded only with the expected cert, or
- `http_certificate_pinning` / `ssl_pinning_plugin`, or
- a `dio` `badCertificateCallback`/interceptor comparing the leaf/SPKI
  fingerprint.

#### How to test
1. Intercept with a CA the device trusts but that is **not** the pinned one
   (standard Burp CA, no engine patch).
2. **Pinned (secure):** connection fails / app errors even though the CA is
   trusted → pinning is enforced at the Dart layer.
3. Then defeat it: **reFlutter** or Frida `ssl_verify` hook — if traffic now
   flows, pinning had no secondary integrity check (expected for a pentest, note
   it as bypassable without [RESILIENCE](MASVS-RESILIENCE.md) backing).
- MASTG: [MASTG-TEST-0244](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0244.md)/[0385](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0385.md) (missing pinning, dynamic/static),
  [MASTG-TEST-0396](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0396.md)/[0397](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0397.md) (delegate bypassing validation).

#### Positive evidence (secure)
With a trusted-but-unpinned CA, the app refuses to connect to its own backend;
pin is on the leaf/intermediate SPKI; a backup pin exists.

#### Negative evidence (insecure)
Traffic flows through your proxy using the standard CA with **no** engine patch
(no pinning at all); or the "pin" is only a hostname/`badCertificateCallback`
check that your CA satisfies.

---
*Covers MASVS-NETWORK-1/-2. Backend TLS/cert posture and HSTS belong to the API —
[ASVS V12](../_asvs-base/V12-Secure-Communication.md). Defeating pinning as a
control → [RESILIENCE](MASVS-RESILIENCE.md).*
