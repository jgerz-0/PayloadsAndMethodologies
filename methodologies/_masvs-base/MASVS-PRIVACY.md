# MASVS-PRIVACY – Privacy (MASVS v2)

> **OWASP MASVS v2 · MASVS-PRIVACY** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-PRIVACY-1** | The app minimizes access to sensitive data and resources. | Apps should only request access to the data they absolutely need for their functionality and always with informed consent from the user. This control ensures that apps practice data minimization and restricts access control, reducing the potential impact of data breaches or leaks.  Furthermore, apps should share data with third parties only when necessary, and this should include enforcing that third-party SDKs operate based on user consent, not by default or without it. Apps should prevent third-party SDKs from ignoring consent signals or from collecting data before consent is confirmed.  Additionally, apps should be aware of the 'supply chain' of SDKs they incorporate, ensuring that no data is unnecessarily passed down their chain of dependencies. This end-to-end responsibility for data aligns with recent SBOM regulatory requirements, making apps more accountable for their data practices. |
| **MASVS-PRIVACY-2** | The app prevents identification of the user. | Protecting user identity is crucial. This control emphasizes the use of unlinkability techniques like data abstraction, anonymization and pseudonymization to prevent user identification and tracking.  Another key aspect addressed by this control is to establish technical barriers when employing complex 'fingerprint-like' signals (e.g. device IDs, IP addresses, behavioral patterns) for specific purposes. For instance, a fingerprint used for fraud detection should be isolated and not repurposed for audience measurement in an analytics SDK. This ensures that each data stream serves its intended function without risking user privacy. |
| **MASVS-PRIVACY-3** | The app is transparent about data collection and usage. | Users have the right to know how their data is being used. This control ensures that apps provide clear information about data collection, storage, and sharing practices, including any behavior a user wouldn't reasonably expect, such as background data collection. Apps should also adhere to platform guidelines on data declarations. |
| **MASVS-PRIVACY-4** | The app offers user control over their data. | Users should have control over their data. This control ensures that apps provide mechanisms for users to manage, delete, and modify their data, and change privacy settings as needed (e.g. to revoke consent). Additionally, apps should re-prompt for consent and update their transparency disclosures when they require more data than initially specified. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0206](../../upstream/MASTG/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0206.md) | android | Undeclared PII in Network Traffic Capture | dynamic, network |
| [MASTG-TEST-0254](../../upstream/MASTG/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0254.md) | android | Dangerous App Permissions | static, code |
| [MASTG-TEST-0255](../../upstream/MASTG/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0255.md) | android | Permission Requests Not Minimized |  |
| [MASTG-TEST-0256](../../upstream/MASTG/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0256.md) | android | Missing Permission Rationale |  |
| [MASTG-TEST-0257](../../upstream/MASTG/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0257.md) | android | Not Resetting Unused Permissions |  |
| [MASTG-TEST-0281](../../upstream/MASTG/tests-beta/ios/MASVS-PRIVACY/MASTG-TEST-0281.md) | ios | Undeclared Known Tracking Domains | static, dynamic |
| [MASTG-TEST-0318](../../upstream/MASTG/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0318.md) | android | References to SDK APIs Known to Handle Sensitive User Data | static, code |
| [MASTG-TEST-0319](../../upstream/MASTG/tests-beta/android/MASVS-PRIVACY/MASTG-TEST-0319.md) | android | Runtime Use of SDK APIs Known to Handle Sensitive User Data | dynamic, hooks |
| [MASTG-TEST-0360](../../upstream/MASTG/tests-beta/ios/MASVS-PRIVACY/MASTG-TEST-0360.md) | ios | Purpose String Accuracy for Reachable Protected Resource Access | static, config, manual |
| [MASTG-TEST-0361](../../upstream/MASTG/tests-beta/ios/MASVS-PRIVACY/MASTG-TEST-0361.md) | ios | Runtime Use of Protected Resource APIs Without Accurate Purpose Strings | dynamic, hooks, manual |
| [MASTG-TEST-0362](../../upstream/MASTG/tests-beta/ios/MASVS-PRIVACY/MASTG-TEST-0362.md) | ios | Entitlements for Unjustified Capability Exposure | static, package, manual |
| [MASTG-TEST-0363](../../upstream/MASTG/tests-beta/ios/MASVS-PRIVACY/MASTG-TEST-0363.md) | ios | Runtime Use of Entitlement-Backed APIs for Unjustified Capability Exposure | dynamic, hooks, manual |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
