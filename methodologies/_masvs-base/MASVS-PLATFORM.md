# MASVS-PLATFORM – Platform Interaction (MASVS v2)

> **OWASP MASVS v2 · MASVS-PLATFORM** · Control IDs, statements, and descriptions are verbatim from the official standard.
> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml) · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)
>
> **Role in this repo:** framework-agnostic mobile base (the client-side sibling of the [ASVS base](../_asvs-base/README.md), which covers the backend API). When a mobile methodology is generated (see [`_masvs-base/README.md`](README.md) and the `create-methodology` skill), each control below is projected onto the target stack (e.g. Flutter) as: the concrete mechanism/sink, how to test it (static + dynamic), tooling, and **positive (secure) vs negative (insecure) evidence**.

> **Profiles:** MASVS v2 controls are tested at security-testing *profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an engagement by profile.

## Controls

| Control | Statement | Description |
| :-- | :-- | :-- |
| **MASVS-PLATFORM-1** | The app uses IPC mechanisms securely. | Apps typically use platform provided IPC mechanisms to intentionally expose data or functionality. Both installed apps and the user are able to interact with the app in many different ways. This control ensures that all interactions involving IPC mechanisms happen securely. |
| **MASVS-PLATFORM-2** | The app uses WebViews securely. | WebViews are typically used by apps that have a need for increased control over the UI. This control ensures that WebViews are configured securely to prevent sensitive data leakage as well as sensitive functionality exposure (e.g. via JavaScript bridges to native code). |
| **MASVS-PLATFORM-3** | The app uses the user interface securely. | Sensitive data has to be displayed in the UI in many situations (e.g. passwords, credit card details, OTP codes in notifications). This control ensures that this data doesn't end up being unintentionally leaked due to platform mechanisms such as auto-generated screenshots or accidentally disclosed via e.g. shoulder surfing or sharing the device with another person. |

## MASTG v2 tests covering this category

Concrete testing procedures from the MAS Testing Guide (live V2 tests). Each links to the upstream procedure with commands/evidence.

| MASTG test | Platform | Title | Type |
| :-- | :-- | :-- | :-- |
| [MASTG-TEST-0250](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0250.md) | android | References to Content Provider Access in WebViews | static, code |
| [MASTG-TEST-0251](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0251.md) | android | Runtime Use of Content Provider Access APIs in WebViews | dynamic, hooks, manual |
| [MASTG-TEST-0252](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0252.md) | android | References to Local File Access in WebViews | static, code |
| [MASTG-TEST-0253](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0253.md) | android | Runtime Use of Local File Access APIs in WebViews | dynamic, hooks, manual |
| [MASTG-TEST-0258](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0258.md) | android | References to Keyboard Caching Attributes in UI Elements | static, code |
| [MASTG-TEST-0276](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0276.md) | ios | Use of the iOS General Pasteboard | static, code, manual |
| [MASTG-TEST-0277](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0277.md) | ios | Sensitive Data in the iOS General Pasteboard at Runtime | dynamic, hooks |
| [MASTG-TEST-0278](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0278.md) | ios | Pasteboard Contents Not Cleared After Use | static, code |
| [MASTG-TEST-0279](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0279.md) | ios | Pasteboard Contents Not Expiring | static, code |
| [MASTG-TEST-0280](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0280.md) | ios | Pasteboard Contents Not Restricted to Local Device | static, code |
| [MASTG-TEST-0289](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0289.md) | android | Runtime Verification of Sensitive Content Exposure in Screenshots During App Backgrounding | dynamic, filesystem, manual |
| [MASTG-TEST-0290](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0290.md) | ios | Runtime Verification of Sensitive Content Exposure in Screenshots During App Backgrounding | dynamic, filesystem |
| [MASTG-TEST-0291](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0291.md) | android | References to Screen Capturing Prevention APIs | static, code |
| [MASTG-TEST-0292](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0292.md) | android | `setRecentsScreenshotEnabled` Not Used to Prevent Screenshots When Backgrounded | static, code |
| [MASTG-TEST-0293](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0293.md) | android | `setSecure` Not Used to Prevent Screenshots in SurfaceViews | static, code |
| [MASTG-TEST-0294](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0294.md) | android | `SecureOn` Not Used to Prevent Screenshots in Compose Dialogs | static, code |
| [MASTG-TEST-0315](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0315.md) | android | Sensitive Data Exposed via Notifications | static, code |
| [MASTG-TEST-0316](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0316.md) | android | App Exposing User Authentication Data in Text Input Fields | static, code, manual |
| [MASTG-TEST-0320](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0320.md) | android | WebViews Not Cleaning Up Sensitive Data | dynamic, hooks |
| [MASTG-TEST-0331](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0331.md) | ios | Use of Deprecated WebView APIs | static, code |
| [MASTG-TEST-0332](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0332.md) | ios | Attacker-Controlled URI in WebViews | static, code, manual |
| [MASTG-TEST-0333](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0333.md) | ios | Overly Broad File Read Access in WebViews | static, code, manual |
| [MASTG-TEST-0334](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0334.md) | android | Native Code Exposed Through WebViews | static, code, manual |
| [MASTG-TEST-0335](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0335.md) | ios | WebView File Origin Access Relaxed by Configuration | static, code, manual |
| [MASTG-TEST-0336](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0336.md) | ios | Runtime Setting of Relaxed WebView File Origin Policies | dynamic, hooks, manual |
| [MASTG-TEST-0340](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0340.md) | android | References to Overlay Attack Protections | static, code |
| [MASTG-TEST-0346](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0346.md) | ios | References to APIs Hiding Sensitive Data in Text Input Fields | static, code, manual |
| [MASTG-TEST-0347](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0347.md) | ios | Runtime Use of APIs Hiding Sensitive Data in Text Input Fields | dynamic, hooks |
| [MASTG-TEST-0355](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0355.md) | android | References to Unauthorized Database Access through Content Providers | static, config, manual |
| [MASTG-TEST-0356](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0356.md) | android | Runtime Verification of Unauthorized Database Access through Content Providers | dynamic, filesystem, manual |
| [MASTG-TEST-0357](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0357.md) | android | References to Oversharing of File-Based Content Providers | static, config, code, manual |
| [MASTG-TEST-0364](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0364.md) | android | Exported And Unprotected Activities That Expose Sensitive Functionality | static, config, code, manual |
| [MASTG-TEST-0365](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0365.md) | android | Exported And Unprotected Services That Expose Sensitive Functionality | static, config, code, manual |
| [MASTG-TEST-0366](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0366.md) | android | Exported And Unprotected Broadcast Receivers That Expose Sensitive Functionality | static, config, code, manual |
| [MASTG-TEST-0370](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0370.md) | ios | Missing Input Validation in Custom URL Scheme Handlers | static, code |
| [MASTG-TEST-0371](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0371.md) | ios | Missing Source Validation in Custom URL Scheme Handlers | static, code |
| [MASTG-TEST-0376](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0376.md) | ios | References to Native Bridge APIs in WebViews | static, code |
| [MASTG-TEST-0377](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0377.md) | ios | References to `evaluateJavaScript` Used as Bridge Reply in `WKScriptMessageHandler` | static, code, manual |
| [MASTG-TEST-0378](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0378.md) | ios | References to Password Fields in WebView-Loaded HTML | static, code, manual |
| [MASTG-TEST-0379](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0379.md) | ios | References to `evaluateJavaScript` Without Content World Isolation | static, code |
| [MASTG-TEST-0380](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0380.md) | ios | References to `evaluateJavaScript` Writing Sensitive Data into WebView DOM | static, code, manual |
| [MASTG-TEST-0381](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0381.md) | android | References to Insecure PendingIntent Creation | static |
| [MASTG-TEST-0389](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0389.md) | ios | References to the App-Wide Restriction of Custom Keyboards | static, code, manual |
| [MASTG-TEST-0390](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0390.md) | ios | Full Access Requested by a Custom Keyboard Extension | static, code, manual |
| [MASTG-TEST-0393](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0393.md) | android | Use of Unverified App Links | static, config |
| [MASTG-TEST-0394](../../upstream/MASTG/tests-beta/android/MASVS-PLATFORM/MASTG-TEST-0394.md) | android | Missing Input Validation in Custom URL Scheme Handlers | static, code, manual |
| [MASTG-TEST-0395](../../upstream/MASTG/tests-beta/ios/MASVS-PLATFORM/MASTG-TEST-0395.md) | ios | Missing Input Validation in Universal Link Handlers | static, code, manual |

---

### Framework / app projection (filled per stack, not here)

This base page lists *what* must hold for the mobile client. A generated mobile methodology page answers *how to test it on that stack*. For each control above, the generated page should provide, where testable:

- **Mechanism / sink** — the platform or framework API, storage location, config, or code pattern that satisfies or violates the control.
- **How to test** — concrete **static** (decompile / source / manifest) and **dynamic** (runtime, instrumentation, traffic) steps, with tooling and commands.
- **Positive evidence (secure)** — what a correctly-built app shows.
- **Negative evidence (insecure)** — the confirmation signal for the finding.
