# MASVS-PLATFORM – Platform Interaction (Flutter)

> **MASVS v2 · Platform Interaction** — projected onto Flutter (Android + iOS).
> Base: [`_masvs-base/MASVS-PLATFORM.md`](../_masvs-base/MASVS-PLATFORM.md).
> Flutter renders its own UI on a single `FlutterActivity`/`FlutterViewController`,
> so the platform attack surface is the **host shell** (manifest/plist, exported
> components, deep links), **platform channels**, and embedded **WebViews**.

## MASVS-PLATFORM-1 — Use IPC mechanisms securely

#### Mechanism / sink (Flutter)
- **Android exported components:** the host `AndroidManifest.xml` —
  `FlutterActivity` or plugin activities/receivers/services/providers with
  `android:exported="true"` and an `intent-filter`. `FileProvider` from
  `image_picker`/`share_plus` with loose `grantUriPermissions`.
- **Deep links / app links:** `uni_links`, `app_links`, `go_router` routing on
  an incoming URL. Flutter commonly maps the deep-link path straight to an
  in-app route → unauthenticated navigation, parameter injection into a route,
  or a WebView fed an attacker URL.
- **Platform channels (`MethodChannel`/`EventChannel`):** the Dart↔native
  bridge. A channel exposed to, or reachable from, other components that passes
  attacker data into a native sink (file path, SQL, intent).

#### How to test
- Enumerate exported components: `jadx`/`apktool` on the manifest; iOS
  `Info.plist` `CFBundleURLTypes` + associated-domains.
- Fire intents / deep links:
  ```sh
  adb shell am start -a android.intent.action.VIEW -d "myapp://account/transfer?to=attacker&amt=1000"
  adb shell am start -n <pkg>/.SomeExportedActivity --es extra "payload"
  # iOS: xcrun simctl openurl booted "myapp://..."
  ```
- Blutter: trace the deep-link handler → which route/params it trusts; inspect
  `MethodChannel` handlers for unvalidated args.
- MASTG: PLATFORM IPC / deep-link tests (android/ios MASVS-PLATFORM) —
  [`_masvs-base/MASVS-PLATFORM.md`](../_masvs-base/MASVS-PLATFORM.md).

#### Positive evidence (secure)
Only intentionally-public activities exported; deep links validate host/path and
require auth for sensitive routes; channel args validated; no secret returned
over a channel reachable by other apps.

#### Negative evidence (insecure)
`myapp://account/transfer?...` drives a privileged in-app action without auth; an
exported activity launches an arbitrary WebView URL; a `MethodChannel` reads an
attacker-controlled file path.

## MASVS-PLATFORM-2 — Use WebViews securely

#### Mechanism / sink (Flutter)
`webview_flutter` / `flutter_inappwebview`:
- `javaScriptMode: JavaScriptMode.unrestricted` + loading attacker-influenced
  content → XSS in the WebView.
- **JS↔native bridges:** `addJavaScriptChannel` / `addJavaScriptHandler`
  exposing native capability to page JS (the classic mobile "JS bridge RCE"
  surface).
- `allowFileAccess`/`allowUniversalAccessFromFileURLs` loading `file://` or
  mixed content.

#### How to test
- Static: find WebView widget config in Blutter — JS mode, channels, URL source,
  file access flags.
- Dynamic: if content/URL is influenceable (deep link, server response), inject
  JS; if a JS channel exists, call it from the page to reach native.
- MASTG: WebView tests under MASVS-PLATFORM; SSL-in-WebView
  [MASTG-TEST-0284](../../upstream/MASTG/tests-beta/android/MASVS-NETWORK/MASTG-TEST-0284.md).
  Upstream [XSS](../../upstream/PayloadsAllTheThings/XSS%20Injection/README.md).

#### Positive / negative evidence
**Secure:** JS disabled unless needed; only trusted HTTPS content; no native
bridge exposed to untrusted pages; file access off.
**Insecure:** injected `<script>` runs in the WebView; a JS channel invokes
native file/storage access from attacker JS; `file://` with universal access.

## MASVS-PLATFORM-3 — Use the UI securely

#### Mechanism / sink (Flutter)
- **Screenshot / app-switcher snapshot:** sensitive screen captured to the task
  thumbnail. Mitigation: `FLAG_SECURE` (Android) / blur on resign-active (iOS) —
  via `flutter_windowmanager`/`secure_application`. Flutter does **not** set
  these by default.
- **Clipboard:** `Clipboard.setData` of secrets (card/OTP/password) → readable
  by other apps.
- **Notifications:** sensitive content (OTP, message body) on the lock screen.
- **Keyboard cache** for secret fields (→ [STORAGE](MASVS-STORAGE.md)).

#### How to test
- Background the app on a sensitive screen → inspect the recents thumbnail
  (Android `/data/system_ce/.../snapshots`, iOS `Library/SplashBoard`).
- Copy a secret in-app → read clipboard from another app / `adb`.
- Observe lock-screen notifications.

#### Positive / negative evidence
**Secure:** sensitive screens blank/blurred in recents (`FLAG_SECURE`); secrets
not placed on the clipboard (or auto-cleared/`sensitive`); notifications redact.
**Insecure:** full PAN visible in the app-switcher snapshot; OTP sitting in the
clipboard; password-screen thumbnail cached.

---
*Covers MASVS-PLATFORM-1/-2/-3. Deep-link params that reach the backend are also
an [ASVS V4](../_asvs-base/V04-API-and-Web-Service.md)/injection concern.*
