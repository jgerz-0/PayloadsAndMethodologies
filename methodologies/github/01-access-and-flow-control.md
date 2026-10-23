# GitHub · Access & Flow Control

> CICD-SEC [1 Flow Control](../_cicd-base/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md),
> [2 IAM](../_cicd-base/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md),
> [5 PBAC](../_cicd-base/CICD-SEC-05-Insufficient-PBAC.md), projected onto GitHub.

## CICD-SEC-1 — Insufficient flow control (branch protection)
- **Setting/sink:** branch protection / rulesets on the default branch — required
  reviews, required status checks, no force-push, no self-approval.
  ```sh
  gh api repos/<org>/<repo>/branches/main/protection
  ```
- **Positive (secure):** protection on, ≥1 required review, dismiss stale reviews,
  applies to admins. Prowler `repository_default_branch_protection_enabled`,
  `repository_default_branch_requires_multiple_approvals`,
  `repository_default_branch_status_checks_required`,
  `repository_default_branch_protection_applies_to_admins`.
- **Negative (vulnerable):** no protection / admins bypass / 0 reviews → push
  unreviewed code straight to main → it runs in CI (see
  [PPE](02-pipeline-execution-and-dependencies.md)).

## CICD-SEC-2 — Inadequate identity & access management
- **Setting/sink:** org/repo roles, outside collaborators, **MFA enforcement**,
  default member permission, stale/over-scoped **PATs** and SSH keys.
  ```sh
  gh api orgs/<org> --jq '.default_repository_permission,.two_factor_requirement_enabled'
  gh api orgs/<org>/outside_collaborators
  ```
- **Positive (secure):** org-wide MFA required; default permission `read`;
  minimal admins. Prowler `organization_members_mfa_required`,
  `organization_default_repository_permission_strict`.
- **Negative (vulnerable):** MFA not enforced, broad default write, many admins,
  or an over-scoped PAT (repo+workflow+admin:org) recovered from a leak → org
  takeover surface.

## CICD-SEC-5 — Insufficient PBAC (pipeline-based access controls)
- **Setting/sink:** the `GITHUB_TOKEN` **default permissions** and **environment
  protection rules**. A read-write default token lets any workflow (and any
  injected code in it) push code, create releases, or approve PRs.
  ```yaml
  # workflow should scope down:
  permissions: { contents: read }
  ```
- **Positive (secure):** org/repo default workflow permissions **read-only**;
  protected environments require reviewers for deploy jobs. Prowler
  `organization_default_workflow_permissions_read_only`,
  `repository_default_workflow_permissions_read_only`.
- **Negative (vulnerable):** default `GITHUB_TOKEN` is read-write → a poisoned or
  compromised workflow uses it to tamper with the repo/releases.

---
*Base: [CICD-SEC 1](../_cicd-base/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md) ·
[2](../_cicd-base/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md) ·
[5](../_cicd-base/CICD-SEC-05-Insufficient-PBAC.md). Next:
[Pipeline Execution & Dependencies](02-pipeline-execution-and-dependencies.md).*
