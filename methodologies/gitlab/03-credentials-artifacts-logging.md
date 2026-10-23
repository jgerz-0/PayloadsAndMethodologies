# GitLab · Credentials, Artifacts & Logging

> CICD-SEC [6 Credential Hygiene](../_cicd-base/CICD-SEC-06-Insufficient-Credential-Hygiene.md),
> [7 Insecure System Configuration](../_cicd-base/CICD-SEC-07-Insecure-System-Configuration.md),
> [9 Artifact Integrity](../_cicd-base/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md),
> [10 Logging & Visibility](../_cicd-base/CICD-SEC-10-Insufficient-Logging-And-Visibility.md).

## CICD-SEC-6 — Insufficient credential hygiene
- **Setting/sink:** CI/CD **variables** (masked vs protected), secrets in job
  logs / git history, long-lived access/deploy tokens, and **ID-token/OIDC**
  trust to cloud (`aud`/`sub` too broad).
  ```sh
  glab api projects/<id>/variables           # masked? protected? (masked still echo-able)
  trufflehog gitlab --repo <url>
  ```
- **Positive (secure):** secrets **protected + masked**, scoped to protected refs;
  OIDC `sub` pinned to project + ref/environment; short-lived tokens; external
  secrets (Vault).
- **Negative (vulnerable):** a masked-only variable exfiltrated by a poisoned job
  (base64/char-split to defeat masking), secret in history, or broad OIDC trust →
  pipeline→cloud compromise (continue in the [cloud methodology](../_cloud-base/README.md)).

## CICD-SEC-7 — Insecure system configuration
- **Setting/sink:** runner hardening (shell vs Docker, privileged Docker-in-
  Docker, `--privileged`), self-managed GitLab/runner versions (known CVEs),
  branch-protection bypass, `CI_JOB_TOKEN` default-allow-all (older defaults).
- **Positive (secure):** isolated non-privileged runners; patched GitLab/runner;
  job-token scope restricted; signed commits where required.
- **Negative (vulnerable):** privileged DinD runner → host/container escape; an
  outdated self-managed GitLab maps to a public CVE.

## CICD-SEC-9 — Improper artifact integrity validation
- **Setting/sink:** unsigned artifacts/packages in the GitLab Package/Container
  Registry; no provenance/attestation; mutable tags.
- **Positive (secure):** signed artifacts (Sigstore/cosign), provenance,
  protected/immutable package versions.
- **Negative (vulnerable):** unsigned, mutable artifacts → tampered build ships
  downstream undetected.

## CICD-SEC-10 — Insufficient logging & visibility
- **Setting/sink:** **audit events** (group/instance), pipeline + job logs
  retention, alerts on variable/role/runner changes.
  ```sh
  glab api groups/<id>/audit_events          # (Premium/Ultimate)
  ```
- **Positive (secure):** audit events streamed to a SIEM; alerts on sensitive
  changes. **Negative (vulnerable):** no audit streaming / short log retention →
  pipeline tampering and secret access go unseen.

---
*Base: [CICD-SEC 6](../_cicd-base/CICD-SEC-06-Insufficient-Credential-Hygiene.md) ·
[7](../_cicd-base/CICD-SEC-07-Insecure-System-Configuration.md) ·
[9](../_cicd-base/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md) ·
[10](../_cicd-base/CICD-SEC-10-Insufficient-Logging-And-Visibility.md). Back to
[GitLab README](README.md).*
