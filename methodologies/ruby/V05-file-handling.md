# V5 – File Handling (Rails)

> **ASVS 5.0 · Chapter V5** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V05-File-Handling.md`](../_asvs-base/V05-File-Handling.md).
> Uploads (ActiveStorage, CarrierWave, Shrine, Paperclip), file serving
> (`send_file`, `render file:`), path traversal, zip slip.

## V5.2 File upload & content

#### 5.2.2 — Extension + content validation · L1
- **Mechanism (Rails):** CarrierWave `extension_allowlist`/`content_type_allowlist`,
  ActiveStorage content-type validation, or Shrine `validate_mime_type`. Weak
  form: checking only the client-supplied extension or `Content-Type`.
- **How to test:** upload disallowed content with a bypass (double extension
  `x.php.png`, spoofed `Content-Type`, magic-byte mismatch).
- **Payload:** `shell.php.png`; SVG/HTML with script; `Content-Type: image/png`
  on a non-image.
- **Positive (secure):** server validates real content and rejects; stores
  under an internally generated name.
- **Negative (insecure):** disallowed file accepted. Impact depends on serving
  (see 5.3.1). Upstream [Upload Insecure Files](../../upstream/PayloadsAllTheThings/Upload%20Insecure%20Files/README.md).

#### 5.2.1 — Upload size limits · L1 · 5.2.3 compression bombs · 5.2.6 pixel flood
- **Mechanism (Rails):** size caps (validation + proxy `client_max_body_size`);
  for archives (`rubyzip`) check uncompressed size and entry count; for images
  (MiniMagick) cap pixel dimensions.
- **Payload:** oversized file; zip bomb (small→huge); pixel-flood image.
- **Positive:** rejected before processing (`413`/validation error).
- **Negative:** server processes it → CPU/memory/disk DoS.

## V5.3 File storage

#### 5.3.1 — Uploaded files not executed server-side · L1
- **Mechanism (Rails):** uploads must be served from a location that doesn't
  execute code and ideally a separate cookieless domain, with
  `Content-Disposition: attachment`. Risk rises when a reverse proxy serves the
  upload dir or `public/`.
- **Payload:** upload `<svg onload=alert(document.domain)>` / an `.html`; fetch
  the stored blob URL.
- **Positive (secure):** served `Content-Disposition: attachment` +
  `X-Content-Type-Options: nosniff`, non-executing origin; file downloads inert.
- **Negative (insecure):** served inline `text/html` on the app origin →
  stored XSS (or code execution if the dir is interpreted).

#### 5.3.2 — Internally generated file paths · L1 (path traversal)
> Use internally generated/trusted data for file paths, or strictly validate user filenames.

- **Mechanism (Rails):** storing/serving by a user-controlled filename/path.
  `send_file params[:path]`, `File.read(params[:path])`, upload paths built from
  a user filename.
- **Payload:** `../../../../etc/passwd` · `..%2f..%2fconfig/master.key` ·
  `....//....//config/database.yml`
- **Positive (secure):** path built from a DB id / `File.expand_path` confined
  under an allowed root; traversal → `404`.
- **Negative (insecure):** arbitrary file contents returned (high-value Rails
  targets: `config/master.key`, `config/credentials.yml.enc`, `.env`,
  `config/database.yml` — see [V11](V11-cryptography.md)). Upstream
  [Directory Traversal](../../upstream/PayloadsAllTheThings/Directory%20Traversal/README.md).

#### 5.3.3 — Zip slip · L3
- **Mechanism (Rails):** archive extraction (`rubyzip`) that trusts entry names
  containing `../` writes outside the target dir.
- **Payload (entry name in the archive):** `../../config/initializers/evil.rb`
- **Positive (secure):** each entry path validated to stay under the extraction
  root.
- **Negative (insecure):** file written outside root → overwrite config/code →
  RCE. Upstream [Zip Slip](../../upstream/PayloadsAllTheThings/Zip%20Slip/README.md).

> **`render file:` Accept-header traversal (CVE-2019-5418):** an action doing
> `render file:` on affected Rails allows unauth arbitrary file read via a
> crafted `Accept: ../../../../etc/passwd{{` header. Version-gated — see
> [V15 CVEs](V15-secure-coding-and-architecture.md).

## V5.4 File download

#### 5.4.1 / 5.4.2 — Download filename validation & encoding · L2
- **Mechanism (Rails):** `send_file`/`send_data` set
  `Content-Disposition`; a user-controlled filename reflected there unescaped
  allows header injection / misleading names (RFC 6266).
- **Payload:** filename `"report\r\nSet-Cookie: x=1.pdf"` / `../../etc/passwd`.
- **Positive (secure):** filename sanitized/encoded; `Content-Disposition`
  intact.
- **Negative (insecure):** CRLF reaches the header, or traversal in the served
  name. See [CRLF Injection](../../upstream/PayloadsAllTheThings/CRLF%20Injection/README.md).

**5.4.3 (L2):** files from untrusted sources AV-scanned. **5.1.1 (L2)** / **5.2.4
(L3)** / **5.2.5 (L3):** documented allowed types/sizes; per-user quota; reject
archives containing symlinks unless explicitly needed.

---
*Covers ASVS V5.1–V5.4. SSRF via image/URL fetch (MiniMagick/carrierwave
remote URL): [V15 §15.3.2](V15-secure-coding-and-architecture.md).*
