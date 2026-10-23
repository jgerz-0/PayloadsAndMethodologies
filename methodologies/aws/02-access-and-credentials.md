# AWS · Phase 2 — Access & Credentials

> ATT&CK [TA0001 Initial Access](../_cloud-base/TA0001-initial-access.md) +
> [TA0006 Credential Access](../_cloud-base/TA0006-credential-access.md).
> Projected onto AWS: how a foothold is obtained and how more credentials are
> harvested once inside.

## Initial access

#### T1078.004 Valid Accounts: Cloud Accounts
- **Service/sink:** leaked `AKIA…`/`ASIA…` keys (GitHub, CI logs, mobile apps,
  `.env`, S3), or console creds + no MFA.
- **How to test:** `trufflehog`/`gitleaks` on repos/artifacts; validate a found
  key with `aws sts get-caller-identity`.
- **Positive (secure):** key invalid/disabled; console requires MFA
  (`iam_user_mfa_enabled_console_access`), keys rotated
  (`iam_rotate_access_key_90_days`).
- **Negative (vulnerable):** key authenticates → foothold. Root/admin key with
  no MFA is critical (`iam_root_hardware_mfa_enabled`).

#### T1190 Exploit Public-Facing Application → SSRF to cloud
- **Service/sink:** a web app on EC2 with an instance profile. SSRF is the
  bridge to IMDS (below).

## Credential access

#### T1552.005 Unsecured Credentials: Cloud Instance Metadata API  ⭐
- **Service/sink:** EC2 IMDS at `169.254.169.254`, reachable via SSRF or on-box.
- **How to test:**
  ```sh
  # IMDSv1 (no token) — the finding:
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>
  # IMDSv2 (requires PUT token first — SSRF usually can't set headers):
  TOKEN=$(curl -X PUT "…/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
  ```
- **Positive (secure):** IMDSv2 enforced (`HttpTokens=required`) → tokenless/SSRF
  request returns `401`. Prowler `ec2_instance_imdsv2_enabled`.
- **Negative (vulnerable):** IMDSv1 returns `AccessKeyId`/`SecretAccessKey`/
  `Token` JSON → export and assume the instance role. Upstream
  [SSRF](../../upstream/PayloadsAllTheThings/Server%20Side%20Request%20Forgery/README.md).

#### T1552.001 Credentials in Files · T1552 Unsecured Credentials
- **Service/sink:** EC2 **user data**, SSM Parameter Store, env vars, AMIs.
  ```sh
  aws ec2 describe-instance-attribute --attribute userData --instance-id <id>  # often has secrets
  aws ssm get-parameters-by-path --path / --recursive --with-decryption
  aws ssm describe-parameters
  ```
- **Negative:** plaintext DB creds/keys in user data or a `String` (not
  `SecureString`) SSM param. Prowler `ssm_document_secrets`,
  `ec2_instance_secrets_user_data`.

#### T1555.006 Credentials from Password Stores: Cloud Secrets Management Stores
- **Service/sink:** Secrets Manager, KMS.
  ```sh
  aws secretsmanager list-secrets ; aws secretsmanager get-secret-value --secret-id <id>
  ```
- **Positive (secure):** `AccessDenied` (scoped resource policy —
  `secretsmanager_not_publicly_accessible`, restrictive policy).
- **Negative (vulnerable):** secret value returned → downstream creds. A
  resource policy allowing `*` is critical.

#### T1528 Steal Application Access Token / T1606.002 Forge SAML Tokens
- STS session tokens, OIDC/SAML federation; forged SAML (Golden SAML) if the
  signing key/ADFS is compromised. Relevant with Identity Center / federation.

---
*Base: [Initial Access](../_cloud-base/TA0001-initial-access.md) ·
[Credential Access](../_cloud-base/TA0006-credential-access.md). Next:
[Phase 3 — Privilege Escalation](03-privilege-escalation.md).*
