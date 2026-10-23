# CICD-SEC-5: Insufficient PBAC (Pipeline-Based Access Controls) (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-5** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-05-Insufficient-PBAC.md`](../../upstream/cicd-top-10/CICD-SEC-05-Insufficient-PBAC.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

Pipeline execution nodes have access to numerous resources and systems within and outside the execution environment. When running malicious code within a pipeline, adversaries leverage insufficient PBAC (Pipeline-Based Access Controls) risks to abuse the permission granted to the pipeline for moving laterally within or outside the CI/CD system.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `repository_default_workflow_permissions_read_only` |
| `organization_default_workflow_permissions_read_only` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
