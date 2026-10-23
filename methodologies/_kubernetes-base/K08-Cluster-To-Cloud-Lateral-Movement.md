# K08: Cluster-To-Cloud Lateral Movement (Kubernetes)

> **OWASP Kubernetes Top 10 (2025) · K08** · ID, title, and Overview are verbatim from the official standard.
> Source: [`upstream/kubernetes-top-ten/2025/en/src/K08-Cluster-To-Cloud-Lateral-Movement.md`](../../upstream/kubernetes-top-ten/2025/en/src/K08-Cluster-To-Cloud-Lateral-Movement.md)
>
> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of the [cloud base](../_cloud-base/README.md)). A generated methodology (`kubernetes/`) projects this risk onto a real cluster: the component/sink, how to test with `kubectl`/tooling, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler check that detects it.

> **ATT&CK Containers tactics:** Lateral Movement, Credential Access.

## Overview (verbatim)

When Kubernetes is run on a cloud provider, the cluster's nodes and workloads are often granted permissions to interact with other cloud services (e.g., object storage, databases, metadata services). If an attacker compromises a container within the cluster, they can attempt to abuse these cloud permissions to "move laterally" from the Kubernetes cluster into the underlying cloud provider account, leading to a much wider and more severe breach.

Securing the boundary between the Kubernetes cluster and the cloud provider's API is essential to contain the impact of a potential compromise.

## Detective coverage — Prowler `kubernetes` checks

_No direct Prowler `kubernetes` check — this risk (cluster→cloud movement) is detected on the **cloud** side; cross-reference the [cloud base](../_cloud-base/README.md) (IMDS / instance credentials).

---

### Methodology projection (filled in `kubernetes/`, not here)

- **Component / sink** — the cluster object/config (Pod `securityContext`, RBAC binding, admission controller, NetworkPolicy, kubelet/apiserver flag).
- **How to test** — `kubectl`/`kubectl-who-can`/`kube-hunter`/`kube-bench`/Peirates/`kubeletctl` enumerate then attempt.
- **Positive (secure)** — request denied / control present.
- **Negative (vulnerable)** — breakout/escalation succeeds; the Prowler check above flags the misconfig.
