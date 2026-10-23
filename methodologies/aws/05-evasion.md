# AWS · Phase 5 — Evasion

> ATT&CK [TA0005 Stealth](../_cloud-base/TA0005-stealth.md) +
> [TA0112 Defense Impairment](../_cloud-base/TA0112-defense-impairment.md)
> (v20 split of the former Defense Evasion). Projected onto AWS: blinding and
> evading detection. **In an authorized test, confirm these non-destructively
> where possible** (check config, don't actually disable prod logging).

#### T1562.008 Impair Defenses: Disable or Modify Cloud Logs
- **Service/sink:** CloudTrail.
  ```sh
  aws cloudtrail stop-logging --name <trail>
  aws cloudtrail delete-trail --name <trail>
  aws cloudtrail update-trail --name <trail> --no-include-global-service-events
  ```
- **Positive (secure):** `AccessDenied`; a multi-region, log-file-validated trail
  you cannot stop; org trail. Prowler `cloudtrail_multi_region_enabled`,
  `cloudtrail_log_file_validation_enabled`, `cloudtrail_logs_s3_bucket_is_not_publicly_accessible`.
- **Negative (vulnerable):** logging stops / trail deleted → actions go
  unrecorded. (Confirm by reading trail status, not by stopping it in prod.)

#### T1562.001 Impair Defenses: Disable Security Tools
- **Service/sink:** GuardDuty, Security Hub, Config, Macie.
  ```sh
  aws guardduty list-detectors
  aws guardduty delete-detector --detector-id <id>     # or update to suspend
  aws configservice stop-configuration-recorder --configuration-recorder-name <n>
  ```
- **Positive (secure):** `AccessDenied`; GuardDuty enabled all regions, org-managed.
  Prowler `guardduty_is_enabled`, `config_recorder_all_regions_enabled`,
  `securityhub_enabled`.
- **Negative (vulnerable):** detector deletable/suspended → threat detection off.

#### T1070 Indicator Removal
- Delete CloudWatch log groups, S3 access logs, flow logs:
  `aws logs delete-log-group`, remove VPC flow logs. Prowler
  `vpc_flow_logs_enabled`, `cloudwatch_log_group_retention_policy_specific_days_enabled`.

#### T1535 Unused/Unsupported Cloud Regions
Operate in a region with no CloudTrail/GuardDuty coverage to avoid logging —
confirm detection parity across **all** regions (ties to multi-region trail).

---
*Base: [Stealth](../_cloud-base/TA0005-stealth.md) ·
[Defense Impairment](../_cloud-base/TA0112-defense-impairment.md). Next:
[Phase 6 — Collection, Exfil & Impact](06-collection-exfil-impact.md).*
