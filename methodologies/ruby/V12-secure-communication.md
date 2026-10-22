# V12 – Secure Communication (Rails)

> **ASVS 5.0 · Chapter V12** — projected onto Ruby on Rails.
> Base: [`_asvs-base/V12-Secure-Communication.md`](../_asvs-base/V12-Secure-Communication.md).
> TLS for inbound and outbound connections. Inbound TLS/HSTS is usually
> terminated at a proxy (test with `testssl.sh`); the Rails-specific risk is
> **outbound TLS certificate verification being disabled**.

## V12.1 / V12.2 TLS configuration (inbound)

#### 12.1.1 / 12.1.2 — TLS versions & cipher suites · L1/L2
- **Mechanism:** terminated at nginx/ALB/Puma. Rails' part is
  `config.force_ssl = true` (redirect + HSTS + `Secure` cookies — see
  [V3.4.1](V03-web-frontend-security.md)).
- **Test:** `testssl.sh https://TARGET` ; `curl -sD- http://TARGET/ -o /dev/null | grep -i location`
- **Positive:** only TLS 1.2/1.3; HTTP→HTTPS redirect; HSTS present.
- **Negative:** TLS 1.0/1.1 or weak ciphers enabled; plaintext HTTP served.

**12.2.1 / 12.2.2 (L1):** all client↔external traffic over TLS with publicly
trusted certs (no fallback to cleartext).

## V12.3 Service-to-service communication

#### 12.3.2 — Outbound TLS certificate validation · L2
- **Mechanism (Rails):** the #1 Rails finding in this chapter —
  `Net::HTTP` with `verify_mode = OpenSSL::SSL::VERIFY_NONE`,
  `http.verify_mode = OpenSSL::SSL::VERIFY_NONE`, HTTParty
  `verify: false`, Faraday `ssl: {verify: false}`, or `OpenSSL::SSL::SSLContext`
  with verification off. Disables MITM protection on calls to payment/identity/
  internal APIs.
- **How to test (grey/white-box):** grep `VERIFY_NONE|verify:\s*false|verify_mode`;
  black-box, MITM an outbound call with a self-signed cert and see if it's
  accepted.
- **Positive (secure):** certificates validated (`VERIFY_PEER`); self-signed/
  mismatched cert → connection fails.
- **Negative (insecure):** `VERIFY_NONE` → MITM of outbound traffic (credential/
  token theft, response tampering).

**12.3.1 / 12.3.3 / 12.3.4 (L2):** TLS for all inbound/outbound and internal
HTTP-based service connections, with trusted (or pinned internal) certs.
**12.1.3 (L2) mTLS**, **12.1.4/12.1.5 (L3)** OCSP stapling / Encrypted Client
Hello, **12.3.5 (L3)** strong intra-service authentication — infra-level;
confirm against the deployment.

---
*Covers ASVS V12.1–V12.3. HSTS/`force_ssl` detail: [V3](V03-web-frontend-security.md).*
