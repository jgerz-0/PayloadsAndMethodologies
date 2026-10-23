# OCI · Phase 5 — Evasion

> ATT&CK [TA0005 Stealth](../_cloud-base/TA0005-stealth.md) +
> [TA0112 Defense Impairment](../_cloud-base/TA0112-defense-impairment.md),
> projected onto OCI. **Confirm non-destructively where possible.**

#### T1562.008 Disable or Modify Cloud Logs
- **Service/sink:** OCI Audit, Logging, Service Connector Hub.
  ```sh
  oci logging log-group list -c <c> ; oci logging log list --log-group-id <id>
  # disabling a log / deleting a log group removes telemetry
  ```
- **Positive (secure):** tenancy Audit retention maximized, logs exported to a
  locked bucket/SIEM, alarms on config changes. Prowler
  `objectstorage_bucket_logging_enabled`, audit/logging checks.
- **Negative (vulnerable):** log/log-group deletable → telemetry gaps. (Confirm
  by reading config, not deleting in prod.)

#### T1562.001 Disable Security Tools
- **Service/sink:** Cloud Guard, Vulnerability Scanning.
  ```sh
  oci cloud-guard configuration get --compartment-id <tenancy>
  ```
- **Positive (secure):** Cloud Guard enabled tenancy-wide. **Negative:** Cloud
  Guard disablable → posture monitoring off.

#### T1535 Unused Regions
Subscribe/operate in a region lacking Cloud Guard/Audit coverage — confirm
parity across subscribed regions.

---
*Base: [Stealth](../_cloud-base/TA0005-stealth.md) ·
[Defense Impairment](../_cloud-base/TA0112-defense-impairment.md). Next:
[Phase 6 — Collection, Exfil & Impact](06-collection-exfil-impact.md).*
