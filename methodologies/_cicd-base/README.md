# CI/CD Base (OWASP Top 10 CI/CD Security Risks + Prowler)

> Framework-agnostic **source of truth** for CI/CD and SCM-platform testing
> (GitHub, GitLab, Jenkins, …). These aren't covered by ASVS/MASVS/ATT&CK-cloud/
> K8s, so they get their own base anchored on the recognized standard — the
> **OWASP Top 10 CI/CD Security Risks** (vendored at
> [`upstream/cicd-top-10`](../../upstream/cicd-top-10/)) — cross-referenced to
> **Prowler** `github` checks ([`upstream/prowler`](../../upstream/prowler/), 27
> checks) where the platform is GitHub.

One markdown per risk (CICD-SEC-1..10), ID/title/Definition **verbatim** from
OWASP. The base says **what** can go wrong in a pipeline; the
[`github/`](../github/README.md) and [`gitlab/`](../gitlab/README.md)
methodologies say **how to test it** on each platform.

## Risks (OWASP Top 10 CI/CD Security Risks)

| Risk | Title | GitHub Prowler checks | Base page |
|---|---|--:|---|
| CICD-SEC-1 | Insufficient Flow Control Mechanisms | 4 | [01](CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md) |
| CICD-SEC-2 | Inadequate Identity & Access Management | 3 | [02](CICD-SEC-02-Inadequate-Identity-And-Access-Management.md) |
| CICD-SEC-3 | Dependency Chain Abuse | 1 | [03](CICD-SEC-03-Dependency-Chain-Abuse.md) |
| CICD-SEC-4 | Poisoned Pipeline Execution (PPE) | 3 | [04](CICD-SEC-04-Poisoned-Pipeline-Execution.md) |
| CICD-SEC-5 | Insufficient PBAC (Pipeline-Based Access Controls) | 2 | [05](CICD-SEC-05-Insufficient-PBAC.md) |
| CICD-SEC-6 | Insufficient Credential Hygiene | 1 | [06](CICD-SEC-06-Insufficient-Credential-Hygiene.md) |
| CICD-SEC-7 | Insecure System Configuration | 3 | [07](CICD-SEC-07-Insecure-System-Configuration.md) |
| CICD-SEC-8 | Ungoverned Usage of 3rd Party Services | 2 | [08](CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md) |
| CICD-SEC-9 | Improper Artifact Integrity Validation | 2 | [09](CICD-SEC-09-Improper-Artifact-Integrity-Validation.md) |
| CICD-SEC-10 | Insufficient Logging and Visibility | 0¹ | [10](CICD-SEC-10-Insufficient-Logging-And-Visibility.md) |

¹ Verify via the platform's audit-log configuration / API.

## Which base
Use this for the **CI/CD and source-control platform** (GitHub/GitLab orgs,
Actions/Pipelines, runners). The **app** being built is [ASVS](../_asvs-base/README.md);
where the pipeline deploys to a **cloud** account, the pipeline's cloud
credentials/OIDC trust tie into the [cloud base](../_cloud-base/README.md).

## Regenerating
```sh
git submodule update --remote upstream/cicd-top-10 upstream/prowler
python3 methodologies/_cicd-base/generate.py
git add upstream/cicd-top-10 upstream/prowler methodologies/_cicd-base
git commit -m "chore: regenerate cicd base"
```

## References
- [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/) (vendored)
- [Prowler](../../upstream/prowler/) `github` provider · tools: [gato(-x)](https://github.com/praetorian-inc/gato-x) (GitHub Actions attack), [Legitify](https://github.com/Legit-Labs/legitify), [poutine](https://github.com/boostsecurityio/poutine) (pipeline SAST), [tartufo](https://github.com/godaddy/tartufo)/trufflehog (secrets)
- Siblings: [ASVS](../_asvs-base/README.md) · [cloud base](../_cloud-base/README.md)
