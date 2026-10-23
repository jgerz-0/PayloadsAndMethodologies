# K04: Lack Of Cluster Level Policy Enforcement (Kubernetes)

> **OWASP Kubernetes Top 10 (2025) · K04** · ID, title, and Overview are verbatim from the official standard.
> Source: [`upstream/kubernetes-top-ten/2025/en/src/K04-Lack-Of-Cluster-Level-Policy-Enforcement.md`](../../upstream/kubernetes-top-ten/2025/en/src/K04-Lack-Of-Cluster-Level-Policy-Enforcement.md)
>
> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of the [cloud base](../_cloud-base/README.md)). A generated methodology (`kubernetes/`) projects this risk onto a real cluster: the component/sink, how to test with `kubectl`/tooling, and **positive (secure) vs negative (vulnerable)** evidence, tied to the Prowler check that detects it.

> **ATT&CK Containers tactics:** Defense Impairment, Stealth.

## Overview (verbatim)

Out of the box, Kubernetes provides significant flexibility in how workloads and resources are configured. While this is powerful, it lacks a default, cluster-wide mechanism for enforcing security policies. This can lead to security gaps and misconfigurations as clusters scale and are managed by multiple teams.

It is important to leverage Kubernetes' built-in policy mechanisms and, where necessary, its native extension points to ensure that all resources deployed to the cluster adhere to organizational and security best practices.

## Detective coverage — Prowler `kubernetes` checks

Relevant Prowler checks (service(s): apiserver):

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

---

### Methodology projection (filled in `kubernetes/`, not here)

- **Component / sink** — the cluster object/config (Pod `securityContext`, RBAC binding, admission controller, NetworkPolicy, kubelet/apiserver flag).
- **How to test** — `kubectl`/`kubectl-who-can`/`kube-hunter`/`kube-bench`/Peirates/`kubeletctl` enumerate then attempt.
- **Positive (secure)** — request denied / control present.
- **Negative (vulnerable)** — breakout/escalation succeeds; the Prowler check above flags the misconfig.
