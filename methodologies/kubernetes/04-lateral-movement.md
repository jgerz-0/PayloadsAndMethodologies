# Kubernetes · Phase 4 — Lateral Movement

> OWASP [K05 Missing Network Segmentation](../_kubernetes-base/K05-Missing-Network-Segmentation-Controls.md)
> + [K03 Secrets Management Failures](../_kubernetes-base/K03-Secrets-Management-Failures.md).

## Pod-to-pod / pod-to-service (K05)
- **Component/sink:** flat pod network with no `NetworkPolicy` — any pod can
  reach any other pod, the API server, and cloud metadata.
  ```sh
  kubectl get networkpolicy -A                    # none? flat network
  # from a pod: scan the pod CIDR, hit internal services, reach 169.254.169.254
  nmap -sT <pod-cidr> ; curl http://<internal-svc>.<ns>.svc.cluster.local
  ```
- **Positive (secure):** default-deny `NetworkPolicy` per namespace; egress to
  metadata blocked. Prowler `core_minimize_*`/network-policy checks.
- **Negative (vulnerable):** free pod-to-pod + egress to metadata → lateral reach
  and the cloud pivot ([Phase 5](05-cluster-to-cloud.md)).

## Harvest secrets & service-account tokens (K03)
- **Component/sink:** Kubernetes Secrets (base64, **not encrypted** by default),
  mounted SA tokens, secrets in env/ConfigMaps.
  ```sh
  kubectl get secrets -A -o json | jq '.items[].data'      # base64 only
  kubectl get secret <s> -o jsonpath='{.data.token}' | base64 -d
  # from a breakout (Phase 3): read other pods' tokens from the node
  find /var/lib/kubelet/pods -name token 2>/dev/null
  ```
- **Positive (secure):** etcd **encryption at rest** on
  (`apiserver_encryption_provider_config_set`), external secrets manager
  (Vault/CSI), `automountServiceAccountToken: false` where unused,
  short-lived projected tokens. Prowler `apiserver_encryption_provider_config_set`.
- **Negative (vulnerable):** readable Secrets / mounted tokens of privileged SAs
  → impersonate those SAs, decrypt app data. A stolen privileged SA token used
  against the API moves you across namespaces.

## Impersonation / token reuse
A harvested SA token or a user with `impersonate` lets you act as any
principal: `kubectl --token=<stolen>` or `kubectl --as=<user> --as-group=<grp>`.

---
*Next: [Phase 5 — Cluster → Cloud](05-cluster-to-cloud.md).*
