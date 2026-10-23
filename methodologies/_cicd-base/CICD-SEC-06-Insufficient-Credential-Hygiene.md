# CICD-SEC-6: Insufficient Credential Hygiene (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-6** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-06-Insufficient-Credential-Hygiene.md`](../../upstream/cicd-top-10/CICD-SEC-06-Insufficient-Credential-Hygiene.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

Insufficient credential hygiene risks deal with an attacker’s ability to obtain and use various secrets and tokens spread throughout the pipeline due to flaws having to do with access controls around the credentials, insecure secret management and overly permissive credentials.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `repository_secret_scanning_enabled` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
