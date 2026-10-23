# CICD-SEC-2: Inadequate Identity and Access Management (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-2** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md`](../../upstream/cicd-top-10/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

Inadequate Identity and Access Management risks stem from the difficulties in managing the vast amount of identities spread across the different systems in the engineering ecosystem, from source control to deployment. The existence of poorly managed identities - both human and programmatic accounts - increases the potential and the extent of damage of their compromise.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `organization_members_mfa_required` |
| `organization_default_repository_permission_strict` |
| `repository_default_branch_protection_applies_to_admins` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
