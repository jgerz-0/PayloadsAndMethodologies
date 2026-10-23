# M365 · Phase 3 — Privilege Escalation

> ATT&CK [TA0004 Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md),
> projected onto M365 / Entra. Escalation is via **directory roles**, **app/SP
> Graph permissions**, or **service-admin roles** (Exchange/SharePoint).

#### T1098 Account Manipulation — Entra directory escalation

| Hold | Escalation |
|---|---|
| **Application Administrator** / `Application.ReadWrite.All` | add a secret to a privileged SP, sign in as it |
| app/SP with `RoleManagement.ReadWrite.Directory` | grant self/any principal **Global Admin** |
| **Privileged Authentication Administrator** | reset a Global Admin's creds/MFA |
| owner of a privileged app or group | inherit its access |
| **Privileged Role Administrator** | assign any Entra role |

```powershell
# add a credential to a high-privilege service principal:
Add-MgServicePrincipalPassword -ServicePrincipalId <id>
# or escalate a role (with RoleManagement.ReadWrite.Directory):
New-MgRoleManagementDirectoryRoleAssignment -PrincipalId <me> -RoleDefinitionId <GA> -DirectoryScopeId "/"
```
- **Positive (secure):** least-privilege Graph app perms
  (`entra_app_registration_no_unused_privileged_permissions`); PIM (JIT) for
  roles; no standing App Admin; phishing-resistant MFA for admins.
- **Negative (vulnerable):** adding an SP credential or a role assignment succeeds
  → tenant control. **M365→Azure pivot:** a Global Admin can seize Azure RBAC
  (root mgmt group) — see [Azure Phase 3](../azure/03-privilege-escalation.md).

#### Service-admin escalation
- **Exchange:** an org-management/RBAC role lets you grant mailbox access or add
  transport rules (→ [Phase 4](04-lateral-movement-and-persistence.md)).
- **SharePoint admin:** site-collection admin over any site → all documents.

---
*Base: [Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md).
Next: [Phase 4 — Lateral Movement & Persistence](04-lateral-movement-and-persistence.md).*
