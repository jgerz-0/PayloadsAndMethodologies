# Kubernetes · Phase 6 — Evasion & Impact

> OWASP [K04 Lack of Cluster-Level Policy Enforcement](../_kubernetes-base/K04-Lack-Of-Cluster-Level-Policy-Enforcement.md)
> + [K10 Inadequate Logging and Monitoring](../_kubernetes-base/K10-Inadequate-Logging-And-Monitoring.md).
> **Confirm non-destructively where possible.**

## Policy-enforcement gaps (K04) — what lets the above succeed
- **Component/sink:** admission control — Pod Security Admission (PSA),
  OPA/Gatekeeper, Kyverno, validating/mutating webhooks.
  ```sh
  kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations
  kubectl label ns <ns> pod-security.kubernetes.io/enforce=restricted --dry-run=server -o yaml
  ```
- **Positive (secure):** PSA `restricted` enforced cluster-wide; Gatekeeper/
  Kyverno deny privileged/hostPath pods. Prowler
  `apiserver_admission_control_plugins_*` (e.g. `NodeRestriction`, `PodSecurity`).
- **Negative (vulnerable):** no admission policy → the privileged-pod breakout in
  [Phase 3](03-privesc-and-breakout.md) is accepted. (A disabled/ bypassable
  admission webhook is a defense-evasion finding.)

## Logging & detection gaps (K10) — evasion
- **Component/sink:** API server **audit logging**, falco/runtime detection.
  ```sh
  # check apiserver flags: --audit-log-path, --audit-policy-file
  kubectl get pod -n kube-system kube-apiserver-<node> -o yaml | grep -i audit
  ```
- **Positive (secure):** audit logging on with a sound policy, shipped off-cluster;
  runtime detection (Falco). Prowler `apiserver_audit_log_path_set`,
  `apiserver_audit_log_maxage_set`, `apiserver_audit_log_maxbackup_set`.
- **Negative (vulnerable):** no/!minimal audit logging → exec, secret reads, and
  privileged-pod creation go unrecorded. Deleting events / using `exec` (not a
  new pod) further reduces footprint.

## Impact
#### T1496 Resource Hijacking · T1485 Data Destruction · T1489 Service Stop
- Cryptomining pods, deleting Deployments/PVCs, draining nodes, deploying a
  malicious DaemonSet (runs on every node), or encrypting PV data.
- **Positive (secure):** ResourceQuota/LimitRange; RBAC denies delete on
  workloads; immutable backups (Velero). **Negative:** able to schedule
  workloads cluster-wide / delete PVCs → DoS or data loss. **Confirm via
  `can-i`/dry-run, don't execute in prod.**

---
*Back to [Kubernetes README](README.md). Cloud pivot: [Phase 5](05-cluster-to-cloud.md).*
