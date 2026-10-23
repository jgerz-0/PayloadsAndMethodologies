# GCP · Phase 2 — Access & Credentials

> ATT&CK [TA0001 Initial Access](../_cloud-base/TA0001-initial-access.md) +
> [TA0006 Credential Access](../_cloud-base/TA0006-credential-access.md),
> projected onto GCP.

## Initial access

#### T1078.004 Valid Accounts: Cloud Accounts
- **Service/sink:** leaked SA key JSON (repos, CI, GCS, images), or user creds.
  ```sh
  gcloud auth activate-service-account --key-file key.json
  gcloud auth list                                   # confirm identity
  ```
- **Positive (secure):** key disabled; user-managed SA keys disallowed
  (`iam_sa_no_user_managed_keys`). **Negative:** key authenticates → foothold as
  that SA.

## Credential access

#### T1552.005 Cloud Instance Metadata API  ⭐
- **Service/sink:** the metadata server on Compute Engine / GKE nodes.
  ```sh
  curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
  curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes
  ```
- **Positive (secure):** the instance runs a **non-default** SA with minimal
  scopes; metadata concealment / Workload Identity on GKE. Prowler
  `compute_instance_default_service_account_in_use_with_full_api_access`.
- **Negative (vulnerable):** returns an OAuth token for the **default compute SA
  with `cloud-platform` scope + Editor** → broad project control. The classic
  GCP SSRF→token→takeover. Upstream
  [SSRF](../../upstream/PayloadsAllTheThings/Server%20Side%20Request%20Forgery/README.md).

#### T1552.001 Credentials in Files · T1555.006 Cloud Secrets Stores
- **Service/sink:** instance/project **metadata** (startup scripts), Secret
  Manager, source repos.
  ```sh
  gcloud compute instances describe <vm> --format="value(metadata)"   # startup-script secrets
  gcloud secrets list ; gcloud secrets versions access latest --secret=<name>
  ```
- **Positive (secure):** `PERMISSION_DENIED`; secret not public
  (`secretmanager_secret_not_publicly_accessible`).
- **Negative (vulnerable):** plaintext creds in startup-script metadata, or
  secret value returned → downstream access.

#### T1528 Steal Application Access Token
OAuth tokens via `gcloud auth print-access-token`; abuse of over-scoped OAuth
grants in Workspace. Impersonation tokens (next phase) are the main lever.

---
*Base: [Initial Access](../_cloud-base/TA0001-initial-access.md) ·
[Credential Access](../_cloud-base/TA0006-credential-access.md). Next:
[Phase 3 — Privilege Escalation](03-privilege-escalation.md).*
