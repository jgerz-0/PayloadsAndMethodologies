# K05: Missing Network Segmentation Controls (Kubernetes)

> **OWASP Kubernetes Top 10 (2025) · K05** · ID, title, and Overview are verbatim from the official standard.
> Source: [`upstream/kubernetes-top-ten/2025/en/src/K05-Missing-Network-Segmentation-Controls.md`](../../upstream/kubernetes-top-ten/2025/en/src/K05-Missing-Network-Segmentation-Controls.md)
>
> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of the [cloud base](../_cloud-base/README.md)). A generated methodology (`kubernetes/`) projects this risk onto a real cluster: the component/sink, how to test with `kubectl`/tooling, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler check that detects it.

> **ATT&CK Containers tactics:** Lateral Movement.

## Overview (verbatim)

By default Kubernetes does not restrict traffic between pods in the cluster or from pods to services in the control plane, which allows attackers to target those systems. This can present a risk especially in large multi-tenant clusters, where many services may be available.

## Detective coverage — Prowler `kubernetes` checks

Relevant Prowler checks (service(s): core):

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

---

### Methodology projection (filled in `kubernetes/`, not here)

- **Component / sink** — the cluster object/config (Pod `securityContext`, RBAC binding, admission controller, NetworkPolicy, kubelet/apiserver flag).
- **How to test** — `kubectl`/`kubectl-who-can`/`kube-hunter`/`kube-bench`/Peirates/`kubeletctl` enumerate then attempt.
- **Positive (secure)** — request denied / control present.
- **Negative (vulnerable)** — breakout/escalation succeeds; the Prowler check above flags the misconfig.
