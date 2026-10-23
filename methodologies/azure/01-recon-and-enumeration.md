# Azure · Phase 1 — Recon & Enumeration

> ATT&CK [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) + external recon,
> projected onto Azure + Entra ID. Enumerate **both** planes (resource RBAC and
> directory).

## Who am I / what can I do

#### T1087 Account Discovery · T1526 Cloud Service Discovery
```sh
az account show                                   # current subscription/tenant
az ad signed-in-user show                         # Entra identity
az role assignment list --all --assignee <id>     # Azure RBAC roles
az account management-group list                  # mgmt-group hierarchy
roadrecon gather && roadrecon gui                  # full Entra dump (users, apps, roles)
```
- **Positive (secure):** scoped principal; directory reads restricted
  (`Restrict access to Entra admin portal` / guest restrictions).
- **Negative (vulnerable):** any member can read the whole directory (default
  allows broad user/app/role enumeration) → map attack paths with AzureHound.

#### Resource enumeration (both planes)
```sh
az resource list -o table ; az vm list -o table
az ad app list --all ; az ad sp list --all        # app registrations / service principals
az role assignment list --all                      # who has Owner/UAA
```

## Public / unauthenticated attack surface

#### T1580 Cloud Infrastructure Discovery — external
- **Tenant/user recon (unauth):** federation + user existence via the login
  endpoints (MicroBurst `Invoke-UserEnumerationAzure`, o365creeper); informs
  password spraying ([Phase 2](02-access-and-credentials.md)).
- **Public blob storage:** container/blob brute (MicroBurst
  `Invoke-EnumerateAzureBlobs`); `az storage blob list --account-name <a> -c <c> --auth-mode login`.
  - Negative: anonymous blob/container access → public data. Prowler
    `storage_blob_public_access_level_is_disabled`,
    `storage_account_public_network_access_disabled`.
- **Public endpoints:** App Service, Functions, SQL, Cosmos with public network
  access. Prowler `storage_account_public_network_access_disabled`,
  network exposure checks.
- **NSG exposure:** `0.0.0.0/0` to 22/3389. Prowler
  `network_ssh_internet_access_restricted`, `network_rdp_internet_access_restricted`.

## Enumerate service principals & secrets (set up privesc)
```sh
az ad app credential list --id <appId>             # client secrets/certs
az ad sp list --all --query "[].{name:displayName,appId:appId}"
```
Over-privileged service principals and app secrets with long lifetimes are prime
privesc/persistence targets.

---
*Base: [TA0007 Discovery](../_cloud-base/TA0007-discovery.md). Next:
[Phase 2 — Access & Credentials](02-access-and-credentials.md).*
