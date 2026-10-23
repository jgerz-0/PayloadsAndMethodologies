# M365 · Phase 6 — Collection, Exfiltration & Impact

> ATT&CK [TA0009 Collection](../_cloud-base/TA0009-collection.md) +
> [TA0010 Exfiltration](../_cloud-base/TA0010-exfiltration.md) +
> [TA0040 Impact](../_cloud-base/TA0040-impact.md), projected onto M365.
> **Impact is destructive — demonstrate non-destructively unless scoped.**

## Collection
#### T1114 Email Collection · T1213 Data from Information Repositories
- **Service/sink:** Exchange mailboxes, SharePoint/OneDrive, Teams.
  ```powershell
  Get-MgUserMessage -UserId victim@target.com -All           # mail (with grant)
  # SharePoint/OneDrive files via Graph Files.Read.All; Teams chat via Chat.Read.All
  Search-UnifiedAuditLog / eDiscovery content search          # bulk collection
  ```
- **Positive (secure):** scoped delegated perms; external sharing restricted;
  DLP policies. **Negative:** app-wide read grant collects the tenant's mail/files.

## Exfiltration
#### T1537 Transfer to Cloud Account · T1048 Exfil over alt protocol
- Auto-forwarding rules to external ([Phase 4](04-lateral-movement-and-persistence.md));
  external SharePoint sharing links; eDiscovery export.
  ```powershell
  Get-SPOTenant | fl SharingCapability                        # ExternalUserAndGuestSharing = open
  ```
- **Positive (secure):** external forwarding disabled; sharing restricted
  (`sharepoint_external_sharing_restricted`, `drive`-style sharing checks).
- **Negative (vulnerable):** external forward / anonymous sharing link → data
  leaves the tenant.

## Impact
#### T1486 Data Encrypted for Impact · T1485/T1490
- **Service/sink:** ransomware via OneDrive/SharePoint file encryption; mailbox
  deletion; disabling recovery (retention/versioning).
- **Positive (secure):** SharePoint/OneDrive versioning + retention + recycle bin;
  litigation hold. **Negative:** versioning/retention disablable + mass file
  encryption → data loss. **Confirm via config/permission, don't execute.**

#### T1531 Account Access Removal
Resetting passwords / revoking sessions to lock out legitimate admins. Detect via
sign-in and audit logs.

---
*Base: [Collection](../_cloud-base/TA0009-collection.md) ·
[Exfiltration](../_cloud-base/TA0010-exfiltration.md) ·
[Impact](../_cloud-base/TA0040-impact.md). Back to [M365 README](README.md).*
