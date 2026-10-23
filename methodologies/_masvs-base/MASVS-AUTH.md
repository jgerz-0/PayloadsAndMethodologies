# MASVS-AUTH – Authentication and Authorization (MASVS v2)

> **OWASP MASVS v2 · MASVS-AUTH** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-AUTH-1** | The app uses secure authentication and authorization protocols and follows the relevant best practices. | Most apps connecting to a remote endpoint require user authentication and also enforce some kind of authorization. While the enforcement of these mechanisms must be on the remote endpoint, the apps also have to ensure that it follows all the relevant best practices to ensure a secure use of the involved protocols. |
| **MASVS-AUTH-2** | The app performs local authentication securely according to the platform best practices. | Many apps allow users to authenticate via biometrics or a local PIN code. These authentication mechanisms need to be correctly implemented. Additionally, some apps might not have a remote endpoint, and rely fully on local app authentication. |
| **MASVS-AUTH-3** | The app secures sensitive operations with additional authentication. | Some additional form of authentication is often desirable for sensitive actions inside the app. This can be done in different ways (biometric, pin, MFA code generator, email, deep links, etc) and they all need to be implemented securely. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0266](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0266.md) | ios | References to APIs for Event-Bound Biometric Authentication | static, code |
| [MASTG-TEST-0267](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0267.md) | ios | Runtime Use Of Event-Bound Biometric Authentication | dynamic, hooks |
| [MASTG-TEST-0268](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0268.md) | ios | References to APIs Allowing Fallback to Non-Biometric Authentication | static, code |
| [MASTG-TEST-0269](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0269.md) | ios | Runtime Use Of APIs Allowing Fallback to Non-Biometric Authentication | dynamic, hooks |
| [MASTG-TEST-0270](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0270.md) | ios | References to APIs Detecting Biometric Enrollment Changes | static, code |
| [MASTG-TEST-0271](../../upstream/MASTG/tests-beta/ios/MASVS-AUTH/MASTG-TEST-0271.md) | ios | Runtime Use Of APIs Detecting Biometric Enrollment Changes | dynamic, hooks |
| [MASTG-TEST-0326](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0326.md) | android | References to APIs Allowing Fallback to Non-Biometric Authentication | static, code |
| [MASTG-TEST-0327](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0327.md) | android | References to APIs for Event-Bound Biometric Authentication | static, code |
| [MASTG-TEST-0328](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0328.md) | android | References to APIs Detecting Biometric Enrollment Changes | static, code |
| [MASTG-TEST-0329](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0329.md) | android | References to APIs Enforcing Authentication without Explicit User Action | static, code |
| [MASTG-TEST-0330](../../upstream/MASTG/tests-beta/android/MASVS-AUTH/MASTG-TEST-0330.md) | android | References to APIs for Keys used in Biometric Authentication with Extended Validity Duration | static, code |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
