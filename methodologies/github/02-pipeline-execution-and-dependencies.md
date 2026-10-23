# GitHub · Pipeline Execution & Dependencies

> CICD-SEC [4 Poisoned Pipeline Execution](../_cicd-base/CICD-SEC-04-Poisoned-Pipeline-Execution.md),
> [3 Dependency Chain Abuse](../_cicd-base/CICD-SEC-03-Dependency-Chain-Abuse.md),
> [8 Ungoverned 3rd-Party Services](../_cicd-base/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md),
> projected onto GitHub Actions.

## CICD-SEC-4 — Poisoned Pipeline Execution (PPE)  ⭐
- **Setting/sink:** workflows that run **untrusted code with secrets/write token**:
  - `pull_request_target` + checking out the PR head → attacker PR code runs with
    the base repo's secrets and a write `GITHUB_TOKEN` (the classic GitHub PPE).
  - `workflow_run` chained off untrusted workflows.
  - **Self-hosted runners** on public repos → any forked PR runs code on your
    persistent runner (RCE, runner compromise, lateral movement).
- **How to test:** `gato-x` enumerate+attack; open a PR that edits a referenced
  script/test/action (Indirect PPE) or the workflow (Direct PPE) to echo a canary
  / print `env`.
- **Positive (secure):** no `pull_request_target` checkout of PR code; forked-PR
  workflows require approval (`organization_actions_pull_request_approval_disabled`
  = false → approval required); ephemeral GitHub-hosted runners; workflow perms
  read-only. Prowler `githubactions_workflow_security_scan`,
  `*_default_workflow_permissions_read_only`.
- **Negative (vulnerable):** your PR's code executes in CI with secrets / a
  write token / on a self-hosted runner → secret exfil, repo tamper, pivot.

## CICD-SEC-3 — Dependency chain abuse
- **Setting/sink:** unpinned **Actions** (`uses: org/action@main` or a mutable
  tag, not a SHA), dependency confusion in package installs during build,
  typosquatted actions.
- **How to test:** review workflows for `@main`/`@v3` (mutable) action refs;
  check internal package names claimable on public registries.
- **Positive (secure):** actions pinned by **full commit SHA**; dependency
  scanning on (`repository_dependency_scanning_enabled`); private registry scoping.
- **Negative (vulnerable):** a mutable third-party action can be updated by its
  owner (or a compromised owner) to run in your pipeline → supply-chain RCE.

## CICD-SEC-8 — Ungoverned 3rd-party services
- **Setting/sink:** OAuth apps / GitHub Apps installed org-wide with broad scopes;
  marketplace actions with repo access.
  ```sh
  gh api orgs/<org>/installations
  ```
- **Positive (secure):** app installs restricted/reviewed; least-scope.
  **Negative (vulnerable):** a broad third-party app/integration = standing
  access an attacker can abuse or that widens blast radius.

---
*Base: [CICD-SEC 4](../_cicd-base/CICD-SEC-04-Poisoned-Pipeline-Execution.md) ·
[3](../_cicd-base/CICD-SEC-03-Dependency-Chain-Abuse.md) ·
[8](../_cicd-base/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md). Next:
[Credentials, Artifacts & Logging](03-credentials-artifacts-logging.md).*
