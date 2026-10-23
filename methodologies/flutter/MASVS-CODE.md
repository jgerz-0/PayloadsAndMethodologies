# MASVS-CODE – Code Quality (Flutter)

> **MASVS v2 · Code Quality** — projected onto Flutter (Android + iOS).
> Base: [`_masvs-base/MASVS-CODE.md`](../_masvs-base/MASVS-CODE.md).
> Platform floor, forced-update, vulnerable dependencies (pub + native), and
> untrusted-input handling at the app's many entry points.

## MASVS-CODE-1 — Requires an up-to-date platform version

#### Mechanism / sink (Flutter)
`android/app/build.gradle` `minSdkVersion` (Flutter's current floor is low by
default) and iOS `IPHONEOS_DEPLOYMENT_TARGET`. Supporting very old OSes keeps
the app on platforms missing security features (e.g. Keystore StrongBox,
scoped storage, modern TLS).

#### How to test
- Static: read `minSdkVersion` (manifest `uses-sdk`) and the iOS deployment
  target (`Info.plist` `MinimumOSVersion`).
- MASTG: MASVS-CODE platform-version tests.

#### Positive / negative evidence
**Secure:** `minSdk` ≥ a currently-supported Android API with the security
features the app relies on; iOS target recent. **Insecure:** `minSdk 19`/iOS 10
while the app relies on StrongBox/biometric-bound keys that don't exist there.

## MASVS-CODE-2 — Mechanism for enforcing app updates

#### Mechanism / sink (Flutter)
A forced-update gate (server returns min-supported version; app blocks until
updated), often via `upgrader`/`in_app_update`/`new_version_plus` or a custom
version check against the backend.

#### How to test
Spoof an old client version in the version-check request (intercept) and see if
the app still proceeds; confirm the gate is **server-driven**, not a Dart
constant that can be patched out.

#### Positive / negative evidence
**Secure:** server rejects/soft-blocks unsupported client versions; the gate
can't be skipped by editing the response alone. **Insecure:** no version floor,
or the check is purely client-side and bypassable.

## MASVS-CODE-3 — Only components without known vulnerabilities

#### Mechanism / sink (Flutter)
Two dependency planes:
- **Dart/pub packages** — `pubspec.lock` pins versions; outdated/abandoned
  packages with CVEs.
- **Native deps** — plugin `.so`/frameworks and the **Flutter engine version**
  itself (`libflutter.so`); older engines bundle older BoringSSL/skia with known
  issues.

#### How to test
- If source/`pubspec.lock` available: `flutter pub outdated`,
  `dart pub audit` (OSV), cross-check against advisories.
- Black-box: identify the engine/plugin versions from the binary
  ([fingerprinting](README.md#fingerprinting-quick-ref)) and map to known CVEs;
  MobSF flags vulnerable native libs.
- MASTG: MASVS-CODE dependency tests. Upstream
  [CVE Exploits](../../upstream/PayloadsAllTheThings/CVE%20Exploits/README.md).

#### Positive / negative evidence
**Secure:** recent engine + patched packages, no advisory hits. **Insecure:** a
pinned package or the Flutter engine version maps to a public CVE.

## MASVS-CODE-4 — Validate and sanitize untrusted input

#### Mechanism / sink (Flutter)
Entry points: deep-link/route params ([PLATFORM](MASVS-PLATFORM.md)), platform
channels, WebView messages, files, and **API responses**. Dart's memory safety
removes classic native overflows, but injection reappears when Dart passes input
to a sink:
- `sqflite` **raw SQL** (`rawQuery('... $userInput')`) → SQL injection in the
  local DB.
- WebView HTML built from input → XSS ([PLATFORM](MASVS-PLATFORM.md)).
- Path built from input for `dart:io` `File(...)` → local path traversal.
- Deserializing untrusted JSON/data into privileged objects without validation.

#### How to test
- Static (Blutter): find `rawQuery`/`rawInsert` with interpolation, `File()`
  paths from params, `jsonDecode` feeding trusted logic.
- Dynamic: send injection payloads via the reachable entry point (deep link,
  channel, API response you control via MITM).
- **Payload (local SQLi):** a text field / param like `x' OR '1'='1`.
- **Payload (path traversal):** `../../databases/secret.db` into a file param.
- MASTG: MASVS-CODE injection/input tests. Upstream
  [SQLi](../../upstream/PayloadsAllTheThings/SQL%20Injection/README.md),
  [Directory Traversal](../../upstream/PayloadsAllTheThings/Directory%20Traversal/README.md).

#### Positive / negative evidence
**Secure:** parameterized `sqflite` queries (`whereArgs`), validated/allow-listed
route params and file paths, encoded WebView content. **Insecure:** injected SQL
alters the local query result; `../` escapes the sandbox dir; attacker JSON flips
an authorization field the client trusts.

---
*Covers MASVS-CODE-1/-2/-3/-4. Server-side validation of the same inputs is
[ASVS V1/V2](../_asvs-base/V01-Encoding-and-Sanitization.md).*
