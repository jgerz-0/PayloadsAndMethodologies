# MASVS-RESILIENCE – Resilience Against Reverse Engineering and Tampering (MASVS v2)

> **OWASP MASVS v2 · MASVS-RESILIENCE** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-RESILIENCE-1** | The app validates the integrity of the platform. | Running on a platform that has been tampered with can be very dangerous for apps, as this may disable certain security features, putting the data of the app at risk. Trusting the platform is essential for many of the MASVS controls relying on the platform being secure (e.g. secure storage, biometrics, sandboxing, etc.). This control tries to validate that the OS has not been compromised and its security features can thus be trusted. |
| **MASVS-RESILIENCE-2** | The app implements anti-tampering mechanisms. | Apps run on a user-controlled device, and without proper protections it's relatively easy to run a modified version locally (e.g. to cheat in a game, or enable premium features without paying), or upload a backdoored version of it to third-party app stores. This control tries to ensure the integrity of the app's intended functionality by preventing modifications to the original code and resources. |
| **MASVS-RESILIENCE-3** | The app implements anti-static analysis mechanisms. | Understanding the internals of an app is typically the first step towards tampering with it (either dynamically, or statically). This control tries to impede comprehension by making it as difficult as possible to figure out how an app works using static analysis. |
| **MASVS-RESILIENCE-4** | The app implements anti-dynamic analysis techniques. | Sometimes pure static analysis is very difficult and time consuming so it typically goes hand in hand with dynamic analysis. Observing and manipulating an app during runtime makes it much easier to decipher its behavior. This control aims to make it as difficult as possible to perform dynamic analysis, as well as prevent dynamic instrumentation which could allow an attacker to modify the code at runtime. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0219](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0219.md) | ios | Testing for Debugging Symbols | static, code |
| [MASTG-TEST-0220](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0220.md) | ios | Usage of Outdated Code Signature Format | static, code |
| [MASTG-TEST-0224](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0224.md) | android | Usage of Insecure APK Signature Version | static, code |
| [MASTG-TEST-0225](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0225.md) | android | Usage of Insecure APK Signature Key Size | static, code |
| [MASTG-TEST-0226](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0226.md) | android | Debuggable Flag Enabled in the AndroidManifest | static, code |
| [MASTG-TEST-0227](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0227.md) | android | Debugging Enabled for WebViews | static, code |
| [MASTG-TEST-0240](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0240.md) | ios | Jailbreak Detection in Code | static, code |
| [MASTG-TEST-0241](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0241.md) | ios | Runtime Use of Jailbreak Detection Techniques | dynamic, hooks |
| [MASTG-TEST-0246](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0246.md) | ios | Runtime Use of Secure Screen Lock Detection APIs | dynamic, hooks |
| [MASTG-TEST-0247](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0247.md) | android | References to APIs for Detecting Secure Screen Lock | static, code |
| [MASTG-TEST-0248](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0248.md) | ios | References to APIs for Detecting Secure Screen Lock | static, code |
| [MASTG-TEST-0249](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0249.md) | android | Runtime Use of Secure Screen Lock Detection APIs | dynamic, hooks |
| [MASTG-TEST-0261](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0261.md) | ios | Debuggable Entitlement Enabled in the entitlements.plist | static, code |
| [MASTG-TEST-0263](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0263.md) | android | Logging of StrictMode Violations | dynamic, logs |
| [MASTG-TEST-0264](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0264.md) | android | Runtime Use of StrictMode APIs | dynamic, hooks |
| [MASTG-TEST-0265](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0265.md) | android | References to StrictMode APIs | static, code |
| [MASTG-TEST-0288](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0288.md) | android | Debugging Symbols in Native Binaries | static, code |
| [MASTG-TEST-0324](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0324.md) | android | References to Root Detection Mechanisms | static, code |
| [MASTG-TEST-0325](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0325.md) | android | Runtime Use of Root Detection Techniques | dynamic, hooks |
| [MASTG-TEST-0338](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0338.md) | android | References to Storage Integrity Check APIs | static, code, manual |
| [MASTG-TEST-0341](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0341.md) | android | Runtime Use of Hook Detection Techniques | dynamic, hooks |
| [MASTG-TEST-0351](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0351.md) | android | Runtime Use of Emulator Detection Techniques | dynamic, hooks |
| [MASTG-TEST-0352](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0352.md) | android | References to Debugging Detection APIs | static, code, manual |
| [MASTG-TEST-0353](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0353.md) | android | Runtime Use of Debugging Detection APIs | dynamic, hooks, manual |
| [MASTG-TEST-0354](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0354.md) | ios | Runtime Use of Hook Detection Techniques | dynamic, hooks |
| [MASTG-TEST-0358](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0358.md) | ios | Implementation Details Exposure Through Logging APIs | static, code |
| [MASTG-TEST-0359](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0359.md) | ios | Implementation Details Exposure in Logs | dynamic, logs |
| [MASTG-TEST-0367](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0367.md) | ios | Runtime Use of Virtual Device Detection Techniques | dynamic |
| [MASTG-TEST-0368](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0368.md) | android | Insufficient Obfuscation of Security-Relevant Java/Kotlin Code | static, code, manual |
| [MASTG-TEST-0369](../../upstream/MASTG/tests-beta/android/MASVS-RESILIENCE/MASTG-TEST-0369.md) | android | Insufficient Obfuscation of Security-Relevant Native Code | static, package, manual |
| [MASTG-TEST-0387](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0387.md) | ios | References to Storage Integrity Check APIs | static, code, manual |
| [MASTG-TEST-0391](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0391.md) | ios | Insufficient Obfuscation of Security-Relevant Native Code | static, package, manual |
| [MASTG-TEST-0401](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0401.md) | ios | References to Debugging Detection APIs | static, code, manual |
| [MASTG-TEST-0402](../../upstream/MASTG/tests-beta/ios/MASVS-RESILIENCE/MASTG-TEST-0402.md) | ios | Runtime Use of Debugging Detection APIs | dynamic, hooks, manual |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
