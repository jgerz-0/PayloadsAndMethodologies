# K07: Misconfigured And Vulnerable Cluster Components (Kubernetes)

> **OWASP Kubernetes Top 10 (2025) · K07** · ID, title, and Overview are verbatim from the official standard.
> Source: [`upstream/kubernetes-top-ten/2025/en/src/K07-Misconfigured-And-Vulnerable-Cluster-Components.md`](../../upstream/kubernetes-top-ten/2025/en/src/K07-Misconfigured-And-Vulnerable-Cluster-Components.md)
>
> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of the [cloud base](../_cloud-base/README.md)). A generated methodology (`kubernetes/`) projects this risk onto a real cluster: the component/sink, how to test with `kubectl`/tooling, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler check that detects it.

> **ATT&CK Containers tactics:** Initial Access, Privilege Escalation.

## Overview (verbatim)

Misconfigurations and vulnerabilities in cluster components can leave them exposed to attackers, allowing for easier compromise of applications and the cluster itself. As Kubernetes ships without hardened defaults, it's important to change default settings to improve cluster security.

## Detective coverage — Prowler `kubernetes` checks

Relevant Prowler checks (service(s): kubelet, scheduler, controllermanager, apiserver):

| Check ID |
| :-- |
| `kubelet_authorization_mode` |
| `kubelet_client_ca_file_set` |
| `kubelet_conf_file_ownership` |
| `kubelet_conf_file_permissions` |
| `kubelet_config_yaml_ownership` |
| `kubelet_config_yaml_permissions` |
| `kubelet_disable_anonymous_auth` |
| `kubelet_disable_read_only_port` |
| `kubelet_event_record_qps` |
| `kubelet_manage_iptables` |
| `kubelet_rotate_certificates` |
| `kubelet_service_file_ownership_root` |
| `kubelet_service_file_permissions` |
| `kubelet_streaming_connection_timeout` |
| `kubelet_strong_ciphers_only` |
| `kubelet_tls_cert_and_key` |
| `scheduler_bind_address` |
| `scheduler_profiling` |
| `controllermanager_bind_address` |
| `controllermanager_disable_profiling` |
| `controllermanager_garbage_collection` |
| `controllermanager_root_ca_file_set` |
| `controllermanager_rotate_kubelet_server_cert` |
| `controllermanager_service_account_credentials` |
| `controllermanager_service_account_private_key_file` |
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

---

### Methodology projection (filled in `kubernetes/`, not here)

- **Component / sink** — the cluster object/config (Pod `securityContext`, RBAC binding, admission controller, NetworkPolicy, kubelet/apiserver flag).
- **How to test** — `kubectl`/`kubectl-who-can`/`kube-hunter`/`kube-bench`/Peirates/`kubeletctl` enumerate then attempt.
- **Positive (secure)** — request denied / control present.
- **Negative (vulnerable)** — breakout/escalation succeeds; the Prowler check above flags the misconfig.
