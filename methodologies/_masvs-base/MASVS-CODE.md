# MASVS-CODE – Code Quality (MASVS v2)

> **OWASP MASVS v2 · MASVS-CODE** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-CODE-1** | The app requires an up-to-date platform version. | Every release of the mobile OS includes security patches and new security features. By supporting older versions, apps stay vulnerable to well-known threats. This control ensures that the app is running on an up-to-date platform version so that users have the latest security protections. |
| **MASVS-CODE-2** | The app has a mechanism for enforcing app updates. | Sometimes critical vulnerabilities are discovered in the app when it is already in production. This control ensures that there is a mechanism to force the users to update the app before they can continue using it. |
| **MASVS-CODE-3** | The app only uses software components without known vulnerabilities. | To be truly secure, a full whitebox assessment should have been performed on all app components. However, as it usually happens with e.g. for third-party components this is not always feasible and not typically part of a penetration test. This control covers "low-hanging fruit" cases, such as those that can be detected just by scanning libraries for known vulnerabilities. |
| **MASVS-CODE-4** | The app validates and sanitizes all untrusted inputs. | Apps have many data entry points including the UI, IPC, the network, the file system, etc. This incoming data might have been inadvertently modified by untrusted actors and may lead to bypass of critical security checks as well as classical injection attacks such as SQL injection, XSS or insecure deserialization. This control ensures that this data is treated as untrusted input and is properly verified and sanitized before it's used. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0222](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0222.md) | android | Position Independent Code (PIC) Not Enabled | static, code |
| [MASTG-TEST-0223](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0223.md) | android | Stack Canaries Not Enabled | static, code |
| [MASTG-TEST-0228](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0228.md) | ios | Position Independent Code (PIC) not Enabled | static, code |
| [MASTG-TEST-0229](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0229.md) | ios | Stack Canaries Not enabled | static, code |
| [MASTG-TEST-0230](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0230.md) | ios | Automatic Reference Counting (ARC) not enabled | static, code |
| [MASTG-TEST-0245](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0245.md) | android | References to Platform Version APIs | static, code |
| [MASTG-TEST-0272](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0272.md) | android | Identify Dependencies with Known Vulnerabilities in the Android Project | static, code |
| [MASTG-TEST-0273](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0273.md) | ios | Identify Dependencies with Known Vulnerabilities by Scanning Dependency Managers Artifacts | static, code |
| [MASTG-TEST-0274](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0274.md) | android | Dependencies with Known Vulnerabilities in the App's SBOM | static, developer |
| [MASTG-TEST-0275](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0275.md) | ios | Dependencies with Known Vulnerabilities in the App's SBOM | static, developer |
| [MASTG-TEST-0337](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0337.md) | android | References to Object Deserialization of Untrusted Data | static, code |
| [MASTG-TEST-0339](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0339.md) | android | SQL Injection in Content Providers | static, code |
| [MASTG-TEST-0372](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0372.md) | android | Implicit Intents Used for Internal App Communication | static, code, manual |
| [MASTG-TEST-0374](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0374.md) | android | References to Implicit Intents Carrying Sensitive Extras | static, code, manual |
| [MASTG-TEST-0375](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0375.md) | android | Missing Validation of Data Returned from Implicit Intents | dynamic, hooks, manual |
| [MASTG-TEST-0382](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0382.md) | android | Runtime Use of Enforced Updating APIs | dynamic, network, hooks, manual |
| [MASTG-TEST-0383](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0383.md) | ios | References to Enforced Updating APIs | static, code, manual |
| [MASTG-TEST-0384](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0384.md) | ios | Runtime Use of Enforced Updating APIs | dynamic, network, hooks, manual |
| [MASTG-TEST-0386](../../upstream/MASTG/tests-beta/ios/MASVS-CODE/MASTG-TEST-0386.md) | ios | References to Object Deserialization of Untrusted Data | static, code, manual |
| [MASTG-TEST-0392](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0392.md) | android | References to Enforced Updating APIs | static, code, manual |
| [MASTG-TEST-0398](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0398.md) | android | References to WebViewClient URL Loading Handlers | static, code, manual |
| [MASTG-TEST-0399](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0399.md) | android | SafeBrowsing Disabled | static, config, code |
| [MASTG-TEST-0400](../../upstream/MASTG/tests-beta/android/MASVS-CODE/MASTG-TEST-0400.md) | android | Runtime Use of WebViewClient URL Loading Handlers | dynamic, hooks, manual |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
