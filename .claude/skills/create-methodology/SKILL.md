---
name: create-methodology
description: >-
  Generate a framework-specific offensive-security testing methodology from the
  verification-standard bases in this repo — the ASVS 5.0 base
  (methodologies/_asvs-base/) for web apps / APIs / backends, the MASVS v2 base
  (methodologies/_masvs-base/) for mobile apps, and the cloud base
  (methodologies/_cloud-base/, MITRE ATT&CK Cloud + Prowler) for cloud
  environments. Use this WHENEVER the user asks to "create a <framework/
  platform> methodology", "build/add/generate a methodology" for a stack (Ruby
  on Rails, .NET / ASP.NET, Node.js / Express, Django, Spring Boot, Angular,
  React; mobile: Flutter, React Native, native Android/iOS; or cloud: AWS, GCP,
  Azure, Kubernetes, M365/Entra), to "map ASVS/MASVS/ATT&CK to <target>", or
  wants a per-chapter / per-category / per-tactic pentest methodology with test
  payloads and secure-vs-insecure evidence. It picks the right base, walks it in
  order, and projects each requirement/control/technique onto the target: the
  concrete mechanism/sink/service, how to test it, payload(s) or static+dynamic
  or enumerate+attempt steps, and positive (secure) vs negative (insecure/
  vulnerable) evidence. Always use this for methodology-authoring requests in
  this repo even if the user does not say "ASVS", "MASVS", or "ATT&CK".
---

# Create a framework methodology from an OWASP verification-standard base

This repo separates **what** must hold (a vendored OWASP verification standard)
from **how to test it on a given stack** (framework methodologies). Your job
when this skill triggers is to produce the second from the first, so coverage
is complete and consistent across every framework.

- **Style exemplars:** [`methodologies/springboot/README.md`](../../../methodologies/springboot/README.md) and [`methodologies/angular/README.md`](../../../methodologies/angular/README.md) show the house voice: concrete sinks, copy-paste payloads, terse "secure vs insecure" tells, links into `upstream/PayloadsAllTheThings`. (A Ruby on Rails methodology, if present, is the closest ASVS-aligned example.)

## Step 0 — Pick the base (web → ASVS, mobile → MASVS, cloud → ATT&CK/Prowler)

There are three bases. One skill, one projection contract; the base is what
varies. Choose by what the target *is*:

| Target | Base | Shape |
|---|---|---|
| Web app, HTTP API, backend framework (Rails, Django, Spring Boot, Express, ASP.NET, …) | [`methodologies/_asvs-base/`](../../../methodologies/_asvs-base/) | 17 chapters (V1–V17), 345 requirements, IDs/levels/text verbatim from `upstream/ASVS` |
| Mobile app (Flutter, React Native, native Android/iOS) | [`methodologies/_masvs-base/`](../../../methodologies/_masvs-base/) | 8 categories, 24 controls verbatim from `upstream/MASVS`, each linked to MASTG v2 test procedures in `upstream/MASTG` |
| Cloud environment / control plane (AWS, GCP, Azure, K8s, M365/Entra) | [`methodologies/_cloud-base/`](../../../methodologies/_cloud-base/) | 12 ATT&CK cloud tactics, 188 techniques verbatim from MITRE ATT&CK, cross-referenced to Prowler config checks in `upstream/prowler` |

**Some targets need more than one base.** A **mobile app**: client = MASVS, its
backend = ASVS — generate MASVS and, unless scoped out, cover the backend
against ASVS. A **cloud engagement**: control plane = this cloud base, the apps
running on it = ASVS, any mobile client = MASVS. If it is genuinely unclear
which surface the user wants, ask — otherwise default to the primary target's
base, name the others as adjacent scope, and state it.

**Never invent requirements/controls/techniques; read them from the chosen
base.** The rest of this skill is written in ASVS ("chapter/requirement") terms;
for a mobile target read **category**/**control**, for a cloud target read
**tactic**/**technique**. See **Mobile specifics** and **Cloud specifics** below
for where the flow differs (output structure and the evidence axes).

- **Output:** `methodologies/<framework>/` — one page per base chapter/category, mirroring the base 1:1, plus a `README.md` index.

## Step 1 — Scope

Settle these before writing. Ask the user only if a choice is genuinely
unclear from the request; otherwise pick the sensible default and state it.

- **Framework / stack** (required) — e.g. "Ruby on Rails", "ASP.NET Core", "Express + Prisma", "Flutter", "React Native". Pin the dominant libraries for each concern because the projection is library-specific (web: Rails→Devise/ActiveRecord; Django→`django.contrib.auth`/ORM; Express→Passport/Sequelize. mobile: Flutter→`flutter_secure_storage`/Dio/`pointycastle`; RN→AsyncStorage/Keychain bridges; native→Keystore/Keychain).
- **Level / profile** (default **L2**) — ASVS: L1 baseline, L2 standard, L3 high-assurance. MASVS: `L1` baseline, `L2` defense-in-depth, and `R` resilience (anti-reversing/tampering — the MASVS-RESILIENCE category; include it only when the app has a meaningful threat model for it, e.g. DRM, anti-fraud, payments). Cover every item at or below the target; mention higher ones only where cheap.
- **Test posture** (default **black/grey-box**, offensive tester) — governs what is directly testable vs. only verifiable with source. For mobile, also note **artifact access**: do you have the APK/IPA, and is it a debug or release build? (Decompilation and instrumentation depth depend on it.)
- **Platform** (mobile only, default **both**) — Android, iOS, or both. The MASTG test rows in the base are platform-tagged; projecting onto Flutter means covering both unless scoped to one.

## Step 2 — Read the base, chapter by chapter

Process the base pages **in order** — ASVS chapters V1→V17, or MASVS categories
STORAGE→CRYPTO→AUTH→NETWORK→PLATFORM→CODE→RESILIENCE→PRIVACY. For each, read its
base page (e.g. `methodologies/_asvs-base/V06-Authentication.md`, or
`methodologies/_masvs-base/MASVS-STORAGE.md`) and work through every
requirement/control row. For MASVS, also open the linked **MASTG test**
procedures for that category — they carry the concrete static/dynamic steps,
commands, and tooling you project onto the stack. Do not batch from memory —
the requirement/control text is the contract.

## Step 3 — Output structure

Create `methodologies/<framework>/` with:

- `README.md` — index: a one-paragraph framing, a **fingerprinting** quick ref for the stack, and an **ASVS chapter → page** table. Follow the layout of `methodologies/_asvs-base/README.md` and the existing `ruby/README.md`.
- One page per chapter, named to mirror the base: `V01-encoding-and-sanitization.md`, … `V17-webrtc.md`. (A stack with no WebRTC still gets a short V17 page stating it's out of scope and why — completeness is the point of an ASVS-driven methodology.)

Each chapter page is organized **by ASVS section** (`## V6.2 Password Security`),
and within a section, **by requirement**. Keep the requirement ID and level
visible so the page maps back to the base and to a report.

## Step 4 — Project each requirement (the core)

For every requirement, decide its nature and render accordingly:

**(a) Directly testable** (input sent, config observable, behaviour probeable) —
render the full block:

```markdown
#### 6.2.2 — Breached-password check · L2
> Verify that passwords are checked against a set of breached passwords.

- **Mechanism (Rails):** `Devise` + the `devise-pwned_password` gem, or a custom
  validator hitting HaveIBeenPwned's range API. Absent gem/validator = not done.
- **How to test:** register / change password to a known-breached value
  (`Password1!`, `123456`).
- **Payload:** `user[password]=Password1!`
- **Positive (secure):** `422 Unprocessable Entity`, form error "this password
  has previously appeared in a data breach"; account not created.
- **Negative (insecure):** `302` to the signed-in dashboard; a breached password
  is accepted — finding.
```

**(b) Config / header / transport** — give the exact setting that satisfies it
and a wire-level check (`curl -sD- ... | grep -i <header>`), then the
secure vs insecure response.

**(c) Governance / documentation-only** (many `V*.1 Documentation` and L3
"document the rules" requirements) — don't fabricate a payload. State in one
line that it's a design/documentation control, what artifact or interview
evidences it, and the black-box signal if its *absence* is observable
(e.g. inconsistent enforcement). Keep these short so they don't drown the
testable content.

**(d) Not applicable to this stack** — list the ID and one line why
(e.g. "9.x self-contained tokens — N/A, app uses opaque server-side sessions").
Never silently drop a requirement; a reader must be able to see every ID
accounted for.

### Positive / negative response discipline

The whole value of these pages is the **confirmation signal**: what the tester
actually sees. Make positive (secure) and negative (insecure) outcomes
concrete — status code, decisive header, body text, redirect, timing, or
persisted-state change — not "it works" / "it's vulnerable". Prefer a real
`HTTP` request/response sketch or a `curl` one-liner when an input is sent.

## Mobile specifics (MASVS targets only)

Two places the flow differs from the web/ASVS case:

**Output structure.** One page per **MASVS category**, named to mirror the base:
`MASVS-STORAGE.md`, `MASVS-CRYPTO.md`, `MASVS-AUTH.md`, `MASVS-NETWORK.md`,
`MASVS-PLATFORM.md`, `MASVS-CODE.md`, `MASVS-RESILIENCE.md`, `MASVS-PRIVACY.md`,
plus `README.md`. Organize each page **by control** (`## MASVS-STORAGE-1`), and
under it group the relevant **MASTG tests** you projected. The `README.md`
fingerprinting quick-ref is mobile-flavoured: how to confirm the framework
(e.g. Flutter → `libapp.so` + `libflutter.so`, `flutter_assets/` in the APK;
RN → `index.android.bundle`), how to get the artifact, and the tooling baseline.

**Evidence axes.** Mobile findings are **static + dynamic**, not request/
response. For each control render, where applicable:

- **Mechanism / sink** — the platform/framework API, storage location, manifest/
  plist entry, or code pattern (e.g. Flutter `shared_preferences` → plaintext
  XML/plist; `flutter_secure_storage` → Keystore/Keychain).
- **Static** — decompile/inspect: `apktool`, `jadx`, Blutter/reFlutter for the
  Dart snapshot, `strings` on `libapp.so`, manifest/`Info.plist`,
  `codesign`/`otool`/`class-dump`.
- **Dynamic** — runtime: Frida/Objection hooks, filesystem dump after use,
  proxy traffic (mitmproxy/Burp) — noting Flutter ignores the system proxy and
  pins at the BoringSSL layer, so interception needs reFlutter / a Frida
  `ssl_verify` bypass / `proxydroid`, not just a trusted CA.
- **Positive (secure) / Negative (insecure) evidence** — the concrete on-device
  artifact: "secret absent from `shared_prefs/*.xml`, present only in Keystore"
  vs "API key in cleartext in `strings libapp.so`".

The MASVS-RESILIENCE category (root/jailbreak detection, anti-hooking, anti-
tampering, obfuscation) is the `R` profile — test it as *controls to defeat*
(does a Frida attach / rooted device / repackaged APK get detected and the app
refuse to run?), and treat its absence as a resilience gap, not a vuln per se.

## Cloud specifics (ATT&CK/Prowler targets only)

Two places the flow differs from the web/ASVS case:

**Output structure.** Cloud methodologies are organized by **kill-chain phase**,
not one page per tactic — an engagement runs as a chain. Create `methodologies/
<provider>/` (e.g. `aws/`, `gcp/`, `azure/`) with a `README.md` (the provider's
auth/identity model, recon + enumeration, Prowler/ScoutSuite/Pacu tooling,
assumed-breach vs black-box starting point) plus phase pages:
`01-recon-and-enumeration.md`, `02-access-and-credentials.md`,
`03-privilege-escalation.md`, `04-lateral-movement-and-persistence.md`,
`05-evasion.md`, `06-collection-exfil-impact.md`. Each phase page covers the
ATT&CK tactic(s) the base maps to that phase (see
[`_cloud-base/README.md`](../../../methodologies/_cloud-base/README.md)), and
organizes by **technique ID**, cross-linking the base tactic page.

**Evidence axes.** Cloud findings are **enumerate → attempt**, against a
provider API — not request/response on a URL. For each technique render, where
applicable:

- **Service / sink** — the concrete service/API/resource (IAM, STS, S3,
  Metadata/IMDS, KMS, Lambda, Entra ID, GCS, IAM bindings, service accounts).
- **How to test** — the enumeration step then the attempt: the CLI/API call
  (`aws`, `gcloud`, `az`, `kubectl`) or tool (Pacu, ScoutSuite, enumerate-iam,
  ROADtools, GCPBucketBrute). Give the actual command.
- **Positive evidence (secure)** — `AccessDenied` / `403` / SCP or guardrail
  blocks it / MFA challenge.
- **Negative evidence (vulnerable)** — the call succeeds, creds/data returned,
  the role is assumable — the confirmation signal. **Name the Prowler check ID**
  that detects the underlying misconfiguration (e.g. `ec2_imdsv2_enabled`,
  `iam_policy_no_administrative_privileges`) so the offensive finding ties to the
  detective control. Prowler check IDs live under
  `upstream/prowler/prowler/providers/<provider>/services/.../<check>.metadata.json`
  (only AWS checks carry `TTPs/<tactic>` tags; for Azure/GCP find checks by
  service/category).

Authorization note: real cloud testing needs explicit provider authorization
(AWS/Azure/GCP each have pentest rules); assume an **authorized** engagement and
say so. Prefer non-destructive confirmation (read/enumerate, dry-run) over
anything that modifies or impacts resources.

## Step 5 — Wire it up

- Add a pointer to the repo root `README.md` methodologies list (match the
  existing Angular/Spring Boot entries). For a mobile methodology note the base
  it was generated from (MASVS v2) and, if a companion backend methodology was
  produced, cross-link the two.
- If the user asked to commit/push, branch (`<framework>-methodology`), commit
  with the repo's attribution convention, and follow the push flow already
  established. Don't commit the `upstream/` submodules or unrelated working-tree
  changes.

## House rules

- **Grounded, not invented.** Requirements come from the base; CVEs, gem/
  package names, and version-gated behaviour must be real — verify before
  asserting, and say when something is version-dependent. A wrong CVE or a
  hallucinated "secure default" makes the page worse than nothing.
- **Framework-specific over generic.** Anyone can say "test for XSS". The value
  is "`<%= raw user.bio %>` / `html_safe` is the Rails opt-out; default `<%= %>`
  escapes." Name the sink, the default, and the override that breaks it.
- **Link, don't duplicate.** For generic payload lists, link the matching
  `upstream/PayloadsAllTheThings/<Category>/README.md` page (relative path from
  `methodologies/<framework>/`, URL-encoding spaces as `%20`) rather than
  re-deriving them. Keep this page about what's *specific to the stack*.
- **Lean.** One tight block per requirement beats three paragraphs. A tester
  scans these mid-engagement.

## Worked example — IDOR/BOLA (ASVS 8.2.2 → Rails)

```markdown
#### 8.2.2 — Data-specific access control (IDOR / BOLA) · L1
> Verify that data-specific access is restricted to consumers with explicit
> permissions ... to mitigate IDOR and BOLA.

- **Mechanism (Rails):** lookups must be scoped to the subject —
  `current_user.invoices.find(params[:id])`, not `Invoice.find(params[:id])`.
  A Pundit/CanCanCan `authorize` call is the alternative enforcement point.
- **How to test:** as user B, request an object id owned by user A.
- **Payload:** `GET /invoices/1041` with user B's session cookie.
- **Positive (secure):** `404 Not Found` (scoped query misses) or `403`.
- **Negative (insecure):** `200 OK` returning user A's invoice — finding.
  Sequential ids (`/invoices/1042`, `1043`, …) then enable enumeration.
```

When you finish, tell the user which chapters produced testable pages vs.
mostly-governance pages, and anything you scoped out (and why).
