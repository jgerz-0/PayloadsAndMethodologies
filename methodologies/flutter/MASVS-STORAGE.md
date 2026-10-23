# MASVS-STORAGE – Storage (Flutter)

> **MASVS v2 · Storage** — projected onto Flutter (Android + iOS).
> Base: [`_masvs-base/MASVS-STORAGE.md`](../_masvs-base/MASVS-STORAGE.md).
> The dominant Flutter finding is **sensitive data in a plaintext plugin store**
> (`shared_preferences`, Hive, sqflite) where `flutter_secure_storage` was
> required.

## MASVS-STORAGE-1 — The app securely stores sensitive data

#### Mechanism / sink (Flutter)
Plugin determines the on-disk protection:

| Plugin | Android location | iOS location | Encrypted? |
|---|---|---|---|
| `shared_preferences` | `shared_prefs/<pkg>_preferences.xml` | `NSUserDefaults` plist | **No** — cleartext |
| `hive`/`hive_flutter` (unencrypted box) | `app_flutter/*.hive` | `Documents/*.hive` | **No** unless `HiveAesCipher` |
| `sqflite` / `drift` / `isar` | `databases/*.db` | `Documents/*.db` | **No** unless SQLCipher |
| `path_provider` temp/app docs | `files/`, `cache/` | `Documents/`, `tmp/` | **No** |
| `flutter_secure_storage` | Keystore-backed `EncryptedSharedPreferences` | **Keychain** | **Yes** |

#### How to test
- **Static (Blutter):** find storage calls in `libapp.so` — `SharedPreferences`,
  `Hive.box`, `openDatabase`, `FlutterSecureStorage`. Note *what* is written
  where.
- **Dynamic:** exercise the app (login, save card/token), then dump the sandbox:
  ```sh
  adb shell run-as <pkg> ls -R /data/data/<pkg>        # Android (debuggable or root)
  # iOS: frida-ios-dump / ssh, inspect <app>/Documents, Library/Preferences
  ```
  Grep the pulled files for the known secret (token, PAN, password).
- MASTG: [MASTG-TEST-0207](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0207.md),
  [MASTG-TEST-0287](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0287.md) (SharedPreferences),
  [MASTG-TEST-0299](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0299.md)–[0302](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0302.md) (iOS private storage).

#### Positive evidence (secure)
Secret absent from `shared_prefs/*.xml`, Hive/DB files and plists; present only
in Keychain / Keystore-backed `flutter_secure_storage`. iOS files carry a Data
Protection class (`NSFileProtectionComplete`).

#### Negative evidence (insecure)
Token/PAN/password in cleartext in `*_preferences.xml`, a `.hive`/`.db` file, or
`NSUserDefaults` plist — e.g.:
```
$ adb shell run-as com.target cat shared_prefs/com.target_preferences.xml
<string name="auth_token">eyJhbGciOi...</string>
```

> iOS Keychain caveat: an item stored with `kSecAttrAccessibleAlways` (or
> `flutter_secure_storage` `IOSAccessibility.always`) persists in unencrypted
> backups — flag it. Prefer `first_unlock_this_device`.

## MASVS-STORAGE-2 — The app prevents leakage of sensitive data

#### Mechanism / sink (Flutter)
- **Logs:** `print()`/`debugPrint()`/`log()` and `dio`/`http` loggers
  (`LogInterceptor`, `PrettyDioLogger`) writing requests/tokens to logcat/
  syslog. These survive in release builds unless stripped.
- **External storage (Android):** `path_provider` `getExternalStorageDirectory`
  / media saves → world-readable pre-scoped-storage.
- **Backups:** Android `android:allowBackup="true"` (default) → `adb backup` /
  cloud backup includes the sandbox; iOS files not excluded from iCloud backup.
- **Keyboard cache / autocomplete:** `TextField` without
  `enableSuggestions:false`/`autocorrect:false` (and `obscureText` for secrets).

#### How to test
- `adb logcat | grep -iE "token|password|authorization|card"` while using the app.
- `adb backup -f out.ab <pkg>` then inspect (if `allowBackup`).
- Check `AndroidManifest.xml` for `allowBackup`/`fullBackupContent`; iOS check
  `isExcludedFromBackup` on written files.
- MASTG: [MASTG-TEST-0203](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0203.md)/[0231](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0231.md) (logging),
  [MASTG-TEST-0200](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0200.md) (external storage),
  [MASTG-TEST-0216](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0216.md)/[0262](../../upstream/MASTG/tests-beta/android/MASVS-STORAGE/MASTG-TEST-0262.md) (backup),
  [MASTG-TEST-0313](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0313.md)/[0314](../../upstream/MASTG/tests-beta/ios/MASVS-STORAGE/MASTG-TEST-0314.md) (keyboard cache).

#### Positive evidence (secure)
No secrets in logcat/syslog; `allowBackup="false"` or sensitive paths excluded;
secret fields use `obscureText:true` + suggestions disabled; nothing sensitive
on external/shared storage.

#### Negative evidence (insecure)
Auth header/token printed in logcat; `adb backup` yields the token DB; a saved
document/image with PII on shared storage; password field cached by the keyboard.

---
*Covers MASVS-STORAGE-1/-2. Encryption *quality* of secure stores → [CRYPTO](MASVS-CRYPTO.md).
Screenshot/clipboard UI leakage → [PLATFORM](MASVS-PLATFORM.md).*
