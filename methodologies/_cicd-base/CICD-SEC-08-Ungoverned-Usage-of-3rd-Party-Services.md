# CICD-SEC-8: Ungoverned Usage of 3rd Party Services (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-8** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md`](../../upstream/cicd-top-10/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

The CI/CD attack surface consists of an organization’s organic assets, such as the SCM or CI, and the 3rd party services which are granted access to those organic assets. Risks having to do with ungoverned usage of 3rd party services rely on the extreme ease with which a 3rd party service can be granted access to resources in CI/CD systems, effectively expanding the attack surface of the organization.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `organization_repository_creation_limited` |
| `organization_default_repository_permission_strict` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
