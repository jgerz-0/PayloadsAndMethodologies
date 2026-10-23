# MASVS-RESILIENCE – Reverse Engineering & Tampering (Flutter)

> **MASVS v2 · Resilience** — projected onto Flutter (Android + iOS).
> Base: [`_masvs-base/MASVS-RESILIENCE.md`](../_masvs-base/MASVS-RESILIENCE.md).
> This is the **`R` profile** — only in scope when the app has a real
> anti-tampering/anti-fraud/DRM threat model (payments, banking, games). Test
> these as **controls to defeat**, and treat *absence* as a resilience gap, not
> a vulnerability in itself.

> **Flutter reality:** by default Flutter gives you *some* reversing friction
> for free (Dart AOT snapshot that standard decompilers can't read — see
> [README](README.md#what-makes-flutter-different-read-first)), but **no**
> runtime self-defense. Root/jailbreak, Frida, and repackaging detection only
> exist if a plugin adds them (`freerasp`, `flutter_jailbreak_detection`,
> `safe_device`) or via native code.

## MASVS-RESILIENCE-1 — Validate platform integrity (root/jailbreak)

#### Mechanism / sink (Flutter)
Root/jailbreak detection via `flutter_jailbreak_detection`, `freerasp`,
`safe_device`, or native checks (su binaries, Magisk, Cydia, suspicious mounts).

#### How to test
Run on a rooted/jailbroken device. Then try to defeat detection: Magisk
DenyList/Shamiko, `frida` hooks on the detection methods, or patch the check in
the repackaged app.
- MASTG: MASVS-RESILIENCE platform-integrity tests
  ([`_masvs-base/MASVS-RESILIENCE.md`](../_masvs-base/MASVS-RESILIENCE.md)).

#### Positive / negative evidence
**Resilient:** app detects root/jailbreak and refuses or degrades, and detection
survives trivial Frida/hiding attempts (multiple, native-side checks).
**Gap:** no detection (runs freely on rooted device), or a single Dart boolean
check that one Frida hook flips.

## MASVS-RESILIENCE-2 — Anti-tampering

#### Mechanism / sink (Flutter)
Integrity verification: APK signature check, Play Integrity / App Attest,
checksum of `libapp.so`/assets, detection of repackaging (reFlutter *modifies*
the engine — a good integrity check notices).

#### How to test
- Repackage: `apktool d`/`b` + re-sign, or install a **reFlutter**-patched
  build, and see if the app still runs.
- Check for Play Integrity / DeviceCheck/App Attest calls (static + intercept
  the attestation request).

#### Positive / negative evidence
**Resilient:** resigned/repackaged or reFlutter'd build is detected (refuses to
run / backend rejects via attestation). **Gap:** reFlutter build runs normally
(no integrity check) — which is also why interception usually "just works".

## MASVS-RESILIENCE-3 — Anti-static-analysis (obfuscation)

#### Mechanism / sink (Flutter)
`flutter build --obfuscate --split-debug-info=...` renames Dart symbols and
strips the mapping. Without it, Blutter recovers clean function/class names and
strings.

#### How to test
Run Blutter / `strings libapp.so`: are business-logic symbols and string
literals (URLs, keys, feature names) readable? Check for a `--split-debug-info`
symbol file shipped by accident.

#### Positive / negative evidence
**Resilient:** `--obfuscate` applied — Blutter output is mangled, few meaningful
strings. **Gap:** full symbol names, endpoint URLs, secret-looking strings, and
logic plainly recoverable from the snapshot.

## MASVS-RESILIENCE-4 — Anti-dynamic-analysis (anti-debug / anti-hook)

#### Mechanism / sink (Flutter)
Detection of Frida/debuggers/emulators via `freerasp`/native (open ports 27042,
`frida` in maps, `ptrace`, `TracerPid`, emulator artifacts).

#### How to test
Attach Frida/Objection, run on an emulator, attach a debugger — observe whether
the app detects and reacts; then bypass (rename frida-server, non-default port,
hook the detection, `gum`/stalker evasion).
- MASTG: MASVS-RESILIENCE anti-debug/anti-hook tests.

#### Positive / negative evidence
**Resilient:** Frida attach / emulator / debugger detected and the app
exits/degrades, with layered checks. **Gap:** Frida attaches and hooks freely,
app runs on an emulator, no `TracerPid`/port checks — the whole dynamic
methodology in these pages runs unimpeded.

---
*Covers MASVS-RESILIENCE-1/-4. These controls protect the *other* categories;
bypassing them is often the prerequisite for the STORAGE/NETWORK/AUTH tests
above, so document which bypass each required.*
