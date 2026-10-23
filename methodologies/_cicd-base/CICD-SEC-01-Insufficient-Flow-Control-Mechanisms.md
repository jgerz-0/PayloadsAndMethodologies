# CICD-SEC-1: Insufficient Flow Control Mechanisms (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-1** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md`](../../upstream/cicd-top-10/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

Insufficient flow control mechanisms refer to the ability of an attacker that has obtained permissions to a system within the CI/CD process (SCM, CI, Artifact repository, etc.) to single handedly push malicious code or artifacts down the pipeline, due to a lack in mechanisms that enforce additional approval or review.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `repository_default_branch_protection_enabled` |
| `repository_default_branch_requires_multiple_approvals` |
| `repository_default_branch_status_checks_required` |
| `organization_actions_pull_request_approval_disabled` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
