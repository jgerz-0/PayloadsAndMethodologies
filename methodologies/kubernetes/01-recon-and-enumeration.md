# Kubernetes · Phase 1 — Recon & Enumeration

> Surface discovery for the [Kubernetes base](../_kubernetes-base/README.md)
> risks. Know your identity, what it can do, and what's exposed.

## Who am I / what can I do
```sh
kubectl auth whoami
kubectl auth can-i --list                      # your effective permissions
kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>   # a SA's perms
kubectl-who-can create pods                    # reverse: who holds a verb
```
- **Positive (secure):** namespaced, minimal verbs; `can-i create pods`/`*` = no.
- **Negative (vulnerable):** broad verbs (`*` on `*`, cluster-scoped) → likely a
  privesc/lateral path ([Phase 3](03-privesc-and-breakout.md)). Prowler
  `rbac_cluster_admin_usage`, `rbac_minimize_wildcard_use_roles`.

## Cluster enumeration (from a token/kubeconfig)
```sh
kubectl get nodes,ns,pods -A -o wide
kubectl get roles,rolebindings,clusterroles,clusterrolebindings -A
kubectl get secrets -A                          # if permitted
kubectl get pods -A -o jsonpath='{..image}'     # images (supply chain, K07)
```

## In-pod enumeration (you have a shell in a container)
```sh
# the pod's service-account token — the keys to the API:
cat /var/run/secrets/kubernetes.io/serviceaccount/token
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace
env | grep -i KUBERNETES                         # API server address
# am I privileged? can I see the host?
id; capsh --print; ls -la /; mount | grep -i host
```
Peirates automates in-pod enumeration + attacks.

## External surface
#### exposed control-plane / node components (→ [K06](../_kubernetes-base/K06-Overly-Exposed-Kubernetes-Components.md))
```sh
kube-hunter --remote <cluster-ip>               # scans for exposed API/kubelet/etcd/dashboard
```
- API server `:6443`/`:8080`, kubelet `:10250`/`:10255`, etcd `:2379`, dashboard,
  cAdvisor. Negative: anonymous/insecure access (see [Phase 2](02-initial-access.md)).

---
*Next: [Phase 2 — Initial Access](02-initial-access.md).*
