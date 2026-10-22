# V12 – Secure Communication (ASVS 5.0)

> **ASVS 5.0 · Chapter V12** · Requirement IDs, levels, and text are verbatim from the official standard.
> Source: [`upstream/ASVS/5.0/en/0x21-V12-Secure-Communication.md`](../../upstream/ASVS/5.0/en/0x21-V12-Secure-Communication.md)
>
> **Role in this repo:** framework-agnostic base. When a framework methodology is generated (see [`_asvs-base/README.md`](README.md) and the `create-methodology` skill), every requirement below is projected onto the target stack as: the concrete mechanism/sink, how to test it, payloads (where applicable), and **positive (secure) vs negative (insecure) response examples**.

> **Level key:** `L1` baseline · `L2` standard (most apps) · `L3` high-assurance.

## Control Objective

This chapter includes requirements related to the specific mechanisms that should be in place to protect data in transit, both between an end-user client and a backend service, as well as between internal and backend services.

The general concepts promoted by this chapter include:

* Ensuring that communications are encrypted externally, and ideally internally as well.
* Configuring encryption mechanisms using the latest guidance, including preferred algorithms and ciphers.
* Using signed certificates to ensure that communications are not being intercepted by unauthorized parties.

In addition to outlining general principles and best practices, the ASVS also provides more in-depth technical information about cryptographic strength in Appendix C - Cryptography Standards.

## V12.1 General TLS Security Guidance

This section provides initial guidance on how to secure TLS communications. Up-to-date tools should be used to review TLS configuration on an ongoing basis.

While the use of wildcard TLS certificates is not inherently insecure, a compromise of a certificate that is deployed across all owned environments (e.g., production, staging, development, and test) may lead to a compromise of the security posture of the applications using it. Proper protection, management, and the use of separate TLS certificates in different environments should be employed if possible.

| # | L | Requirement |
| :-- | :--: | :-- |
| **12.1.1** | 1 | Verify that only the latest recommended versions of the TLS protocol are enabled, such as TLS 1.2 and TLS 1.3. The latest version of the TLS protocol must be the preferred option. |
| **12.1.2** | 2 | Verify that only recommended cipher suites are enabled, with the strongest cipher suites set as preferred. L3 applications must only support cipher suites which provide forward secrecy. |
| **12.1.3** | 2 | Verify that the application validates that mTLS client certificates are trusted before using the certificate identity for authentication or authorization. |
| **12.1.4** | 3 | Verify that proper certification revocation, such as Online Certificate Status Protocol (OCSP) Stapling, is enabled and configured. |
| **12.1.5** | 3 | Verify that Encrypted Client Hello (ECH) is enabled in the application's TLS settings to prevent exposure of sensitive metadata, such as the Server Name Indication (SNI), during TLS handshake processes. |

## V12.2 HTTPS Communication with External Facing Services

Ensure all HTTP traffic to external-facing services which the application exposes is sent encrypted, with publicly trusted certificates.

| # | L | Requirement |
| :-- | :--: | :-- |
| **12.2.1** | 1 | Verify that TLS is used for all connectivity between a client and external facing, HTTP-based services, and does not fall back to insecure or unencrypted communications. |
| **12.2.2** | 1 | Verify that external facing services use publicly trusted TLS certificates. |

## V12.3 General Service to Service Communication Security

Server communications (both internal and external) involve more than just HTTP. Connections to and from other systems must also be secure, ideally using TLS.

| # | L | Requirement |
| :-- | :--: | :-- |
| **12.3.1** | 2 | Verify that an encrypted protocol such as TLS is used for all inbound and outbound connections to and from the application, including monitoring systems, management tools, remote access and SSH, middleware, databases, mainframes, partner systems, or external APIs. The server must not fall back to insecure or unencrypted protocols. |
| **12.3.2** | 2 | Verify that TLS clients validate certificates received before communicating with a TLS server. |
| **12.3.3** | 2 | Verify that TLS or another appropriate transport encryption mechanism used for all connectivity between internal, HTTP-based services within the application, and does not fall back to insecure or unencrypted communications. |
| **12.3.4** | 2 | Verify that TLS connections between internal services use trusted certificates. Where internally generated or self-signed certificates are used, the consuming service must be configured to only trust specific internal CAs and specific self-signed certificates. |
| **12.3.5** | 3 | Verify that services communicating internally within a system (intra-service communications) use strong authentication to ensure that each endpoint is verified. Strong authentication methods, such as TLS client authentication, must be employed to ensure identity, using public-key infrastructure and mechanisms that are resistant to replay attacks. For microservice architectures, consider using a service mesh to simplify certificate management and enhance security. |

## References

For more information, see also:

* [OWASP - Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
* [Mozilla's Server Side TLS configuration guide](https://wiki.mozilla.org/Security/Server_Side_TLS)
* [Mozilla's tool to generate known good TLS configurations](https://ssl-config.mozilla.org/).
* [O-Saft - OWASP Project to validate TLS configuration](https://owasp.org/www-project-o-saft/)

---

### Framework projection (filled per stack, not here)

This base page lists *what* must hold. A framework methodology page answers *how to test it on that stack*. For each requirement above, the generated page should provide, where testable black/grey-box:

- **Mechanism / sink** — the framework API, config, or pattern that satisfies or violates the requirement.
- **How to test** — concrete steps; **payload(s)** when an input is sent.
- **Positive response (secure)** — what a correctly-configured app returns (status, headers, body, behaviour).
- **Negative response (insecure)** — what a vulnerable app returns, i.e. the confirmation signal for the finding.
