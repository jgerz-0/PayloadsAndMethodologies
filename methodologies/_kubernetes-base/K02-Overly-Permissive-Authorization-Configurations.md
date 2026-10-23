# K02: Overly Permissive Authorization Configurations (Kubernetes)

> **OWASP Kubernetes Top 10 (2025) · K02** · ID, title, and Overview are verbatim from the official standard.
> Source: [`upstream/kubernetes-top-ten/2025/en/src/K02-Overly-Permissive-Authorization-Configurations.md`](../../upstream/kubernetes-top-ten/2025/en/src/K02-Overly-Permissive-Authorization-Configurations.md)
>
> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of the [cloud base](../_cloud-base/README.md)). A generated methodology (`kubernetes/`) projects this risk onto a real cluster: the component/sink, how to test with `kubectl`/tooling, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler check that detects it.

> **ATT&CK Containers tactics:** Privilege Escalation, Lateral Movement.

## Overview (verbatim)

Kubernetes provides a rich and flexible set of options for authorizing users and services to operate on cluster objects. With that flexibility, goes the risk of excessive access which could allow for unauthorized access to Kubernetes resources.

## Detective coverage — Prowler `kubernetes` checks

Relevant Prowler checks (service(s): rbac):

| Check ID |
| :-- |
| `rbac_cluster_admin_usage` |
| `rbac_minimize_csr_approval_access` |
| `rbac_minimize_node_proxy_subresource_access` |
| `rbac_minimize_pod_creation_access` |
| `rbac_minimize_pv_creation_access` |
| `rbac_minimize_secret_access` |
| `rbac_minimize_service_account_token_creation` |
| `rbac_minimize_webhook_config_access` |
| `rbac_minimize_wildcard_use_roles` |

---

### Methodology projection (filled in `kubernetes/`, not here)

- **Component / sink** — the cluster object/config (Pod `securityContext`, RBAC binding, admission controller, NetworkPolicy, kubelet/apiserver flag).
- **How to test** — `kubectl`/`kubectl-who-can`/`kube-hunter`/`kube-bench`/Peirates/`kubeletctl` enumerate then attempt.
- **Positive (secure)** — request denied / control present.
- **Negative (vulnerable)** — breakout/escalation succeeds; the Prowler check above flags the misconfig.
