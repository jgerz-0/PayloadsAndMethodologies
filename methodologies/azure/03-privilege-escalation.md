# Azure · Phase 3 — Privilege Escalation

> ATT&CK [TA0004 Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md),
> projected onto Azure RBAC **and** Entra ID. Watch for escalation that crosses
> the two planes.

#### T1548 Abuse Elevation Control / T1098 Account Manipulation — Azure RBAC paths
- **Service/sink:** ARM role assignments.

| Role / permission you hold | Escalation |
|---|---|
| **User Access Administrator** (`Microsoft.Authorization/roleAssignments/write`) | grant yourself **Owner** on any scope |
| **Contributor** | can't grant roles, but can run code on VMs → managed-identity token (next phase) |
| `Microsoft.Compute/.../runCommand` | run SYSTEM/root commands on a VM |
| custom role with `*/write` on `Microsoft.Authorization` | self-assign roles |

```sh
az role assignment create --assignee <me> --role Owner --scope /subscriptions/<sub>
```
- **Positive (secure):** `AuthorizationFailed`; no UAA/Owner; locks on role
  assignment. Prowler `iam_subscription_roles_owner_custom_not_created`,
  `iam_role_user_access_admin_restricted`.
- **Negative (vulnerable):** role assignment succeeds → Owner.

#### T1098 — Entra ID directory escalation
- **Service/sink:** Microsoft Graph, Entra roles, app registrations.

| Hold | Escalation |
|---|---|
| **Application Administrator** / `Application.ReadWrite.All` | add a secret to a privileged service principal, log in as it |
| owner of an app/SP with high Graph perms (`RoleManagement.ReadWrite.Directory`) | grant self Global Admin |
| **Privileged Role Administrator** | assign any Entra role |
| dynamic-group abuse / self-service group ownership | join a group that confers access |

```sh
az ad app credential reset --id <appId>           # mint a secret for a priv SP
```
- **Positive (secure):** least-privilege Graph app permissions; no standing
  Application Admin; PIM (just-in-time) for privileged roles.
- **Negative (vulnerable):** you add a credential to a high-privilege SP or grant
  a directory role → tenant-level control. **Entra→Azure pivot:** a Global Admin
  can toggle "Access management for Azure resources" to gain UAA on the root
  mgmt group, then Owner everywhere.

---
*Base: [Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md).
Next: [Phase 4 — Lateral Movement & Persistence](04-lateral-movement-and-persistence.md).*
