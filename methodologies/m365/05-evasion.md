# M365 · Phase 5 — Evasion

> ATT&CK [TA0005 Stealth](../_cloud-base/TA0005-stealth.md) +
> [TA0112 Defense Impairment](../_cloud-base/TA0112-defense-impairment.md),
> projected onto M365. **Confirm non-destructively where possible.**

#### T1562.008 Disable or Modify Cloud Logs
- **Service/sink:** Unified Audit Log (Purview), mailbox auditing.
  ```powershell
  Get-AdminAuditLogConfig ; Get-Mailbox victim | fl AuditEnabled
  Set-Mailbox victim -AuditEnabled $false          # disable per-mailbox audit
  ```
- **Positive (secure):** Unified Audit Log on tenant-wide; mailbox auditing on by
  default; alerts on audit-config change. Prowler `purview_audit_log_search_enabled`-style checks.
- **Negative (vulnerable):** audit log / mailbox audit disablable → actions
  unlogged. (Read config to confirm, don't disable in prod.)

#### T1564.008 Email Hiding Rules
Inbox rules that delete/move security notifications (e.g. move "login alert" to
RSS/Deleted) to hide account compromise. Check `Get-InboxRule` for suspicious
move/delete rules.

#### T1562.001 Disable Security Tools
Weakening anti-phishing/anti-spam (Defender for Office) policies, Safe Links/Safe
Attachments, or Conditional Access. Prowler `defender_*` and
`entra_conditional_access_*` checks flag weakened policy.

#### T1550 Use Alternate Authentication Material
Pass-the-PRT / token replay to avoid re-auth and MFA prompts (TokenTactics,
AADInternals) — detection evasion via valid tokens.

---
*Base: [Stealth](../_cloud-base/TA0005-stealth.md) ·
[Defense Impairment](../_cloud-base/TA0112-defense-impairment.md). Next:
[Phase 6 — Collection, Exfil & Impact](06-collection-exfil-impact.md).*
