# GitHub · Credentials, Artifacts & Logging

> CICD-SEC [6 Credential Hygiene](../_cicd-base/CICD-SEC-06-Insufficient-Credential-Hygiene.md),
> [7 Insecure System Configuration](../_cicd-base/CICD-SEC-07-Insecure-System-Configuration.md),
> [9 Artifact Integrity](../_cicd-base/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md),
> [10 Logging & Visibility](../_cicd-base/CICD-SEC-10-Insufficient-Logging-And-Visibility.md).

## CICD-SEC-6 — Insufficient credential hygiene
- **Setting/sink:** secrets in git history / logs / env; over-scoped
  `GITHUB_TOKEN`; long-lived PATs; **OIDC** trust that's too broad (cloud role
  assumable from any repo/branch).
  ```sh
  trufflehog github --org <org>                       # secrets in history
  # review cloud OIDC trust: sub claim should pin repo + ref/environment
  ```
- **Positive (secure):** secret scanning + push protection on
  (`repository_secret_scanning_enabled`); OIDC `sub` pinned to
  `repo:org/repo:ref:refs/heads/main` or an environment; short-lived creds.
- **Negative (vulnerable):** live secret in history; OIDC trust `repo:org/*` →
  any branch/PR mints the cloud role → pipeline→cloud compromise (continue in the
  [cloud methodology](../_cloud-base/README.md)).

## CICD-SEC-7 — Insecure system configuration
- **Setting/sink:** self-hosted runner hardening (non-ephemeral, over-privileged,
  shared across repos), branch-protection bypasses, no signed commits / linear
  history, force-push allowed.
- **Positive (secure):** ephemeral/isolated runners; signed commits + linear
  history + no force-push. Prowler `repository_default_branch_requires_signed_commits`,
  `repository_default_branch_requires_linear_history`,
  `repository_default_branch_disallows_force_push`.
- **Negative (vulnerable):** persistent shared runner / force-push to protected
  branch → tamper and persistence.

## CICD-SEC-9 — Improper artifact integrity validation
- **Setting/sink:** unsigned build artifacts/releases; no provenance (SLSA /
  Sigstore); mutable releases.
- **Positive (secure):** signed commits/tags, build provenance/attestations,
  immutable releases (`repository_immutable_releases_enabled`).
- **Negative (vulnerable):** artifacts/releases unsigned & mutable → a tampered
  artifact ships undetected downstream.

## CICD-SEC-10 — Insufficient logging & visibility
- **Setting/sink:** org **audit log** streaming; Actions run logs retention.
  ```sh
  gh api orgs/<org>/audit-log --jq '.[0]'             # (enterprise)
  ```
- **Positive (secure):** audit log streamed to a SIEM; alerts on secret/role
  changes. **Negative (vulnerable):** no audit streaming → pipeline tampering and
  secret access go unseen. (Verify via settings/API — no direct Prowler check.)

---
*Base: [CICD-SEC 6](../_cicd-base/CICD-SEC-06-Insufficient-Credential-Hygiene.md) ·
[7](../_cicd-base/CICD-SEC-07-Insecure-System-Configuration.md) ·
[9](../_cicd-base/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md) ·
[10](../_cicd-base/CICD-SEC-10-Insufficient-Logging-And-Visibility.md). Back to
[GitHub README](README.md).*
