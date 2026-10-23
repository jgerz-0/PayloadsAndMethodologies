# M365 · Phase 1 — Recon & Enumeration

> ATT&CK [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) + external recon,
> projected onto Microsoft 365 / Entra ID.

## Unauthenticated tenant recon
#### T1590/T1589 — external
- **Tenant existence / federation:** `https://login.microsoftonline.com/getuserrealm.srf?login=user@target.com`
  (Managed vs Federated), OpenID config at `/.well-known/openid-configuration`,
  `GetCredentialType` for user existence.
- **User enumeration:** o365creeper / MailSniper `Invoke-UserEnumerationAs...`;
  AADInternals `Invoke-AADIntReconAsOutsider` reveals tenant name, domains, MX,
  DKIM, MDI presence.
- **Negative (vulnerable):** valid users distinguishable → spray target list
  ([Phase 2](02-access-and-credentials.md)).

## Authenticated directory enumeration
#### T1087 Account Discovery · T1526 Cloud Service Discovery
```powershell
Connect-MgGraph -Scopes "Directory.Read.All"
Get-MgUser -All ; Get-MgGroup -All
Get-MgDirectoryRole ; Get-MgDirectoryRoleMember -DirectoryRoleId <id>   # who is admin
Get-MgServicePrincipal -All ; Get-MgApplication -All                     # apps / consent
roadrecon gather ; roadrecon gui
```
- **Positive (secure):** directory reads restricted; guest/member enumeration
  limited (`entra_access_review_guest_users_configured`); admin portal access
  restricted (`entra_admin_portals_access_restriction`).
- **Negative (vulnerable):** any member reads the whole directory (default) →
  enumerate Global Admins, high-privilege apps, consent grants with AzureHound.

## Service surface
```powershell
Connect-ExchangeOnline ; Get-OrganizationConfig        # Exchange posture
Get-SPOTenant                                           # SharePoint external sharing
```

---
*Base: [TA0007 Discovery](../_cloud-base/TA0007-discovery.md). Next:
[Phase 2 — Access & Credentials](02-access-and-credentials.md).*
