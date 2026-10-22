---
name: create-methodology
description: >-
  Generate a framework-specific offensive-security testing methodology from the
  OWASP ASVS 5.0 base in this repo (methodologies/_asvs-base/). Use this
  WHENEVER the user asks to "create a <framework> methodology", "build/add/
  generate an ASVS methodology" for a stack (Ruby on Rails, .NET / ASP.NET,
  Node.js / Express, Django, Flask, Laravel, Spring Boot, Go, Angular, React,
  etc.), to "map ASVS to <framework>", or wants a per-ASVS-chapter pentest
  methodology with test payloads and secure-vs-insecure response examples.
  It walks the ASVS base chapter by chapter and projects each requirement onto
  the target stack: the concrete mechanism/sink, how to test it, payload(s),
  and positive (secure) vs negative (insecure) response examples. Always use
  this for methodology-authoring requests in this repo even if the user does
  not say the word "ASVS".
---

# Create a framework methodology from the ASVS base

This repo separates **what** must hold (the vendored OWASP ASVS 5.0 standard)
from **how to test it on a given stack** (framework methodologies). Your job
when this skill triggers is to produce the second from the first, so coverage
is complete and consistent across every framework.

- **Base (source of truth):** [`methodologies/_asvs-base/`](../../../methodologies/_asvs-base/) — one page per ASVS chapter V1–V17, 345 requirements, IDs/levels/text verbatim from `upstream/ASVS`. **Never invent requirements; read them from here.**
- **Output:** `methodologies/<framework>/` — one page per ASVS chapter, mirroring the base 1:1, plus a `README.md` index.
- **Style exemplars:** [`methodologies/springboot/README.md`](../../../methodologies/springboot/README.md) and [`methodologies/angular/README.md`](../../../methodologies/angular/README.md) show the house voice: concrete sinks, copy-paste payloads, terse "secure vs insecure" tells, links into `upstream/PayloadsAllTheThings`. (A Ruby on Rails methodology, if present, is the closest ASVS-aligned example.)

## Step 1 — Scope

Settle these before writing. Ask the user only if a choice is genuinely
unclear from the request; otherwise pick the sensible default and state it.

- **Framework / stack** (required) — e.g. "Ruby on Rails", "ASP.NET Core", "Express + Prisma". Pin the dominant libraries for each concern (auth, ORM, templating, session) because the projection is library-specific (Rails→Devise/ActiveRecord; Django→`django.contrib.auth`/ORM; Express→Passport/Sequelize, etc.).
- **ASVS level** (default **L2**) — L1 baseline, L2 standard (most apps), L3 high-assurance. Cover every requirement at or below the target level; mention higher-level ones only where cheap.
- **Test posture** (default **black/grey-box**, offensive tester) — this governs which requirements are directly testable vs. only verifiable with source.

## Step 2 — Read the base, chapter by chapter

Process ASVS chapters **in order V1→V17**. For each chapter, read its base
page (e.g. `methodologies/_asvs-base/V06-Authentication.md`) and work through
every requirement row. Do not batch from memory — the requirement text is the
contract.

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

## Step 5 — Wire it up

- Add a pointer to the repo root `README.md` methodologies list (match the
  existing Angular/Spring Boot entries).
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
