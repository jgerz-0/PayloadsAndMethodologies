# Kubernetes Testing Methodology (OWASP K8s Top 10-aligned)

> Offensive testing methodology for **Kubernetes** clusters (EKS/GKE/AKS/
> self-managed), structured against the
> [Kubernetes base](../_kubernetes-base/README.md) (OWASP Kubernetes Top 10 2025
> + ATT&CK Containers + Prowler). Organized by **attack phase**; each OWASP risk
> (K01–K10) is projected onto a real cluster with `kubectl`/tooling, and
> **positive (secure, `Forbidden`) vs negative (vulnerable)** evidence tied to
> the **Prowler `kubernetes` check ID**.

> **Authorization.** Test only clusters you're authorized to. Pod breakout and
> control-plane access are high-impact — assume an **authorized** engagement and
> prefer non-destructive confirmation.

## Attack model
Kubernetes pentests follow a chain: get a foothold (exposed component, app RCE,
or a token), enumerate what that identity can do, **escalate** (workload
misconfig → node breakout, or RBAC → cluster-admin), move **laterally** (pod→pod,
secrets, service tokens), then pivot **cluster→cloud** (the node's cloud
instance credentials — the highest-impact step). Starting point is usually one
of: **external** (exposed API server / kubelet / dashboard), **in-pod** (app RCE
gives you a shell + the pod's service-account token), or **assumed-breach**
(given a kubeconfig / token).

## Tooling
- **kubectl** + **[kubectl-who-can](https://github.com/aquasecurity/kubectl-who-can)** / `kubectl auth can-i --list`.
- **[Prowler](../../upstream/prowler/)** — `prowler kubernetes` (92 checks); findings name the check ID.
- **[kube-bench](https://github.com/aquasecurity/kube-bench)** (CIS), **[kube-hunter](https://github.com/aquasecurity/kube-hunter)**, **[kubescape](https://github.com/kubescape/kubescape)** (scans against this Top 10), **[Peirates](https://github.com/inguardians/peirates)** (in-pod attack tool), **[kubeletctl](https://github.com/cyberark/kubeletctl)**.

## Phases → OWASP K8s Top 10 risks

| Phase | Page | OWASP risk(s) |
|---|---|---|
| Recon & enumeration | [01](01-recon-and-enumeration.md) | surface for all |
| Initial access | [02](02-initial-access.md) | [K06](../_kubernetes-base/K06-Overly-Exposed-Kubernetes-Components.md) · [K09](../_kubernetes-base/K09-Broken-Authentication-Mechanisms.md) · [K07](../_kubernetes-base/K07-Misconfigured-And-Vulnerable-Cluster-Components.md) |
| Privesc & node breakout | [03](03-privesc-and-breakout.md) | [K01](../_kubernetes-base/K01-Insecure-Workload-Configurations.md) · [K02](../_kubernetes-base/K02-Overly-Permissive-Authorization-Configurations.md) |
| Lateral movement | [04](04-lateral-movement.md) | [K05](../_kubernetes-base/K05-Missing-Network-Segmentation-Controls.md) · [K03](../_kubernetes-base/K03-Secrets-Management-Failures.md) |
| Cluster → cloud | [05](05-cluster-to-cloud.md) | [K08](../_kubernetes-base/K08-Cluster-To-Cloud-Lateral-Movement.md) |
| Evasion & impact | [06](06-evasion-and-impact.md) | [K04](../_kubernetes-base/K04-Lack-Of-Cluster-Level-Policy-Enforcement.md) · [K10](../_kubernetes-base/K10-Inadequate-Logging-And-Monitoring.md) |

## Adjacent scope
The node's cloud account → the matching [cloud methodology](../_cloud-base/README.md)
(AWS/GCP/Azure). Apps in pods → [ASVS](../_asvs-base/README.md). Supply chain
(images) → [K07] + image scanning.

## References
- [Kubernetes base](../_kubernetes-base/README.md) · [OWASP K8s Top 10](https://owasp.org/www-project-kubernetes-top-ten/)
- [HackTricks Cloud – Kubernetes](https://cloud.hacktricks.xyz/) · [ATT&CK Containers](https://attack.mitre.org/matrices/enterprise/containers/)
