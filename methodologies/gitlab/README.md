# GitLab (CI/CD & Groups) Testing Methodology (CICD-SEC-aligned)

> Offensive testing methodology for **GitLab** groups/projects and **GitLab
> CI/CD**, structured against the [CI/CD base](../_cicd-base/README.md) (OWASP
> Top 10 CI/CD Security Risks). Each CICD-SEC risk is projected onto GitLab with
> the concrete setting/sink, how to test (API/pipeline), and **positive (secure)
> vs negative (vulnerable)** evidence.

> **No Prowler provider for GitLab** — verify via the GitLab **API** (`glab` /
> REST) and pipeline review. **Authorization:** test only groups/projects you're
> authorized to; poisoned-pipeline tests run code on runners — assume an
> **authorized** engagement and prove non-destructively.

## GitLab CI/CD model (what you're attacking)
| Element | Notes |
|---|---|
| **`.gitlab-ci.yml`** | pipeline definition; runs on runners per job |
| **Runners** | **shared** (SaaS/instance) vs group/project; **shell/Docker executor** — a shell executor is RCE on the host |
| **`CI_JOB_TOKEN`** | per-job token; its **allowlist** controls cross-project API access (abuse = lateral movement) |
| **CI/CD variables** | **masked** (hidden in logs) vs **protected** (only protected refs); masked ≠ secret — exfiltratable |
| **Protected branches/tags/environments** | gate who can push/deploy |
| **Tokens** | personal / **project** / **group** access tokens, deploy tokens, deploy keys |

## Tooling
- **glab CLI** + GitLab REST API; **[poutine](https://github.com/boostsecurityio/poutine)** (GitLab pipeline SAST), **trufflehog** (secrets), manual `.gitlab-ci.yml` review.
- No Prowler `gitlab` provider — base cross-refs are to the OWASP risk, not a check ID.

## Pages → CICD-SEC risks
| Page | CICD-SEC risks |
|---|---|
| [01 Access & flow control](01-access-and-flow-control.md) | [1](../_cicd-base/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md) · [2](../_cicd-base/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md) · [5](../_cicd-base/CICD-SEC-05-Insufficient-PBAC.md) |
| [02 Pipeline execution & dependencies](02-pipeline-execution-and-dependencies.md) | [3](../_cicd-base/CICD-SEC-03-Dependency-Chain-Abuse.md) · [4](../_cicd-base/CICD-SEC-04-Poisoned-Pipeline-Execution.md) · [8](../_cicd-base/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md) |
| [03 Credentials, artifacts & logging](03-credentials-artifacts-logging.md) | [6](../_cicd-base/CICD-SEC-06-Insufficient-Credential-Hygiene.md) · [7](../_cicd-base/CICD-SEC-07-Insecure-System-Configuration.md) · [9](../_cicd-base/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md) · [10](../_cicd-base/CICD-SEC-10-Insufficient-Logging-And-Visibility.md) |

## Adjacent scope
Where a pipeline deploys to a cloud account (OIDC / stored creds) → the matching
[cloud methodology](../_cloud-base/README.md). The app being built → [ASVS](../_asvs-base/README.md).

## References
- [CI/CD base](../_cicd-base/README.md) · [OWASP Top 10 CI/CD](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
- [GitLab CI/CD security](https://docs.gitlab.com/ee/ci/pipelines/pipeline_security.html)
