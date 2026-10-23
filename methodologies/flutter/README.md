# Flutter Mobile Testing Methodology (MASVS v2-aligned)

> Offensive testing methodology for **Flutter** apps (Android + iOS), structured
> 1:1 against the [MASVS v2 base](../_masvs-base/README.md). One page per MASVS
> category; within each, controls are projected onto Flutter with the concrete
> sink/mechanism, **static** (decompile/inspect) and **dynamic** (runtime/
> traffic) steps, tooling, and **positive (secure) vs negative (insecure)
> evidence**.
>
> Generated via the [`create-methodology`](../../.claude/skills/create-methodology/SKILL.md)
> skill from the MASVS base, so coverage tracks the standard. For generic
> procedures it links the upstream MASTG test and the
> [PayloadsAllTheThings](../../upstream/PayloadsAllTheThings/README.md) library
> and focuses on what is *specific to Flutter*.

## Scope: client + backend

A Flutter engagement has **two halves**:

* **This methodology (MASVS)** — the on-device client: storage, crypto, pinning,
  platform interaction, resilience.
* **The backend** — the REST/GraphQL API the app calls is a normal **ASVS**
  target. Test it with the [ASVS base](../_asvs-base/README.md) (and a generated
  backend methodology for its stack). Most *high-impact* findings (authz/IDOR,
  mass assignment, injection) live there — the Flutter client is largely a
  confidentiality/integrity-of-the-client story.

## What makes Flutter different (read first)

Flutter does **not** behave like a native Android/iOS app for the two things
testers rely on most — decompilation and traffic interception:

1. **Dart is AOT-compiled into a native snapshot.** Release builds ship
   `lib/arm64-v8a/libapp.so` (the Dart code+constants, as a VM snapshot) and
   `libflutter.so` (the engine). `jadx`/`apktool` only show the thin
   Java/Kotlin/Obj-C host shell and plugin bridges — **not** your Dart business
   logic. To reverse the Dart you need snapshot-aware tooling:
   [**Blutter**](https://github.com/worawit/blutter) (static, recovers
   functions/objects from `libapp.so`),
   [**reFlutter**](https://github.com/Impact-I/reFlutter) (patches the engine),
   `flutter-spy`, and `strings libapp.so`.
2. **Flutter has its own TLS stack and ignores the system proxy + user CA
   store.** Dart-level HTTP (`dart:io HttpClient`, `package:http`, `dio`) goes
   through the engine's statically-linked **BoringSSL** — it does **not** read
   the device/WiFi proxy, the Android Network Security Config, or iOS ATS trust
   settings for its own sockets. So installing a Burp CA and setting a proxy
   captures **WebView and native-plugin** traffic but shows **nothing** for Dart
   traffic. Intercept it with one of:
   - **reFlutter** — repackages the APK/IPA with a patched engine that forces a
     proxy and disables cert verification (easiest).
   - **Frida** — hook `ssl_crypto_x509_session_verify_cert_chain` in
     `libflutter.so` (e.g. `disable-flutter-tls-verification`,
     `frida-interception-and-unpinning`) + redirect traffic to your proxy with
     a transparent route (`proxydroid`, iptables/`rvictl`, or a VPN like
     PCAPdroid).

Most of this methodology's static steps assume you have run Blutter/reFlutter;
most dynamic steps assume a rooted/jailbroken (or emulator/simulator) device
and Frida/Objection.

## Fingerprinting (quick ref)

| Signal | Tell |
|---|---|
| Is it Flutter? | APK contains `lib/*/libflutter.so` + `lib/*/libapp.so`, `assets/flutter_assets/`; IPA has `Frameworks/Flutter.framework` + `App.framework/App` |
| Flutter/engine version | `strings libflutter.so \| grep -i "flutter_engine\|Dart VM"`; match the Dart snapshot hash to an engine build (reFlutter prints it) |
| Dart snapshot | `App.framework/App` (iOS) / `libapp.so` (Android) — feed to Blutter |
| Obfuscated? | Built with `--obfuscate --split-debug-info` → Blutter output has mangled names, few strings |
| Plugins in use | `pubspec.lock` if leaked; else plugin `.so`/classes in the shell (e.g. `FlutterSecureStoragePlugin`, `LocalAuthPlugin`, `WebViewFlutterPlugin`) |
| Networking lib | `package:http`/`dio`/`chopper` symbols in Blutter output; WebViews imply `webview_flutter`/`flutter_inappwebview` |

## Tooling baseline

* **Unpack/shell:** `apktool`, `jadx`, `unzip`; iOS: `unzip` the IPA, `otool`,
  `class-dump`, `frida-ios-dump`.
* **Dart reversing:** Blutter, reFlutter, `flutter-spy`, `strings`.
* **Dynamic:** Frida + Objection, `disable-flutter-tls-verification` /
  `frida-interception-and-unpinning`, mitmproxy/Burp, PCAPdroid/proxydroid.
* **Static scanners:** [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF)
  (automates a lot of the below), `semgrep` with Dart rules.
* **Storage inspection:** `adb shell run-as <pkg>` / root, `frida-fs`, iOS
  `filemon`/`fsmon`, DB browsers for SQLite/Hive.

## Categories

| MASVS | Flutter page | Dominant Flutter concerns |
|---|---|---|
| MASVS-STORAGE | [STORAGE](MASVS-STORAGE.md) | `shared_preferences`/Hive/sqflite plaintext vs `flutter_secure_storage`; logs; backups; keyboard cache |
| MASVS-CRYPTO | [CRYPTO](MASVS-CRYPTO.md) | `Random` vs `Random.secure`, `encrypt`/`pointycastle` misuse, hardcoded keys in snapshot, ECB/static IV |
| MASVS-AUTH | [AUTH](MASVS-AUTH.md) | `local_auth` biometrics (bypassable), token handling, backend authz is ASVS |
| MASVS-NETWORK | [NETWORK](MASVS-NETWORK.md) | BoringSSL pinning/`badCertificateCallback`, cleartext, interception setup |
| MASVS-PLATFORM | [PLATFORM](MASVS-PLATFORM.md) | platform channels, deep links, WebView JS bridges, screenshot/clipboard leakage |
| MASVS-CODE | [CODE](MASVS-CODE.md) | `minSdk`/deployment target, forced update, vulnerable pub/native deps, input validation |
| MASVS-RESILIENCE | [RESILIENCE](MASVS-RESILIENCE.md) | root/jailbreak detection, Frida/repack detection, `--obfuscate`, anti-debug (R profile) |
| MASVS-PRIVACY | [PRIVACY](MASVS-PRIVACY.md) | permissions/consent, tracker SDKs, device identifiers, data deletion |

## Profiles

Scope by MASVS profile: **L1** baseline (all apps), **L2** defense-in-depth
(sensitive data — finance/health), **R** resilience (anti-reversing/tampering —
only when there's a real threat model: payments, anti-fraud, DRM, games).

## References

* [MASVS v2 base](../_masvs-base/README.md) · [OWASP MAS](https://mas.owasp.org/)
* Backend half: [ASVS 5.0 base](../_asvs-base/README.md)
* [OWASP Mobile App Security Cheat Sheet](../../upstream/CheatSheetSeries/cheatsheets/Mobile_Application_Security_Cheat_Sheet.md)
* Upstream: [PayloadsAllTheThings](../../upstream/PayloadsAllTheThings/README.md)
