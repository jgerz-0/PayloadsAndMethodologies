# CICD-SEC-4: Poisoned Pipeline Execution (PPE) (CI/CD)

> **OWASP Top 10 CI/CD Security Risks · CICD-SEC-4** · ID, title, and Definition are verbatim from the official standard.
> Source: [`upstream/cicd-top-10/CICD-SEC-04-Poisoned-Pipeline-Execution.md`](../../upstream/cicd-top-10/CICD-SEC-04-Poisoned-Pipeline-Execution.md)
>
> **Role in this repo:** framework-agnostic CI/CD base. A generated methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) projects this risk onto the platform: the concrete setting/sink, how to test it, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler `github` check where applicable.

## Definition (verbatim)

Poisoned Pipeline Execution (PPE) risks refer to the ability of an attacker with access to source control systems - and without access to the build environment, to manipulate the build process by injecting malicious code/commands into the build pipeline configuration, essentially ‘poisoning’ the pipeline and running malicious code as part of the build process.

## Detective coverage — Prowler `github` checks

| Check ID |
| :-- |
| `organization_default_workflow_permissions_read_only` |
| `repository_default_workflow_permissions_read_only` |
| `githubactions_workflow_security_scan` |

---

### Methodology projection (filled per platform, not here)

- **Setting / sink** — the concrete platform control (branch protection, runner config, token scope, OIDC trust, webhook, workflow permissions).
- **How to test** — the API/UI check or attack (e.g. open a PR that edits the pipeline file; request the repo's secrets via a poisoned workflow).
- **Positive (secure)** — control enforced / action blocked.
- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; the Prowler check above (GitHub) flags the gap.
