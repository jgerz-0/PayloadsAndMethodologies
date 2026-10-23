# MASVS-PRIVACY – Privacy (Flutter)

> **MASVS v2 · Privacy** — projected onto Flutter (Android + iOS).
> Base: [`_masvs-base/MASVS-PRIVACY.md`](../_masvs-base/MASVS-PRIVACY.md).
> Mostly **design/transparency** controls, verified by inspecting declared
> permissions, bundled tracker SDKs, identifiers sent on the wire, and
> data-control features — plus the store privacy declarations. Few are a binary
> "exploit"; report as privacy findings.

## MASVS-PRIVACY-1 — Minimize access to sensitive data & resources

#### Mechanism / sink (Flutter)
- **Permissions:** Android `AndroidManifest.xml` `uses-permission` + iOS
  `Info.plist` `NS*UsageDescription`, typically pulled in by plugins
  (`geolocator`, `camera`, `contacts_service`, `permission_handler`). Plugins
  often over-declare.
- **Third-party / tracker SDKs** collecting data (analytics, ads, crash) —
  Firebase, Facebook SDK, AppsFlyer, Adjust — and whether they fire **before**
  consent.

#### How to test
- Enumerate permissions (manifest/plist) vs actual features; flag unused
  sensitive ones.
- Identify SDKs (plugin classes, `pubspec.lock`, domains in traffic); intercept
  on first launch **before** accepting consent and see what's already sent.
- MASTG / MASWE privacy tests
  ([`_masvs-base/MASVS-PRIVACY.md`](../_masvs-base/MASVS-PRIVACY.md)).

#### Positive / negative evidence
**Secure:** permissions match features; trackers fire only after consent.
**Insecure:** `ACCESS_FINE_LOCATION` with no location feature; analytics/ad
beacon with device IDs sent on first launch pre-consent.

## MASVS-PRIVACY-2 — Prevent identification of the user

#### Mechanism / sink (Flutter)
Stable device/user identifiers used for tracking or sent to third parties:
`device_info_plus` (Android ID, `identifierForVendor`), advertising ID,
`androidId`, IMEI (legacy), or a home-grown fingerprint reused across purposes.

#### How to test
Intercept outbound analytics/ad traffic; look for persistent identifiers and
whether one signal (e.g. a fraud fingerprint) is reused for analytics.

#### Positive / negative evidence
**Secure:** resettable/abstracted IDs, purpose-isolated. **Insecure:** hardware
IDs or a cross-purpose fingerprint shipped to trackers enabling linkage.

## MASVS-PRIVACY-3 — Transparency about data collection

#### Mechanism / sink (Flutter)
Consistency between what the app **does** (observed collection) and what it
**declares** — in-app privacy notice, Play Data Safety / Apple Privacy Nutrition
labels, consent prompts (ATT on iOS via `app_tracking_transparency`).

#### How to test
Compare observed data flows (from PRIVACY-1/-2 interception) against the stated
privacy disclosures and store labels; check iOS ATT prompt precedes tracking.

#### Positive / negative evidence
**Secure:** declared collection matches observed; ATT honored. **Insecure:**
undisclosed background collection; tracking before/without the ATT prompt.

## MASVS-PRIVACY-4 — User control over their data

#### Mechanism / sink (Flutter)
In-app mechanisms to view/export/delete data, revoke consent, and change privacy
settings; re-prompt/refresh disclosures when scope expands.

#### How to test
Exercise account deletion / consent revocation; confirm it propagates to the
**backend** (data actually deleted/stops flowing), not just a local toggle.

#### Positive / negative evidence
**Secure:** deletion/revocation reaches the server and halts collection.
**Insecure:** "delete my data" only clears local state while the backend retains
it and trackers keep firing.

---
*Covers MASVS-PRIVACY-1/-4. Server-side retention/deletion and PII handling are
[ASVS V14](../_asvs-base/V14-Data-Protection.md).*
