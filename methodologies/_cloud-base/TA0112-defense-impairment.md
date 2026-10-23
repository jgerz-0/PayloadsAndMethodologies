# TA0112 – Defense Impairment (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0112 Defense Impairment**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to break security mechanisms, pipelines, and tooling so defenders can’t see or trust what’s happening.

Defense Impairment consists of techniques that degrade, disable, or undermine the effectiveness and trustworthiness of security controls and monitoring mechanisms. These techniques are characterized by direct interference with defensive systems. The goal is to reduce defenders’ ability to detect, interpret, or respond to adversary activity.

> **Prowler config-check coverage (detective side):** AWS **16** checks tagged `TTPs/Defense Impairment` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1484](https://attack.mitre.org/techniques/T1484) | **Domain or Tenant Policy Modification** | Identity Provider |
| [T1484.002](https://attack.mitre.org/techniques/T1484/002) | &nbsp;&nbsp;↳ Trust Modification | Identity Provider |
| [T1556](https://attack.mitre.org/techniques/T1556) | **Modify Authentication Process** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.006](https://attack.mitre.org/techniques/T1556/006) | &nbsp;&nbsp;↳ Multi-Factor Authentication | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.007](https://attack.mitre.org/techniques/T1556/007) | &nbsp;&nbsp;↳ Hybrid Identity | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.009](https://attack.mitre.org/techniques/T1556/009) | &nbsp;&nbsp;↳ Conditional Access Policies | IaaS, Identity Provider |
| [T1578](https://attack.mitre.org/techniques/T1578) | **Modify Cloud Compute Infrastructure** | IaaS |
| [T1578.001](https://attack.mitre.org/techniques/T1578/001) | &nbsp;&nbsp;↳ Create Snapshot | IaaS |
| [T1578.002](https://attack.mitre.org/techniques/T1578/002) | &nbsp;&nbsp;↳ Create Cloud Instance | IaaS |
| [T1578.003](https://attack.mitre.org/techniques/T1578/003) | &nbsp;&nbsp;↳ Delete Cloud Instance | IaaS |
| [T1578.004](https://attack.mitre.org/techniques/T1578/004) | &nbsp;&nbsp;↳ Revert Cloud Instance | IaaS |
| [T1578.005](https://attack.mitre.org/techniques/T1578/005) | &nbsp;&nbsp;↳ Modify Cloud Compute Configurations | IaaS |
| [T1666](https://attack.mitre.org/techniques/T1666) | **Modify Cloud Resource Hierarchy** | IaaS |
| [T1685](https://attack.mitre.org/techniques/T1685) | **Disable or Modify Tools** | IaaS |
| [T1685.002](https://attack.mitre.org/techniques/T1685/002) | &nbsp;&nbsp;↳ Disable or Modify Cloud Log | IaaS, SaaS, Identity Provider, Office Suite |
| [T1685.007](https://attack.mitre.org/techniques/T1685/007) | &nbsp;&nbsp;↳ Impair Autonomous Defenses | SaaS |
| [T1687](https://attack.mitre.org/techniques/T1687) | **Exploitation for Defense Impairment** | IaaS, SaaS |
| [T1686.001](https://attack.mitre.org/techniques/T1686/001) | ↳ Cloud Firewall | IaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
