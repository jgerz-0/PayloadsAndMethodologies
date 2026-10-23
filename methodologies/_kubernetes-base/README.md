# Kubernetes Base (OWASP Kubernetes Top 10 2025 + ATT&CK Containers + Prowler)

> Framework-agnostic **source of truth** for Kubernetes testing — a sibling of
> the [cloud base](../_cloud-base/README.md). Kubernetes isn't an IaaS provider,
> so it gets its own base anchored on the recognized standard, the **OWASP
> Kubernetes Top 10 (2025)** (vendored at
> [`upstream/kubernetes-top-ten`](../../upstream/kubernetes-top-ten/)), with each
> risk cross-referenced to **Prowler** `kubernetes` checks
> ([`upstream/prowler`](../../upstream/prowler/), 92 checks) and the **MITRE
> ATT&CK Containers** matrix.

One markdown per risk (K01–K10), risk ID/title/Overview **verbatim** from OWASP.
The base says **what** can be wrong; the [`kubernetes/`](../kubernetes/README.md)
methodology says **how to test it** on a real cluster with payloads and
positive/negative evidence.

## Which base
Use this for a **Kubernetes cluster** (EKS/GKE/AKS/self-managed). The hosting
cloud account is the [cloud base](../_cloud-base/README.md); apps in pods are
[ASVS](../_asvs-base/README.md). The **cluster→cloud** boundary (K08) is where
this base and the cloud base meet.

## Risks (OWASP Kubernetes Top 10 2025)

| Risk | Prowler checks | ATT&CK Containers | Base page |
|---|--:|---|---|
| K01 Insecure Workload Configurations | 31 | PrivEsc, Execution | [K01](K01-Insecure-Workload-Configurations.md) |
| K02 Overly Permissive Authorization | 9 | PrivEsc, Lateral | [K02](K02-Overly-Permissive-Authorization-Configurations.md) |
| K03 Secrets Management Failures | 58 | Credential Access | [K03](K03-Secrets-Management-Failures.md) |
| K04 Lack of Cluster-Level Policy Enforcement | 29 | Defense Impairment | [K04](K04-Lack-Of-Cluster-Level-Policy-Enforcement.md) |
| K05 Missing Network Segmentation Controls | 22 | Lateral Movement | [K05](K05-Missing-Network-Segmentation-Controls.md) |
| K06 Overly Exposed Kubernetes Components | 52 | Initial Access | [K06](K06-Overly-Exposed-Kubernetes-Components.md) |
| K07 Misconfigured & Vulnerable Cluster Components | 54 | Initial Access, PrivEsc | [K07](K07-Misconfigured-And-Vulnerable-Cluster-Components.md) |
| K08 Cluster to Cloud Lateral Movement | 0¹ | Lateral, Credential Access | [K08](K08-Cluster-To-Cloud-Lateral-Movement.md) |
| K09 Broken Authentication Mechanisms | 29 | Initial Access, Credential Access | [K09](K09-Broken-Authentication-Mechanisms.md) |
| K10 Inadequate Logging and Monitoring | 29 | Stealth, Defense Impairment | [K10](K10-Inadequate-Logging-And-Monitoring.md) |

¹ K08 is detected on the **cloud** side (instance-metadata / instance creds) —
cross-reference the [cloud base](../_cloud-base/README.md).

## Regenerating
```sh
git submodule update --remote upstream/kubernetes-top-ten upstream/prowler
python3 methodologies/_kubernetes-base/generate.py
git add upstream/kubernetes-top-ten upstream/prowler methodologies/_kubernetes-base
git commit -m "chore: regenerate kubernetes base"
```
`generate.py` copies risk ID/title/Overview verbatim and maps each to Prowler
services + ATT&CK Containers tactics; only the chrome is house style.

## References
- [OWASP Kubernetes Top 10](https://owasp.org/www-project-kubernetes-top-ten/) (vendored) · [ATT&CK Containers matrix](https://attack.mitre.org/matrices/enterprise/containers/)
- [Prowler](../../upstream/prowler/) · tools: `kube-bench` (CIS), `kube-hunter`, `kubescape`, `Peirates`, `kubeletctl`, `kubectl-who-can`
- Siblings: [cloud base](../_cloud-base/README.md) · [ASVS](../_asvs-base/README.md)
