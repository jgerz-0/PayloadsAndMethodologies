# MASVS-STORAGE – Storage (MASVS v2)

> **OWASP MASVS v2 · MASVS-STORAGE** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-STORAGE-1** | The app securely stores sensitive data. | Apps handle sensitive data coming from many sources such as the user, the backend, system services or other apps on the device and usually need to store it locally. The storage locations may be private to the app (e.g. its internal storage) or be public and therefore accessible by the user or other installed apps (e.g. public folders such as Downloads). This control ensures that any sensitive data that is intentionally stored by the app is properly protected independently of the target location. |
| **MASVS-STORAGE-2** | The app prevents leakage of sensitive data. | There are cases when sensitive data is unintentionally stored or exposed to publicly accessible locations; typically as a side-effect of using certain APIs, system capabilities such as backups or logs. This control covers this kind of unintentional leaks where the developer actually has a way to prevent it. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0200](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0200.md) | android | Files Written to External Storage | dynamic, filesystem, manual |
| [MASTG-TEST-0201](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0201.md) | android | Runtime Use of APIs to Access External Storage | dynamic, hooks, manual |
| [MASTG-TEST-0202](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0202.md) | android | References to APIs and Permissions for Accessing External Storage | static, code, manual |
| [MASTG-TEST-0203](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0203.md) | android | Runtime Use of Logging APIs | dynamic, hooks |
| [MASTG-TEST-0207](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0207.md) | android | Runtime Storage of Unencrypted Data in the App Sandbox | dynamic, filesystem |
| [MASTG-TEST-0215](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0215.md) | ios | Sensitive Data Not Marked For Backup Exclusion | static, code |
| [MASTG-TEST-0216](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0216.md) | android | Sensitive Data Not Excluded From Backup | dynamic, filesystem |
| [MASTG-TEST-0231](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0231.md) | android | References to Logging APIs | static, code |
| [MASTG-TEST-0262](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0262.md) | android | References to Backup Configurations Not Excluding Sensitive Data | static, code |
| [MASTG-TEST-0287](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0287.md) | android | Runtime Storage of Unencrypted Data via the SharedPreferences API | dynamic, hooks, manual |
| [MASTG-TEST-0296](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0296.md) | ios | Sensitive Data Exposure in Logs | dynamic, logs |
| [MASTG-TEST-0297](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0297.md) | ios | Sensitive Data Exposure Through Logging APIs | static, code |
| [MASTG-TEST-0298](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0298.md) | ios | Runtime Monitoring of Files Eligible for Backup | dynamic, hooks |
| [MASTG-TEST-0299](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0299.md) | ios | Data Protection Classes for Files in Private Storage | dynamic, filesystem |
| [MASTG-TEST-0300](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0300.md) | ios | References to APIs for Storing Unencrypted Data in Private Storage | static, code |
| [MASTG-TEST-0301](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0301.md) | ios | Runtime Use of APIs for Storing Unencrypted Data in Private Storage | dynamic, hooks |
| [MASTG-TEST-0302](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0302.md) | ios | Sensitive Data Unencrypted in Private Storage Files | dynamic, filesystem |
| [MASTG-TEST-0303](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0303.md) | ios | References to APIs for Storing Unencrypted Data in Shared Storage | static, code |
| [MASTG-TEST-0304](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0304.md) | android | References to Sensitive Data Unencrypted via Android Room Database | static, code |
| [MASTG-TEST-0305](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0305.md) | android | Sensitive Data Stored Unencrypted via DataStore | static, dynamic |
| [MASTG-TEST-0306](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0306.md) | android | References to Sensitive Data Stored Unencrypted via Android Room DB | static, code |
| [MASTG-TEST-0313](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0313.md) | ios | References to APIs for Preventing Keyboard Caching of Text Fields | static, code, manual |
| [MASTG-TEST-0314](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0314.md) | ios | Runtime Monitoring of Text Fields Eligible for Keyboard Caching | dynamic, hooks |
| [MASTG-TEST-0388](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0388.md) | ios | References to Sensitive Data Stored Unprotected in Shared App Group Containers | static, code, manual |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
