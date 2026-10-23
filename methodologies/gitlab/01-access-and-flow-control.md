# GitLab · Access & Flow Control

> CICD-SEC [1 Flow Control](../_cicd-base/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md),
> [2 IAM](../_cicd-base/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md),
> [5 PBAC](../_cicd-base/CICD-SEC-05-Insufficient-PBAC.md), projected onto GitLab.

## CICD-SEC-1 — Insufficient flow control (protected branches / MR approvals)
- **Setting/sink:** protected branches + **merge request approval rules**
  (required approvers, reset on push, no self-approval), "pipelines must succeed".
  ```sh
  glab api projects/<id>/protected_branches
  glab api projects/<id>/approval_rules
  ```
- **Positive (secure):** default branch protected; ≥1 required approval; approvals
  reset on new commits; authors can't approve their own MR.
- **Negative (vulnerable):** no protection / 0 approvals / self-approval allowed →
  merge unreviewed code that then runs in CI ([PPE](02-pipeline-execution-and-dependencies.md)).

## CICD-SEC-2 — Inadequate identity & access management
- **Setting/sink:** group/project **roles** (Guest/Reporter/Developer/Maintainer/
  Owner), external/invited users, **2FA** enforcement, over-scoped **access
  tokens** (personal/project/group) and deploy tokens.
  ```sh
  glab api groups/<id>/members/all ; glab api projects/<id>/access_tokens
  glab api groups/<id> --jq '.require_two_factor_authentication'
  ```
- **Positive (secure):** 2FA enforced group-wide; least-privilege roles; scoped,
  expiring tokens; minimal Owners/Maintainers.
- **Negative (vulnerable):** 2FA off, broad Developer+ access, or a leaked
  over-scoped token (api scope) → project/group takeover surface.

## CICD-SEC-5 — Insufficient PBAC (CI_JOB_TOKEN & protected context)
- **Setting/sink:** `CI_JOB_TOKEN` **allowlist** (which projects a job's token may
  access) and **protected variables/environments** (secrets only on protected
  refs).
  ```sh
  glab api projects/<id>/job_token_scope
  ```
- **Positive (secure):** job-token scope limited to required projects; deploy
  secrets in **protected** variables + protected environments with approvers.
- **Negative (vulnerable):** `CI_JOB_TOKEN` can reach unrelated projects' APIs →
  a compromised/poisoned job pivots across projects; protected secrets exposed to
  unprotected branches.

---
*Base: [CICD-SEC 1](../_cicd-base/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md) ·
[2](../_cicd-base/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md) ·
[5](../_cicd-base/CICD-SEC-05-Insufficient-PBAC.md). Next:
[Pipeline Execution & Dependencies](02-pipeline-execution-and-dependencies.md).*
