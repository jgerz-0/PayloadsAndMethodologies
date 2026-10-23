# GCP · Phase 1 — Recon & Enumeration

> ATT&CK [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) + external recon,
> projected onto GCP.

## Who am I / what can I do

#### T1087 Account Discovery · T1526 Cloud Service Discovery
```sh
gcloud auth list ; gcloud config list                     # active identity
gcloud projects list                                       # projects you can see
gcloud projects get-iam-policy <proj>                      # bindings (if allowed)
gcloud asset search-all-iam-policies --scope=projects/<p>  # IAM across resources
# test effective perms:
gcloud iam list-testable-permissions //cloudresourcemanager.googleapis.com/projects/<p>
```
- **Positive (secure):** scoped member; `getIamPolicy` denied.
- **Negative (vulnerable):** full project IAM policy returned → map impersonation
  chains offline (`roles/editor` or `actAs` bindings jump out).

#### Resource/service enumeration
```sh
gcloud services list --enabled
gcloud compute instances list ; gcloud storage buckets list
gcloud iam service-accounts list                           # the real targets
```

## Public / unauthenticated attack surface

#### T1580 Cloud Infrastructure Discovery — external
- **GCS buckets:** `gsutil ls gs://<bucket>` / GCPBucketBrute (also finds buckets
  whose IAM lets *allUsers*/*allAuthenticatedUsers* read or **write**).
  - Negative: anonymous list/read → public bucket. Prowler
    `cloudstorage_bucket_public_access`; missing uniform access
    `cloudstorage_bucket_uniform_bucket_level_access`.
- **Public compute / Cloud SQL / Cloud Functions / BigQuery:**
  ```sh
  gcloud compute instances list --format="value(name,EXTERNAL_IP)"
  ```
  - Negative: public IP / `allUsers` invoker / public dataset. Prowler
    `compute_instance_public_ip`, `cloudsql_instance_public_access`,
    `cloudfunction_function_not_publicly_accessible`, `bigquery_dataset_public_access`.
- **Firewall exposure:** `0.0.0.0/0` to 22/3389. Prowler
  `compute_firewall_ssh_access_from_the_internet_allowed`,
  `compute_firewall_rdp_access_from_the_internet_allowed`.

## Enumerate service accounts & keys (set up privesc)
```sh
gcloud iam service-accounts list
gcloud iam service-accounts keys list --iam-account <sa-email>
```
User-managed SA keys are long-lived liabilities. Prowler `iam_sa_no_user_managed_keys`,
`iam_sa_user_managed_key_rotate_90_days`.

---
*Base: [TA0007 Discovery](../_cloud-base/TA0007-discovery.md). Next:
[Phase 2 — Access & Credentials](02-access-and-credentials.md).*
