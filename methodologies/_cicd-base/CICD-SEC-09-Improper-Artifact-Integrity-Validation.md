# CICD-SEC-9: Improper Artifact Integrity Validation (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-9** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md`](../../upstream/cicd-top-10/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

Improper artifact integrity validation risks allow an attacker with access to one of the systems in the CI/CD process to push malicious (although seemingly benign) code or artifacts down the pipeline, due to insufficient mechanisms for ensuring the validation of code and artifacts.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `repository_default_branch_requires_signed_commits` |
| `repository_immutable_releases_enabled` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
