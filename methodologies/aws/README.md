# AWS Cloud Testing Methodology (ATT&CK-aligned)

> Offensive testing methodology for **Amazon Web Services**, structured against
> the [cloud attack base](../_cloud-base/README.md) (MITRE ATT&CK cloud tactics
> + Prowler). Organized by **kill-chain phase**; within each, ATT&CK techniques
> are projected onto AWS services with the concrete API/sink, enumerate→attempt
> CLI, and **positive (secure, `AccessDenied`) vs negative (vulnerable, call
> succeeds)** evidence — each tied to the **Prowler check ID** that detects the
> underlying misconfiguration.

> **Authorization.** Cloud testing requires explicit authorization. AWS permits
> customer testing of many services without prior approval under its
> [pentest policy](https://aws.amazon.com/security/penetration-testing/), but
> **not** disruptive tests (DoS) or testing infra you don't own. Assume an
> **authorized** engagement. Prefer read/enumerate and dry-run over anything
> that modifies or impacts resources.

## AWS identity model (what you're attacking)

| Principal | Credential | Notes |
|---|---|---|
| IAM user | long-lived access key (`AKIA…`) + secret, or console password | key rotation → Prowler `iam_rotate_access_key_90_days` |
| IAM role | temporary STS creds (`ASIA…`) via `sts:AssumeRole` | the core of lateral movement |
| EC2 instance profile | role creds via **IMDS** (`169.254.169.254`) | SSRF → creds, T1552.005 |
| Lambda/ECS task role | role creds via env/metadata endpoint | |
| Identity Center (SSO) | federated short-lived creds | |
| Root | account owner | should have hardware MFA, no keys |

Everything authz is **IAM policy** (identity + resource + SCP + permission
boundary + session policy). The attacker's question is always: *what can this
principal do, and does any action let it become a more powerful principal?*

## Starting points
- **External / black-box:** no creds. Focus on public exposure (S3, snapshots,
  AMIs, ECR, ES/OpenSearch, RDS, APIs) and leaked keys.
- **Assumed-breach / grey-box:** given a set of creds (the common cloud-pentest
  model). Start at `sts get-caller-identity`, enumerate your own permissions,
  then walk privesc → lateral → impact.

## Tooling
- **awscli** — `aws <svc> <action>`; set `--profile`; `AWS_PROFILE`.
- **[Prowler](../../upstream/prowler/)** — `prowler aws` — the detective baseline;
  each finding below names its check ID. Run `prowler aws -c <check_id>`.
- **[ScoutSuite](https://github.com/nccgroup/ScoutSuite)** — multi-cloud audit UI.
- **[Pacu](https://github.com/RhinoSecurityLabs/pacu)** — AWS exploitation
  framework (`iam__enum_permissions`, `iam__privesc_scan`, `s3__download_bucket`).
- **[CloudFox](https://github.com/BishopFox/cloudfox)** — attacker-centric
  enumeration ("what can I do with these creds?").
- **enumerate-iam**, **weirdAAL**, **trufflehog** (leaked keys in repos).

## Phases → ATT&CK tactics

| Phase | Page | ATT&CK tactic(s) |
|---|---|---|
| Recon & enumeration | [01](01-recon-and-enumeration.md) | [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) |
| Access & credentials | [02](02-access-and-credentials.md) | [TA0001 Initial Access](../_cloud-base/TA0001-initial-access.md) · [TA0006 Credential Access](../_cloud-base/TA0006-credential-access.md) |
| Privilege escalation | [03](03-privilege-escalation.md) | [TA0004 Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md) |
| Lateral movement & persistence | [04](04-lateral-movement-and-persistence.md) | [TA0008](../_cloud-base/TA0008-lateral-movement.md) · [TA0003](../_cloud-base/TA0003-persistence.md) · [TA0002](../_cloud-base/TA0002-execution.md) |
| Evasion | [05](05-evasion.md) | [TA0005 Stealth](../_cloud-base/TA0005-stealth.md) · [TA0112 Defense Impairment](../_cloud-base/TA0112-defense-impairment.md) |
| Collection, exfil & impact | [06](06-collection-exfil-impact.md) | [TA0009](../_cloud-base/TA0009-collection.md) · [TA0010](../_cloud-base/TA0010-exfiltration.md) · [TA0040](../_cloud-base/TA0040-impact.md) |

## Adjacent scope
- **Apps on AWS** (web/API on EC2/ECS/Lambda/API Gateway) → test against the
  [ASVS base](../_asvs-base/README.md).
- **The control plane itself** is this methodology.

## References
- [Cloud attack base](../_cloud-base/README.md) · [ATT&CK Cloud](https://attack.mitre.org/matrices/enterprise/cloud/)
- [AWS pentest rules](https://aws.amazon.com/security/penetration-testing/)
- [HackTricks Cloud – AWS](https://cloud.hacktricks.xyz/) · Upstream [PayloadsAllTheThings](../../upstream/PayloadsAllTheThings/README.md)
