# Google Workspace · Phase 3 — Privilege Escalation

> ATT&CK [TA0004 Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md),
> projected onto Google Workspace. Escalation = **gaining a super-admin / admin
> role** or **abusing Domain-Wide Delegation**.

#### T1098 Account Manipulation — admin-role & DWD escalation

| Hold | Escalation |
|---|---|
| a delegated admin role with **User Management** | reset a super admin's password / create admin |
| **Services** admin privilege (API controls) | register/approve a **DWD** client to impersonate all users |
| ability to create an **Apps Script** / OAuth app + consent | broad Gmail/Drive access |
| GCP project access where a **DWD SA** lives | mint user-impersonation tokens (see [Phase 2](02-access-and-credentials.md)) |

- **How to test (DWD setup, admin):** register a GCP SA's client ID in Admin
  console → API controls → Domain-wide delegation with scope
  `https://mail.google.com/`, then impersonate any user.
- **Positive (secure):** super admins minimal + hardware 2SV
  (`directory_super_admin_count`, `directory_super_admin_only_admin_roles`); DWD
  not granted or tightly scoped; Marketplace admin-approval only.
- **Negative (vulnerable):** you obtain a super-admin role or stand up a DWD
  client → tenant-wide impersonation and control.

#### Workspace → GCP and back
A super admin can manage the org's GCP resources (org-level IAM); a GCP org admin
can affect Workspace-linked projects. Test both planes together with
[GCP](../gcp/03-privilege-escalation.md).

---
*Base: [Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md).
Next: [Phase 4 — Lateral Movement & Persistence](04-lateral-movement-and-persistence.md).*
