# Google Workspace · Phase 6 — Collection, Exfiltration & Impact

> ATT&CK [TA0009 Collection](../_cloud-base/TA0009-collection.md) +
> [TA0010 Exfiltration](../_cloud-base/TA0010-exfiltration.md) +
> [TA0040 Impact](../_cloud-base/TA0040-impact.md), projected onto Workspace.
> **Impact is destructive — demonstrate non-destructively unless scoped.**

## Collection
#### T1114 Email Collection · T1213 Data from Information Repositories
- **Service/sink:** Gmail, Drive, Google Vault.
  ```sh
  gam user victim@target.com show messages
  gam user victim@target.com show filelist              # Drive inventory
  # Vault export (eDiscovery) collects across the org with admin rights
  ```
- **Positive (secure):** scoped delegation; DLP rules; external sharing limited.
- **Negative (vulnerable):** DWD / Vault / broad OAuth grant collects the org's
  mail and Drive.

## Exfiltration
#### T1537 Transfer to Cloud Account · T1567 Exfil over Web Service
- Gmail auto-forward to external ([Phase 4](04-lateral-movement-and-persistence.md));
  Drive "anyone with the link" sharing; **Google Takeout**; copy to an
  attacker-owned Drive/account.
  ```sh
  gam user victim@target.com add drivefileacl <fileId> anyone role reader
  ```
- **Positive (secure):** external sharing restricted to allowlisted domains
  (`drive_sharing_allowlisted_domains`), forwarding disabled, Takeout disabled for
  the OU. **Negative:** anonymous link / external forward / Takeout → data leaves.

## Impact
#### T1485 Data Destruction · T1486 · T1531 Account Access Removal
- Mass-delete Drive files / empty trash; encrypt documents; reset passwords and
  revoke sessions to lock out admins; suspend accounts.
- **Positive (secure):** Vault retention holds + Drive restore + admin recovery
  paths. **Negative:** retention disablable + mass deletion → data loss. **Confirm
  via config/permission, don't execute in prod.**

---
*Base: [Collection](../_cloud-base/TA0009-collection.md) ·
[Exfiltration](../_cloud-base/TA0010-exfiltration.md) ·
[Impact](../_cloud-base/TA0040-impact.md). Back to [Workspace README](README.md).*
