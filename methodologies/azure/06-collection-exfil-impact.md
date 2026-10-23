# Azure · Phase 6 — Collection, Exfiltration & Impact

> ATT&CK [TA0009 Collection](../_cloud-base/TA0009-collection.md) +
> [TA0010 Exfiltration](../_cloud-base/TA0010-exfiltration.md) +
> [TA0040 Impact](../_cloud-base/TA0040-impact.md), projected onto Azure.
> **Impact is destructive — demonstrate non-destructively unless scoped.**

## Collection

#### T1530 Data from Cloud Storage
- **Service/sink:** Blob storage, Azure SQL, Cosmos DB, Key Vault.
  ```sh
  az storage blob download-batch -d ./loot -s <container> --account-name <a> --auth-mode login
  az sql db list -g <rg> -s <server>
  ```
- **Positive (secure):** `AuthorizationFailed`/`Forbidden`; storage private
  endpoint + key access disabled (`storage_account_key_access_disabled`,
  `storage_account_public_network_access_disabled`).
- **Negative (vulnerable):** blobs/rows downloaded → data collected. Public blob
  access (`storage_blob_public_access_level_is_disabled`) is the finding.

## Exfiltration

#### T1537 Transfer Data to Cloud Account
- **Service/sink:** copy a blob/disk/snapshot to an attacker-controlled storage
  account/tenant; generate a long-lived SAS token for external access:
  ```sh
  az storage container generate-sas --account-name <a> -n <c> --permissions rl \
    --expiry 2030-01-01 -o tsv                       # shareable read link
  ```
- **Positive (secure):** SAS disabled / short-lived; storage firewall restricts
  networks. **Negative:** a long-lived SAS or cross-tenant copy succeeds → data
  readable externally.

## Impact

#### T1486 Data Encrypted for Impact · T1485 Data Destruction
- **Service/sink:** Key Vault keys (CMK), storage/disks. Delete/disable a CMK to
  deny access to everything it encrypts; delete resources.
  ```sh
  az keyvault key delete --vault-name <v> --name <k>     # if no purge protection
  ```
- **Positive (secure):** Key Vault **soft-delete + purge protection** on; resource
  locks; immutable blob storage. Prowler `keyvault_*` (expiry/rotation),
  purge-protection checks.
- **Negative (vulnerable):** key deletable without purge protection / resources
  deletable → data loss. **Confirm via permission check, don't execute in prod.**

#### T1496 Resource Hijacking · T1578 Modify Cloud Compute
Deploy VMs/VMSS at scale (cryptomining) with Contributor; modify compute infra.
Impact = cost/availability. Detect via cost alerts / Defender.

---
*Base: [Collection](../_cloud-base/TA0009-collection.md) ·
[Exfiltration](../_cloud-base/TA0010-exfiltration.md) ·
[Impact](../_cloud-base/TA0040-impact.md). Back to [Azure README](README.md).*
