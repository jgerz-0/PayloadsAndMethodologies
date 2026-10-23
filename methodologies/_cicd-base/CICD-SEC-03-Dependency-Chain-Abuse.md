# CICD-SEC-3: Dependency Chain Abuse (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-3** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-03-Dependency-Chain-Abuse.md`](../../upstream/cicd-top-10/CICD-SEC-03-Dependency-Chain-Abuse.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

Dependency chain abuse risks refer to an attacker’s ability to abuse flaws relating to how engineering workstations and build environments fetch code dependencies. Dependency chain abuse results in a malicious package inadvertently being fetched and executed locally when pulled.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `repository_dependency_scanning_enabled` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
