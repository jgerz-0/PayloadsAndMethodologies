# GitHub (Actions & Org) Testing Methodology (CICD-SEC-aligned)

> Offensive testing methodology for **GitHub** organizations and **GitHub
> Actions**, structured against the [CI/CD base](../_cicd-base/README.md) (OWASP
> Top 10 CI/CD Security Risks). Each CICD-SEC risk is projected onto GitHub with
> the concrete setting/sink, how to test (API/workflow), and **positive (secure)
> vs negative (vulnerable)** evidence, tied to the **Prowler `github` check ID**.

> **Authorization.** Test only orgs/repos you're authorized to. Poisoned-pipeline
> tests execute code on runners — assume an **authorized** engagement and prefer
> non-destructive proof (e.g. echo a canary, don't exfiltrate real secrets).

## GitHub CI/CD model (what you're attacking)
| Element | Notes |
|---|---|
| **Actions workflows** (`.github/workflows/*.yml`) | triggered by events; run on runners |
| **`GITHUB_TOKEN`** | auto-minted per-run token; its **permissions** scope the blast radius |
| **Secrets / variables** | repo / environment / org scoped; exposed to workflows |
| **OIDC** | workflows mint cloud creds via OIDC trust (→ [cloud base](../_cloud-base/README.md)) |
| **Runners** | GitHub-hosted (ephemeral) vs **self-hosted** (persistent → high-value target) |
| **PATs / Apps / deploy keys** | long-lived credentials; over-scoped PATs are common |

## Tooling
- **gh CLI** + GitHub REST/GraphQL API; **[gato-x](https://github.com/praetorian-inc/gato-x)** (Actions attack/enumeration), **[Legitify](https://github.com/Legit-Labs/legitify)** (posture), **[poutine](https://github.com/boostsecurityio/poutine)** (pipeline SAST), **trufflehog** (secrets in history).
- **[Prowler](../../upstream/prowler/)** — `prowler github` (27 checks); findings name the check ID.

## Pages → CICD-SEC risks
| Page | CICD-SEC risks |
|---|---|
| [01 Access & flow control](01-access-and-flow-control.md) | [1](../_cicd-base/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md) · [2](../_cicd-base/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md) · [5](../_cicd-base/CICD-SEC-05-Insufficient-PBAC.md) |
| [02 Pipeline execution & dependencies](02-pipeline-execution-and-dependencies.md) | [3](../_cicd-base/CICD-SEC-03-Dependency-Chain-Abuse.md) · [4](../_cicd-base/CICD-SEC-04-Poisoned-Pipeline-Execution.md) · [8](../_cicd-base/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md) |
| [03 Credentials, artifacts & logging](03-credentials-artifacts-logging.md) | [6](../_cicd-base/CICD-SEC-06-Insufficient-Credential-Hygiene.md) · [7](../_cicd-base/CICD-SEC-07-Insecure-System-Configuration.md) · [9](../_cicd-base/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md) · [10](../_cicd-base/CICD-SEC-10-Insufficient-Logging-And-Visibility.md) |

## Adjacent scope
Where a workflow deploys via OIDC to a cloud account, continue in the matching
[cloud methodology](../_cloud-base/README.md). The app being built → [ASVS](../_asvs-base/README.md).

## References
- [CI/CD base](../_cicd-base/README.md) · [OWASP Top 10 CI/CD](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
- [GitHub Actions security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
