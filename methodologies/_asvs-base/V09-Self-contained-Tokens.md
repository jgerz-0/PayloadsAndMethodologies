# V9 – Self-contained Tokens (ASVS 5.0)

> **ASVS 5.0 · Chapter V9** · Requirement IDs, levels, and text are verbatim from the official standard.
> Source: [`upstream/ASVS/5.0/en/0x18-V9-Self-contained-Tokens.md`](../../upstream/ASVS/5.0/en/0x18-V9-Self-contained-Tokens.md)
>
> **Role in this repo:** framework-agnostic base. When a framework methodology is generated (see [`_asvs-base/README.md`](README.md) and the `create-methodology` skill), every requirement below is projected onto the target stack as: the concrete mechanism/sink, how to test it, payloads (where applicable), and **positive (secure) vs negative (insecure) response examples**.

> **Level key:** `L1` baseline · `L2` standard (most apps) · `L3` high-assurance.

## Control Objective

The concept of a self-contained token is mentioned in the original RFC 6749 OAuth 2.0 from 2012. It refers to a token containing data or claims on which a receiving service will rely to make security decisions. This should be differentiated from a simple token containing only an identifier, which a receiving service uses to look up data locally. The most common examples of self-contained tokens are JSON Web Tokens (JWTs) and SAML assertions.

The use of self-contained tokens has become very widespread, even outside of OAuth and OIDC. At the same time, the security of this mechanism relies on the ability to validate the integrity of the token and to ensure that the token is valid for a particular context. There are many pitfalls with this process, and this chapter provides specific details of the mechanisms that applications should have in place to prevent them.

## V9.1 Token source and integrity

This section includes requirements to ensure that the token has been produced by a trusted party and has not been tampered with.

| # | L | Requirement |
| :-- | :--: | :-- |
| **9.1.1** | 1 | Verify that self-contained tokens are validated using their digital signature or MAC to protect against tampering before accepting the token's contents. |
| **9.1.2** | 1 | Verify that only algorithms on an allowlist can be used to create and verify self-contained tokens, for a given context. The allowlist must include the permitted algorithms, ideally only either symmetric or asymmetric algorithms, and must not include the 'None' algorithm. If both symmetric and asymmetric must be supported, additional controls will be needed to prevent key confusion. |
| **9.1.3** | 1 | Verify that key material that is used to validate self-contained tokens is from trusted pre-configured sources for the token issuer, preventing attackers from specifying untrusted sources and keys. For JWTs and other JWS structures, headers such as 'jku', 'x5u', and 'jwk' must be validated against an allowlist of trusted sources. |

## V9.2 Token content

Before making security decisions based on the content of a self-contained token, it is necessary to validate that the token has been presented within its validity period and that it is intended for use by the receiving service and for the purpose for which it was presented. This helps avoid insecure cross-usage between different services or with different token types from the same issuer.

Specific requirements for OAuth and OIDC are covered in the dedicated chapter.

| # | L | Requirement |
| :-- | :--: | :-- |
| **9.2.1** | 1 | Verify that, if a validity time span is present in the token data, the token and its content are accepted only if the verification time is within this validity time span. For example, for JWTs, the claims 'nbf' and 'exp' must be verified. |
| **9.2.2** | 2 | Verify that the service receiving a token validates the token to be the correct type and is meant for the intended purpose before accepting the token's contents. For example, only access tokens can be accepted for authorization decisions and only ID Tokens can be used for proving user authentication. |
| **9.2.3** | 2 | Verify that the service only accepts tokens which are intended for use with that service (audience). For JWTs, this can be achieved by validating the 'aud' claim against an allowlist defined in the service. |
| **9.2.4** | 2 | Verify that, if a token issuer uses the same private key for issuing tokens to different audiences, the issued tokens contain an audience restriction that uniquely identifies the intended audiences. This will prevent a token from being reused with an unintended audience. If the audience identifier is dynamically provisioned, the token issuer must validate these audiences in order to make sure that they do not result in audience impersonation. |

## References

For more information, see also:

* [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html)

---

### Framework projection (filled per stack, not here)

This base page lists *what* must hold. A framework methodology page answers *how to test it on that stack*. For each requirement above, the generated page should provide, where testable black/grey-box:

- **Mechanism / sink** — the framework API, config, or pattern that satisfies or violates the requirement.
- **How to test** — concrete steps; **payload(s)** when an input is sent.
- **Positive response (secure)** — what a correctly-configured app returns (status, headers, body, behaviour).
- **Negative response (insecure)** — what a vulnerable app returns, i.e. the confirmation signal for the finding.
