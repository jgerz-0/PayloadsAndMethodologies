# MASVS-NETWORK – Network Communication (MASVS v2)

> **OWASP MASVS v2 · MASVS-NETWORK** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-NETWORK-1** | The app secures all network traffic according to the current best practices. | Ensuring data privacy and integrity of any data in transit is critical for any app that communicates over the network. This is typically done by encrypting data and authenticating the remote endpoint, as TLS does. However, there are many ways for a developer to disable the platform secure defaults, or bypass them completely by using low-level APIs or third-party libraries. This control ensures that the app is in fact setting up secure connections in any situation. |
| **MASVS-NETWORK-2** | The app performs identity pinning for all remote endpoints under the developer's control. | Instead of trusting all the default root CAs of the framework or device, this control will make sure that only very specific CAs are trusted. This practice is typically called certificate pinning or public key pinning. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0217](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0217.md) | android | Insecure TLS Protocols Explicitly Allowed in Code | static, code |
| [MASTG-TEST-0218](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0218.md) | android | Insecure TLS Protocols in Network Traffic | dynamic, network |
| [MASTG-TEST-0233](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0233.md) | android | Hardcoded HTTP URLs | static, code |
| [MASTG-TEST-0234](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0234.md) | android | Missing Implementation of Server Hostname Verification with SSLSockets | static, code |
| [MASTG-TEST-0235](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0235.md) | android | Android App Configurations Allowing Cleartext Traffic | static, code |
| [MASTG-TEST-0236](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0236.md) | android | Cleartext Traffic Observed on the Network | dynamic, network |
| [MASTG-TEST-0237](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0237.md) | android | Cross-Platform Framework Configurations Allowing Cleartext Traffic | static, code |
| [MASTG-TEST-0238](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0238.md) | android | Runtime Use of Network APIs Transmitting Cleartext Traffic | dynamic, hooks |
| [MASTG-TEST-0239](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0239.md) | android | Using low-level APIs (e.g. Socket) to set up a custom HTTP connection | static, code |
| [MASTG-TEST-0242](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0242.md) | android | Missing Certificate Pinning in Network Security Configuration | static, code |
| [MASTG-TEST-0243](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0243.md) | android | Expired Certificate Pins in the Network Security Configuration | static, code |
| [MASTG-TEST-0244](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0244.md) | android | Missing Certificate Pinning in Network Traffic | dynamic, network |
| [MASTG-TEST-0282](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0282.md) | android | Unsafe Custom Trust Evaluation | static, code, manual |
| [MASTG-TEST-0283](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0283.md) | android | Incorrect Implementation of Server Hostname Verification | static, code, manual |
| [MASTG-TEST-0284](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0284.md) | android | Incorrect SSL Error Handling in WebViews | static, code, manual |
| [MASTG-TEST-0285](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0285.md) | android | Outdated Android Version Allowing Trust in User-Provided CAs | static, code |
| [MASTG-TEST-0286](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0286.md) | android | Network Security Configuration Allowing Trust in User-Provided CAs | static, code |
| [MASTG-TEST-0295](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0295.md) | android | GMS Security Provider Not Updated | static, code |
| [MASTG-TEST-0321](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0321.md) | ios | Hardcoded HTTP URLs | static, code |
| [MASTG-TEST-0322](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0322.md) | ios | App Transport Security Configurations Allowing Cleartext Traffic | static, code, manual |
| [MASTG-TEST-0323](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0323.md) | ios | Uses of Low-Level Networking APIs for Cleartext Traffic | static, code, manual |
| [MASTG-TEST-0342](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0342.md) | ios | References to Weak ATS TLS Policy Exceptions in Info.plist | static, code |
| [MASTG-TEST-0343](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0343.md) | ios | URLSession TLS Protocol Configuration | static, code, manual |
| [MASTG-TEST-0344](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0344.md) | ios | Network.framework TLS Protocol Configuration | static, code, manual |
| [MASTG-TEST-0345](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0345.md) | ios | Embedded or Third-party TLS Stack Configuration | static, code, manual |
| [MASTG-TEST-0348](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0348.md) | ios | Insecure TLS Protocols in Network Traffic | dynamic, network |
| [MASTG-TEST-0385](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0385.md) | ios | Missing Certificate Pinning in ATS | static |
| [MASTG-TEST-0396](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0396.md) | ios | References to URLSessionDelegate Bypassing Certificate Validation | static, code, manual |
| [MASTG-TEST-0397](../../upstream/MASTG/tests-beta/ios/MASVS-NETWORK/MASTG-TEST-0397.md) | ios | References to WKNavigationDelegate Bypassing Certificate Validation | static, code, manual |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
