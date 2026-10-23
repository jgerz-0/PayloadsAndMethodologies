# MASVS-CRYPTO – Cryptography (MASVS v2)

> **OWASP MASVS v2 · MASVS-CRYPTO** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-CRYPTO-1** | The app employs current strong cryptography and uses it according to industry best practices. | Cryptography plays an especially important role in securing the user's data - even more so in a mobile environment, where attackers having physical access to the user's device is a likely scenario. This control covers general cryptography best practices, which are typically defined in external standards. |
| **MASVS-CRYPTO-2** | The app performs key management according to industry best practices. | Even the strongest cryptography would be compromised by poor key management. This control covers the management of cryptographic keys throughout their lifecycle, including key generation, storage and protection. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0204](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0204.md) | android | Insecure Random API Usage | static, code, manual |
| [MASTG-TEST-0205](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0205.md) | android | Non-random Sources Usage | static, code, manual |
| [MASTG-TEST-0208](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0208.md) | android | Insufficient Key Sizes | static, code |
| [MASTG-TEST-0209](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0209.md) | ios | Insufficient Key Sizes | static, code |
| [MASTG-TEST-0210](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0210.md) | ios | Broken Symmetric Encryption Algorithms | static, code, manual |
| [MASTG-TEST-0211](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0211.md) | ios | Broken Hashing Algorithms | static, code, manual |
| [MASTG-TEST-0212](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0212.md) | android | Use of Hardcoded Cryptographic Keys in Code | static, code |
| [MASTG-TEST-0213](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0213.md) | ios | Use of Hardcoded Cryptographic Keys in Code | static, code, manual |
| [MASTG-TEST-0214](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0214.md) | ios | Hardcoded Cryptographic Keys in Files | static, code, manual |
| [MASTG-TEST-0221](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0221.md) | android | Broken Symmetric Encryption Algorithms | static, code, manual |
| [MASTG-TEST-0232](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0232.md) | android | Broken Symmetric Encryption Modes | static, code, manual |
| [MASTG-TEST-0307](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0307.md) | android | References to Asymmetric Key Pairs Used For Multiple Purposes | static, code |
| [MASTG-TEST-0308](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0308.md) | android | Runtime Use of Asymmetric Key Pairs Used For Multiple Purposes | dynamic, hooks |
| [MASTG-TEST-0309](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0309.md) | android | References to Reused Initialization Vectors in Symmetric Encryption | static, code |
| [MASTG-TEST-0310](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0310.md) | android | Runtime Use of Reused Initialization Vectors in Symmetric Encryption | dynamic, hooks |
| [MASTG-TEST-0311](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0311.md) | ios | Insecure Random API Usage | static, code, manual |
| [MASTG-TEST-0312](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0312.md) | android | References to Explicit Security Provider in Cryptographic APIs | static, code |
| [MASTG-TEST-0317](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0317.md) | ios | Broken Symmetric Encryption Modes | static, code, manual |
| [MASTG-TEST-0349](../../upstream/MASTG/tests-beta/ios/MASVS-CRYPTO/MASTG-TEST-0349.md) | ios | Runtime Use of Insecure Random APIs | dynamic, hooks, manual |
| [MASTG-TEST-0350](../../upstream/MASTG/tests-beta/android/MASVS-CRYPTO/MASTG-TEST-0350.md) | android | Runtime Use of Broken Symmetric Encryption Modes | dynamic, hooks, manual |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
