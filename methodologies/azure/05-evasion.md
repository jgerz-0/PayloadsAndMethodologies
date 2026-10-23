# Azure · Phase 5 — Evasion

> ATT&CK [TA0005 Stealth](../_cloud-base/TA0005-stealth.md) +
> [TA0112 Defense Impairment](../_cloud-base/TA0112-defense-impairment.md),
> projected onto Azure. **Confirm non-destructively where possible.**

#### T1562.008 Disable or Modify Cloud Logs
- **Service/sink:** Azure Monitor diagnostic settings, Activity Log.
  ```sh
  az monitor diagnostic-settings list --resource <id>
  az monitor diagnostic-settings delete --name <n> --resource <id>   # stop log export
  ```
- **Positive (secure):** activity logs exported to an immutable/locked store,
  alerts on changes. Prowler `monitor_storage_account_with_activity_logs_is_private`,
  `monitor_diagnostic_setting_with_appropriate_categories`, and the
  `monitor_alert_create_*` policy-change alert checks.
- **Negative (vulnerable):** diagnostic setting deletable → telemetry stops.
  (Read the setting to confirm, don't delete in prod.)

#### T1562.001 Disable Security Tools
- **Service/sink:** Microsoft Defender for Cloud, Conditional Access.
  ```sh
  az security pricing list -o table                  # Defender plans per resource type
  ```
- **Positive (secure):** Defender for Servers/SQL/Storage on; CA policies
  enforced. Prowler `defender_ensure_defender_for_server_is_on`,
  `defender_ensure_defender_for_sql_servers_is_on`,
  `defender_additional_email_configured_with_a_security_contact`.
- **Negative (vulnerable):** Defender plan downgradable to Free, or a CA policy
  disablable → detection/enforcement off.

#### T1070 Indicator Removal
Delete Log Analytics workspaces / NSG flow logs; clear sign-in logs retention.
Prowler NSG flow-log and log-retention checks.

#### T1535 Unused Cloud Regions
Operate in a region/subscription without Defender/diagnostics coverage — confirm
parity across subscriptions.

---
*Base: [Stealth](../_cloud-base/TA0005-stealth.md) ·
[Defense Impairment](../_cloud-base/TA0112-defense-impairment.md). Next:
[Phase 6 — Collection, Exfil & Impact](06-collection-exfil-impact.md).*
