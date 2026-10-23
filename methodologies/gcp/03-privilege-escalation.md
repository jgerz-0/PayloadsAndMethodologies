# GCP · Phase 3 — Privilege Escalation

> ATT&CK [TA0004 Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md),
> projected onto GCP IAM. GCP privesc is overwhelmingly **service-account
> impersonation** or **IAM-policy editing**.

#### T1548 Abuse Elevation Control / T1098 Account Manipulation — GCP privesc paths
- **Service/sink:** IAM, and services that run **as** an SA (Cloud Functions,
  Compute, Cloud Run, Cloud Build, Deployment Manager).
- **How to test:** enumerate your permissions, match to a known path
  ([Rhino's 30+ GCP privesc methods](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/)):

| Permission you hold | Escalation |
|---|---|
| `iam.serviceAccounts.getAccessToken` | mint a token for a more privileged SA |
| `iam.serviceAccounts.actAs` + `cloudfunctions.functions.create` | deploy a function running as a privileged SA |
| `iam.serviceAccounts.actAs` + `compute.instances.create` | create a VM with a privileged SA, read its token via metadata |
| `iam.serviceAccounts.implicitDelegation` | chain impersonation to a target SA |
| `iam.serviceAccountKeys.create` | mint a key for a privileged SA |
| `*.setIamPolicy` (resourcemanager/projects) | bind `roles/owner` to self |
| `iam.roles.update` (on a role you're granted) | add permissions to your own custom role |
| `cloudbuild.builds.create` | Cloud Build runs as the powerful default Cloud Build SA |
| `deploymentmanager.deployments.create` | DM runs as the Google APIs SA (Editor) |

- **How to test (impersonation):**
  ```sh
  gcloud <anything> --impersonate-service-account=<priv-sa-email>
  gcloud iam service-accounts get-access-token <priv-sa-email>
  # mint a standing key:
  gcloud iam service-accounts keys create k.json --iam-account <priv-sa-email>
  ```
- **Positive (secure):** `PERMISSION_DENIED`; no `actAs`/`getAccessToken`/
  `setIamPolicy`; default SAs not Editor; key creation disabled
  (`iam_sa_no_user_managed_keys`, `compute_instance_default_service_account_in_use_with_full_api_access`).
- **Negative (vulnerable):** impersonation/key-create/policy-bind succeeds and a
  re-check shows elevated access → you now control the target SA / project.

---
*Base: [Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md).
Next: [Phase 4 — Lateral Movement & Persistence](04-lateral-movement-and-persistence.md).*
