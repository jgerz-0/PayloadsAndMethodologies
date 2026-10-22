# V8 – Authorization (Rails)

> **ASVS 5.0 · Chapter V8** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V08-Authorization.md`](../_asvs-base/V08-Authorization.md).
> The dominant Rails bug is the **unscoped lookup**
> (`Model.find(params[:id])`), i.e. IDOR/BOLA. Enforcement is Pundit/CanCanCan
> or hand-rolled `before_action`.

## V8.2 General authorization design

#### 8.2.2 — Data-specific access (IDOR / BOLA) · L1
> Restrict data access to consumers with explicit permission (mitigate IDOR/BOLA).

- **Mechanism (Rails):** scope every lookup to the subject —
  `current_user.invoices.find(params[:id])`, not `Invoice.find(params[:id])`;
  or a Pundit `authorize @invoice`. Applies to `show`/`update`/`destroy`,
  nested resources, JSON/API, and GraphQL `node(id:)`.
- **How to test:** as user B, request an object id owned by user A.
- **Payload:** `GET /invoices/1041` with user B's session cookie.
- **Positive (secure):** `404` (scoped query misses) or `403`.
- **Negative (insecure):** `200` returning A's invoice → IDOR; sequential ids
  (`1042`, `1043`, …) enable enumeration. UUIDs raise the bar but a leaked/
  guessed id still works. Upstream
  [IDOR](../../upstream/PayloadsAllTheThings/Insecure%20Direct%20Object%20References/README.md).

#### 8.2.1 — Function-level access · L1
> Restrict function-level access to consumers with explicit permission.

- **Mechanism (Rails):** Pundit `authorize` + `after_action :verify_authorized`;
  CanCanCan `load_and_authorize_resource` + `check_authorization`;
  or `before_action :require_admin`. Common gap: `before_action :require_admin,
  only: [:destroy]` leaves `update`/`create` open; a controller action that
  simply forgets `authorize`.
- **How to test:** as a low-priv user, invoke admin/privileged actions and each
  verb directly.
- **Positive (secure):** `403`/redirect for every privileged action and verb.
- **Negative (insecure):** action executes for an unauthorized role / verb.

#### 8.2.3 — Field-level access (BOPLA) · L2
> Restrict field-level read/write to consumers with explicit permission.

- **Mechanism (Rails):** write side = strong-parameters per role (don't permit
  `role`/`approved` for self-service — [V15.3.3](V15-secure-coding-and-architecture.md));
  read side = serializers that omit fields the user may not see.
- **How to test:** send a privileged field in an update; inspect JSON for fields
  outside your entitlement.
- **Positive (secure):** extra field ignored; response omits unauthorized fields.
- **Negative (insecure):** privileged field persists, or sensitive field
  returned (e.g. another user's email/`password_digest`). Cf.
  [ORM Leak](../../upstream/PayloadsAllTheThings/ORM%20Leak/README.md).

## V8.3 Operation-level authorization

#### 8.3.1 — Enforced at a trusted service layer · L1
- **Mechanism (Rails):** authorization decisions made server-side, not via
  hidden form fields / client flags the user can flip.
- **How to test:** tamper client-side role/price/flag fields and resubmit.
- **Positive (secure):** server re-derives authorization from `current_user`.
- **Negative (insecure):** client-supplied value drives the decision.

**8.3.2 / 8.3.3 (L3):** authorization changes apply immediately (watch for
stale self-contained tokens — [V9](V09-self-contained-tokens.md)); object
access uses the originating subject's permissions, not an intermediary's.

## V8.4 Other considerations

#### 8.4.1 — Multi-tenant cross-tenant controls · L2
- **Mechanism (Rails):** every query scoped by tenant (`acts_as_tenant`,
  default scopes, or explicit `current_tenant` scoping). Finding: a
  mass-assignable `account_id`/`organization_id`, or an unscoped lookup, lets a
  user reach another tenant's data.
- **Payload:** set `account_id=<other tenant>` in a create/update, or request a
  resource id belonging to another tenant.
- **Positive (secure):** tenant mismatch → `404`/`403`; foreign-key fields not
  mass-assignable.
- **Negative (insecure):** cross-tenant read/write succeeds.

**8.4.2 (L3):** admin interfaces use layered controls (continuous identity,
device posture, context) — network location alone must not authorize.
Also check **mounted engines** (`/sidekiq`, `/blazer`, `/flipper`) sit behind
an `authenticate`/`constraints` block, not merely unlinked
([V13](V13-configuration.md)).

> **Tooling:** Burp **Autorize**/AuthMatrix for A-vs-B replay; `brakeman` flags
> some unscoped finds and missing filters, but IDOR is primarily manual.

---
*Covers ASVS V8.1–V8.4. V8.1.x is documentation of the authorization model.*
