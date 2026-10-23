# GCP Cloud Testing Methodology (ATT&CK-aligned)

> Offensive testing methodology for **Google Cloud Platform**, structured against
> the [cloud attack base](../_cloud-base/README.md) (MITRE ATT&CK + Prowler).
> Organized by **kill-chain phase**; ATT&CK techniques projected onto GCP
> services with the concrete API/sink, enumerate→attempt CLI, and **positive
> (secure, `PERMISSION_DENIED`) vs negative (vulnerable, call succeeds)**
> evidence, each tied to the **Prowler check ID**.

> **Authorization.** GCP requires customers follow the
> [acceptable use / support policy](https://support.google.com/cloud/answer/6262505);
> you don't need prior approval to test your own projects but must not disrupt
> shared infra. Assume an **authorized** engagement; prefer read/enumerate.

## GCP identity model (what you're attacking)

| Principal | Credential | Notes |
|---|---|---|
| Google user / group | OAuth (gcloud login) | org/folder/project IAM bindings |
| **Service account (SA)** | SA **key** (JSON) or short-lived token | the core of GCP attacks |
| Compute instance | SA token via **metadata server** | `metadata.google.internal`, T1552.005 |
| Workload Identity (GKE) | federated SA token | |

Authz = **IAM bindings** (`member` → `role`) at org/folder/project/resource
scope. Danger roles: **primitive** `roles/owner`, `roles/editor` (editor is
huge), and anything with `iam.serviceAccounts.actAs` / `getAccessToken` /
`setIamPolicy`. The attacker's question: *can this member impersonate a more
privileged SA, or edit an IAM policy?*

## Starting points
- **External:** public GCS buckets, public Cloud Functions/Run, public Cloud SQL,
  public BigQuery datasets, leaked SA key JSON.
- **Assumed-breach:** given a user login or an SA key. Start with
  `gcloud auth list` / activate the key, then enumerate bindings.

## Tooling
- **gcloud / gsutil / bq** — `gcloud <svc> ...`; `gcloud auth activate-service-account --key-file key.json`.
- **[Prowler](../../upstream/prowler/)** — `prowler gcp` (115 checks); each finding names its check ID.
- **[ScoutSuite](https://github.com/nccgroup/ScoutSuite)** (`scout gcp`).
- **[GCPBucketBrute](https://github.com/RhinoSecurityLabs/GCPBucketBrute)** — public/privesc bucket discovery.
- **[GCP_Scanner](https://github.com/google/gcp_scanner)**, **hayat**, `gcloud ... --impersonate-service-account`.

## Phases → ATT&CK tactics

| Phase | Page | ATT&CK tactic(s) |
|---|---|---|
| Recon & enumeration | [01](01-recon-and-enumeration.md) | [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) |
| Access & credentials | [02](02-access-and-credentials.md) | [TA0001](../_cloud-base/TA0001-initial-access.md) · [TA0006](../_cloud-base/TA0006-credential-access.md) |
| Privilege escalation | [03](03-privilege-escalation.md) | [TA0004](../_cloud-base/TA0004-privilege-escalation.md) |
| Lateral movement & persistence | [04](04-lateral-movement-and-persistence.md) | [TA0008](../_cloud-base/TA0008-lateral-movement.md) · [TA0003](../_cloud-base/TA0003-persistence.md) · [TA0002](../_cloud-base/TA0002-execution.md) |
| Evasion | [05](05-evasion.md) | [TA0005](../_cloud-base/TA0005-stealth.md) · [TA0112](../_cloud-base/TA0112-defense-impairment.md) |
| Collection, exfil & impact | [06](06-collection-exfil-impact.md) | [TA0009](../_cloud-base/TA0009-collection.md) · [TA0010](../_cloud-base/TA0010-exfiltration.md) · [TA0040](../_cloud-base/TA0040-impact.md) |

## Adjacent scope
Apps on GCP → [ASVS base](../_asvs-base/README.md). GKE workloads → Kubernetes
(Prowler `kubernetes` provider). Google Workspace identity overlaps M365/Entra patterns.

## References
- [Cloud attack base](../_cloud-base/README.md) · [ATT&CK Cloud](https://attack.mitre.org/matrices/enterprise/cloud/)
- [GCP IAM privesc (Rhino)](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) · [HackTricks Cloud – GCP](https://cloud.hacktricks.xyz/)
