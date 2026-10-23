# K01: Insecure Workload Configurations (Kubernetes)

> **OWASP Kubernetes Top 10 (2025) · K01** · ID, title, and Overview are verbatim from the official standard.
> Source: [`upstream/kubernetes-top-ten/2025/en/src/K01-Insecure-Workload-Configurations.md`](../../upstream/kubernetes-top-ten/2025/en/src/K01-Insecure-Workload-Configurations.md)
>
> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of the [cloud base](../_cloud-base/README.md)). A generated methodology (`kubernetes/`) projects this risk onto a real cluster: the component/sink, how to test with `kubectl`/tooling, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler check that detects it.

> **ATT&CK Containers tactics:** Privilege Escalation, Execution.

## Overview (verbatim)

By default, workloads running in a Kubernetes cluster do not have strong security posture, which could make it easier for attackers to compromise applications and expand their compromise to other workloads or the cluster control plane.

It's vital that `securityContext` settings are implemented and other hardening steps are applied to improve the overall security of the cluster.

## Detective coverage — Prowler `kubernetes` checks

Relevant Prowler checks (service(s): core, rbac):

| Check ID |
| :-- |
| `core_cpu_limits_set` |
| `core_cpu_requests_set` |
| `core_image_tag_fixed` |
| `core_liveness_probe_configured` |
| `core_memory_limits_set` |
| `core_memory_requests_set` |
| `core_minimize_admission_hostport_containers` |
| `core_minimize_admission_windows_hostprocess_containers` |
| `core_minimize_allowPrivilegeEscalation_containers` |
| `core_minimize_containers_added_capabilities` |
| `core_minimize_containers_capabilities_assigned` |
| `core_minimize_hostIPC_containers` |
| `core_minimize_hostNetwork_containers` |
| `core_minimize_hostPID_containers` |
| `core_minimize_hostpath_volume_mounts` |
| `core_minimize_net_raw_capability_admission` |
| `core_minimize_privileged_containers` |
| `core_minimize_root_containers_admission` |
| `core_no_secrets_envs` |
| `core_readiness_probe_configured` |
| `core_readonly_root_filesystem_enabled` |
| `core_seccomp_profile_docker_default` |
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
