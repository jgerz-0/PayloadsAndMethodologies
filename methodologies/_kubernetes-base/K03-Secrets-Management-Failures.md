# K03: Secrets Management Failures (Kubernetes)

> **OWASP Kubernetes Top 10 (2025) · K03** · ID, title, and Overview are verbatim from the official standard.
> Source: [`upstream/kubernetes-top-ten/2025/en/src/K03-Secrets-Management-Failures.md`](../../upstream/kubernetes-top-ten/2025/en/src/K03-Secrets-Management-Failures.md)
>
> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of the [cloud base](../_cloud-base/README.md)). A generated methodology (`kubernetes/`) projects this risk onto a real cluster: the component/sink, how to test with `kubectl`/tooling, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler check that detects it.

> **ATT&CK Containers tactics:** Credential Access.

## Overview (verbatim)

Applications running in Kubernetes clusters need access to secrets (e.g. API keys, database credentials) for their operation, and it's important to ensure that these secrets are managed securely, as unauthorized access to secrets can have serious consequences for organization's security.

## Detective coverage — Prowler `kubernetes` checks

Relevant Prowler checks (service(s): apiserver, etcd, core):

| Check ID |
| :-- |
| `apiserver_always_pull_images_plugin` |
| `apiserver_anonymous_requests` |
| `apiserver_audit_log_maxage_set` |
| `apiserver_audit_log_maxbackup_set` |
| `apiserver_audit_log_maxsize_set` |
| `apiserver_audit_log_path_set` |
| `apiserver_auth_mode_include_node` |
| `apiserver_auth_mode_include_rbac` |
| `apiserver_auth_mode_not_always_allow` |
| `apiserver_client_ca_file_set` |
| `apiserver_deny_service_external_ips` |
| `apiserver_disable_profiling` |
| `apiserver_encryption_provider_config_set` |
| `apiserver_etcd_cafile_set` |
| `apiserver_etcd_tls_config` |
| `apiserver_event_rate_limit` |
| `apiserver_kubelet_cert_auth` |
| `apiserver_kubelet_tls_auth` |
| `apiserver_namespace_lifecycle_plugin` |
| `apiserver_no_always_admit_plugin` |
| `apiserver_no_token_auth_file` |
| `apiserver_node_restriction_plugin` |
| `apiserver_request_timeout_set` |
| `apiserver_security_context_deny_plugin` |
| `apiserver_service_account_key_file_set` |
| `apiserver_service_account_lookup_true` |
| `apiserver_service_account_plugin` |
| `apiserver_strong_ciphers_only` |
| `apiserver_tls_config` |
| `etcd_client_cert_auth` |
| `etcd_no_auto_tls` |
| `etcd_no_peer_auto_tls` |
| `etcd_peer_client_cert_auth` |
| `etcd_peer_tls_config` |
| `etcd_tls_encryption` |
| `etcd_unique_ca` |
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
