# V2 – Validation and Business Logic (Rails)

> **ASVS 5.0 · Chapter V2** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V02-Validation-and-Business-Logic.md`](../_asvs-base/V02-Validation-and-Business-Logic.md).
> Input validation as defence-in-depth, plus business-logic integrity:
> sequencing, limits, transactions, concurrency locks, anti-automation.

## V2.1 Documentation (design)

**2.1.1 (L1) / 2.1.2 / 2.1.3 (L2):** documentation of input-validation rules,
cross-field consistency, and per-user/global business limits. Design controls —
evidence is the spec plus consistent enforcement observed in testing. No payload;
their *absence* shows up as the inconsistent-enforcement findings below.

## V2.2 Input validation

#### 2.2.1 — Allowlist input validation · L1
> Validate input against business/functional expectations (positive allowlist).

- **Mechanism (Rails):** model validations (`validates :role, inclusion: {in: %w[...]}`,
  `numericality`, `format`) and strong-parameters shape. Rails merges query,
  form, and JSON params, so a param expected as a String may arrive as an Array
  or Hash (`?x[]=`), bypassing checks that assume a type.
- **Payload:** `?user[]=a&user[]=b` / `q[$ne]=` style type confusion where a
  scalar is expected.
- **Positive (secure):** type/shape validated; unexpected structure → `400`/
  validation error.
- **Negative (insecure):** `TypeError`/500, or the array/hash reaching a sink
  (e.g. `where(params[:q])`) — see [V1 SQLi](V01-encoding-and-sanitization.md).

#### 2.2.2 — Validation at a trusted service layer · L1
- **Mechanism (Rails):** server-side model/controller validation, not just JS.
- **How to test:** submit values the UI forbids directly to the endpoint
  (bypassing client JS).
- **Positive (secure):** server rejects (`422` + validation errors).
- **Negative (insecure):** server persists the UI-forbidden value.

**2.2.3 (L2):** combined-data reasonableness (e.g. ZIP matches state) — test
mismatched but individually-valid combinations.

## V2.3 Business logic security

#### 2.3.1 — Sequential step order · L1
> Process flows only in the expected step order, without skipping.

- **Mechanism (Rails):** multi-step wizards / `aasm`/`state_machines`. Finding:
  POSTing directly to a later step's action skips earlier gates.
- **Payload:** `POST /checkout/confirm` (or set order `state=shipped`) without
  completing payment.
- **Positive (secure):** server enforces the state machine; out-of-order
  transition rejected.
- **Negative (insecure):** later step executes (order ships unpaid).

#### 2.3.3 — Transactional integrity · L2
- **Mechanism (Rails):** multi-write operations wrapped in
  `ActiveRecord::Base.transaction` so a mid-operation failure rolls back.
- **How to test:** force a failure partway (invalid second item, forced
  constraint violation) and check for a half-applied state (charged but no
  order).

#### 2.3.4 — Limited-resource locking (race conditions) · L2
> Locking so limited-quantity resources can't be double-booked via parallel requests.

- **Mechanism (Rails):** `with_lock`/`lock!` (pessimistic), optimistic
  `lock_version`, DB unique indexes, atomic `UPDATE ... SET x = x - ?`. The
  footgun: `find_or_create_by` and `validates uniqueness:` are **check-then-act**
  and race without a DB unique index.
- **How to test:** fire N identical requests in parallel (Burp "send group in
  parallel" / Turbo Intruder) at coupon redemption, balance withdrawal,
  seat/slot booking.
- **Payload:** 20× parallel `POST /coupons/redeem {code: SINGLEUSE}`.
- **Positive (secure):** exactly one success; others `409`/validation error;
  balance decremented once.
- **Negative (insecure):** multiple successes / balance over-credited —
  TOCTOU. Upstream [Race Condition](../../upstream/PayloadsAllTheThings/Race%20Condition/README.md).

**2.3.2 (L2)** business-logic limits (negative/overflow quantities,
`quantity=-1` for a credit) — test bounds; see
[Business Logic Errors](../../upstream/PayloadsAllTheThings/Business%20Logic%20Errors/README.md).
**2.3.5 (L3)** high-value flows need multi-user approval — design/logic check.

## V2.4 Anti-automation

#### 2.4.1 — Anti-automation controls · L2
> Protect against excessive calls (exfiltration, quota exhaustion, brute force).

- **Mechanism (Rails):** Rails has no built-in throttling before 7.2; look for
  `rack-attack` (`config/initializers/rack_attack.rb`) or 7.2+ controller
  `rate_limit`. Absence = unlimited automation on login, reset, OTP, search,
  enumeration endpoints.
- **How to test:** burst 50–100 requests at a sensitive endpoint.
- **Payload:** `for i in $(seq 1 100); do curl -s -o /dev/null -w "%{http_code} " ...; done`
- **Positive (secure):** `429 Too Many Requests` / throttling kicks in.
- **Negative (insecure):** all `200`/`422`, no throttle. Upstream
  [Brute Force Rate Limit](../../upstream/PayloadsAllTheThings/Brute%20Force%20Rate%20Limit/README.md).

**2.4.2 (L3):** flows require realistic human timing — test ultra-fast scripted
submission.

---
*Covers ASVS V2.1–V2.4. Mass assignment is V15.3.3
([V15](V15-secure-coding-and-architecture.md)); input→injection sinks are
[V1](V01-encoding-and-sanitization.md).*
