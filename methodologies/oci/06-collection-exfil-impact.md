# OCI · Phase 6 — Collection, Exfiltration & Impact

> ATT&CK [TA0009 Collection](../_cloud-base/TA0009-collection.md) +
> [TA0010 Exfiltration](../_cloud-base/TA0010-exfiltration.md) +
> [TA0040 Impact](../_cloud-base/TA0040-impact.md), projected onto OCI. **Impact
> is destructive — demonstrate non-destructively unless scoped.**

## Collection
#### T1530 Data from Cloud Storage
- **Service/sink:** Object Storage, Autonomous/DB, Block Volumes.
  ```sh
  oci os object bulk-download -bn <bucket> -ns <ns> --download-dir ./loot
  ```
- **Positive (secure):** `NotAuthorizedOrNotFound`; bucket private + CMK-encrypted
  (`objectstorage_bucket_not_publicly_accessible`, `objectstorage_bucket_encrypted_with_cmk`).
- **Negative (vulnerable):** objects downloaded → data collected (public bucket
  or over-broad policy).

## Exfiltration
#### T1537 Transfer Data to Cloud Account
- **Service/sink:** create a **pre-authenticated request (PAR)** giving external
  read, or copy a bucket/volume to another tenancy:
  ```sh
  oci os preauth-request create -bn <bucket> -ns <ns> --access-type ObjectRead \
    --name x --time-expires 2030-01-01T00:00:00Z
  ```
- **Positive (secure):** PAR creation restricted; retention/versioning on.
  **Negative:** a long-lived PAR URL grants anonymous external read → exfil.

## Impact
#### T1486 Data Encrypted for Impact · T1485 Data Destruction
- **Service/sink:** OCI Vault/KMS keys, buckets/volumes. Disable/schedule-delete a
  master key to deny access; delete buckets/backups.
  ```sh
  oci kms management key schedule-deletion --key-id <ocid> --time-of-deletion ...
  ```
- **Positive (secure):** `NotAuthorizedOrNotFound`; versioning + retention rules;
  key-deletion restricted. **Negative:** key deletable / backups removable → data
  loss. **Confirm via permission check, don't execute in prod.**

#### T1496 Resource Hijacking
Launch compute at scale (cryptomining) where limits allow — impact = cost. Detect
via budgets/Cloud Guard.

---
*Base: [Collection](../_cloud-base/TA0009-collection.md) ·
[Exfiltration](../_cloud-base/TA0010-exfiltration.md) ·
[Impact](../_cloud-base/TA0040-impact.md). Back to [OCI README](README.md).*
