# Kubernetes · Phase 2 — Initial Access

> OWASP [K06 Overly Exposed Components](../_kubernetes-base/K06-Overly-Exposed-Kubernetes-Components.md),
> [K09 Broken Authentication](../_kubernetes-base/K09-Broken-Authentication-Mechanisms.md),
> [K07 Misconfigured/Vulnerable Components](../_kubernetes-base/K07-Misconfigured-And-Vulnerable-Cluster-Components.md).

#### Anonymous / exposed API server (K06/K09)
- **Component/sink:** `kube-apiserver` with `--anonymous-auth=true` or the legacy
  insecure port, reachable from outside.
  ```sh
  curl -k https://<api>:6443/api/v1/namespaces/default/pods        # no creds
  kubectl --server=https://<api>:6443 --insecure-skip-tls-verify get pods
  ```
- **Positive (secure):** `401 Unauthorized`; anonymous auth off. Prowler
  `apiserver_anonymous_requests`, `apiserver_token_auth_file_not_set`.
- **Negative (vulnerable):** anonymous read/list (or worse) → cluster recon/access.

#### Exposed kubelet (K06)
- **Component/sink:** kubelet read-only `:10255` or the authenticated `:10250`
  allowing anonymous/`system:anonymous`.
  ```sh
  curl -k https://<node>:10250/pods                       # list pods
  kubeletctl -i --server <node> pods
  kubeletctl -i --server <node> exec "id" -p <pod> -c <container>   # RCE in a pod
  ```
- **Positive (secure):** kubelet `--anonymous-auth=false`, `--authorization-mode=Webhook`.
  Prowler `kubelet_authorization_mode`, `apiserver_kubelet_authz_rbac`.
- **Negative (vulnerable):** `/exec` runs commands in containers → shell in a pod.

#### etcd / dashboard / other (K06)
- **etcd `:2379`** without client-cert auth → dump **all** cluster secrets.
  Prowler `etcd_tls_encryption`, `etcd_client_cert_auth`.
- **Kubernetes Dashboard** exposed with a privileged SA → full control.

#### App RCE → in-pod foothold (K07)
A vulnerable app in a pod (SSRF/RCE — see [ASVS](../_asvs-base/README.md)) gives
a shell + the pod's **service-account token** → pivot to the API
([Phase 3](03-privesc-and-breakout.md)).

---
*Next: [Phase 3 — Privesc & Node Breakout](03-privesc-and-breakout.md).*
