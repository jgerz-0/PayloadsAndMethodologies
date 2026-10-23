# GCP · Phase 5 — Evasion

> ATT&CK [TA0005 Stealth](../_cloud-base/TA0005-stealth.md) +
> [TA0112 Defense Impairment](../_cloud-base/TA0112-defense-impairment.md),
> projected onto GCP. **Confirm non-destructively where possible** (read config,
> don't disable prod logging).

#### T1562.008 Disable or Modify Cloud Logs
- **Service/sink:** Cloud Audit Logs, Log Sinks.
  ```sh
  gcloud logging sinks list
  gcloud logging sinks delete <sink>            # remove export to SIEM/bucket
  # or edit audit config in the project IAM policy to disable DATA_READ/WRITE logs
  ```
- **Positive (secure):** org-level audit logging enforced, sink destinations
  locked, metric alerts on config changes. Prowler
  `logging_log_metric_filter_and_alert_for_audit_configuration_changes_enabled`,
  `logging_log_metric_filter_and_alert_for_custom_role_changes_enabled`.
- **Negative (vulnerable):** sink deletable / audit logging disablable → actions
  unlogged. (Confirm by reading the audit config, not disabling it in prod.)

#### T1562.001 Disable Security Tools
- **Service/sink:** Security Command Center, org policies.
  Disabling SCC detectors or loosening org policies reduces detection. Prowler
  `iam_cloud_asset_inventory_enabled` (context), SCC-related checks.

#### T1070 Indicator Removal
Delete log buckets / disable VPC flow logs:
```sh
gcloud compute networks subnets update <subnet> --no-enable-flow-logs
```
Prowler `compute_subnet_flow_logs_enabled` (context).

#### T1535 Unused Cloud Regions
Operate in a region/project lacking SCC/audit coverage — confirm detection
parity across the org.

---
*Base: [Stealth](../_cloud-base/TA0005-stealth.md) ·
[Defense Impairment](../_cloud-base/TA0112-defense-impairment.md). Next:
[Phase 6 — Collection, Exfil & Impact](06-collection-exfil-impact.md).*
