# V16 – Security Logging and Error Handling (Rails)

> **ASVS 5.0 · Chapter V16** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V16-Security-Logging-and-Error-Handling.md`](../_asvs-base/V16-Security-Logging-and-Error-Handling.md).
> The marquee finding here is a **development error console reachable in
> production** (`web-console` / `better_errors`) — unauthenticated RCE.

## V16.5 Error handling

#### 16.5.1 — Generic error message (no internals) · L2
- **Mechanism (Rails):** production must use static error pages
  (`config.consider_all_requests_local = false`) and **must not** ship
  `web-console`/`better_errors`+`binding_of_caller` outside the `:development`
  group. Those gems turn any exception page into an interactive Ruby REPL.
- **How to test:** trigger an unhandled exception (bad type in a path,
  malformed JSON body, `?q[]=` type confusion) and inspect the error page.
- **Payload:** `GET /users/abc` (type-mismatched id) ; `-d '{bad'` with
  `Content-Type: application/json`.
- **Positive (secure):** generic static 500 (`public/500.html`), no stack trace.
- **Negative (insecure):**
  - full Rails exception page → stack trace, source excerpt, params, session,
    gem versions (info leak); **or**
  - an **interactive console / REPL** on the error page or at `/__better_errors`
    → evaluate `` `id` `` → **RCE** (confirm non-destructively with `1+1`).
  - (`CVE-2015-3224`: web-console IP-allowlist bypass behind a proxy.)

#### 16.5.3 / 16.5.4 — Fail securely / last-resort handler · L2/L3
- **Mechanism (Rails):** a `rescue_from` catch-all that returns generic errors
  and **fails closed** (no transaction completing despite an error). Finding: a
  `rescue` that swallows an authorization/validation error and proceeds
  (fail-open).
- **How to test:** induce errors mid-operation; check nothing privileged
  proceeds and no internals leak.

**16.5.2 (L2):** graceful degradation when an external resource fails (circuit
breaker), not an error that exposes internals.

## V16.2 / V16.4 Logging hygiene

#### 16.2.5 — Don't log sensitive data · L2
- **Mechanism (Rails):** `config.filter_parameters` must cover every secret
  param — `:password`, `:password_confirmation`, `:token`, `:secret`, `:ssn`,
  `:card`, `:cvv`, `:otp`, `:api_key`, `Authorization`. Missing filters →
  plaintext secrets in `production.log`.
- **How to test (grey/white-box):** review `config/initializers/filter_parameter_logging.rb`;
  if logs are reachable (LFI, exposed log viewer, mounted engine), grep them.
- **Positive (secure):** sensitive params shown as `[FILTERED]` in logs.
- **Negative (insecure):** passwords/tokens in cleartext in logs.

#### 16.4.1 — Log injection encoding (CRLF) · L2
- **Mechanism (Rails):** user input with `\r`/`\n` written to logs unescaped →
  forged log lines / XSS into a log-viewer UI.
- **Payload:** a username/field containing `\n[INFO] fake log entry`.
- **Positive (secure):** newlines encoded/stripped in log output.
- **Negative (insecure):** injected line appears as a separate log entry.
  Upstream [CRLF Injection](../../upstream/PayloadsAllTheThings/CRLF%20Injection/README.md).

## V16.3 Security events (logging coverage)

**16.3.1–16.3.4 (L2):** log authentication (success/failure), failed
authorization, security-control-bypass attempts, and unexpected errors with
sufficient metadata (**16.2.1** when/where/who/what; **16.2.2** synchronized UTC
timestamps). Mostly verifiable grey/white-box or via the logging inventory
(**16.1.1**). **16.4.2/16.4.3 (L2):** logs protected from modification and
shipped to a separate system.

---
*Covers ASVS V16.1–V16.5. Verbose-error/debug config also at
[V13.4.2](V13-configuration.md).*
