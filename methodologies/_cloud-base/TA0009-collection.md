# TA0009 – Collection (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0009 Collection**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to gather data of interest to their goal.

Collection consists of techniques adversaries may use to gather information and the sources information is collected from that are relevant to following through on the adversary's objectives. Frequently, the next goal after collecting data is to either steal (exfiltrate) the data or to use the data to gain more information about the target environment. Common target sources include various drive types, browsers, audio, video, and email. Common collection methods include capturing screenshots and keyboard input.

> **Prowler config-check coverage (detective side):** AWS **2** checks tagged `TTPs/Collection` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1074](https://attack.mitre.org/techniques/T1074) | **Data Staged** | IaaS |
| [T1074.002](https://attack.mitre.org/techniques/T1074/002) | &nbsp;&nbsp;↳ Remote Data Staging | IaaS |
| [T1114](https://attack.mitre.org/techniques/T1114) | **Email Collection** | Office Suite |
| [T1114.002](https://attack.mitre.org/techniques/T1114/002) | &nbsp;&nbsp;↳ Remote Email Collection | Office Suite |
| [T1114.003](https://attack.mitre.org/techniques/T1114/003) | &nbsp;&nbsp;↳ Email Forwarding Rule | Office Suite |
| [T1119](https://attack.mitre.org/techniques/T1119) | **Automated Collection** | IaaS, Office Suite, SaaS |
| [T1213](https://attack.mitre.org/techniques/T1213) | **Data from Information Repositories** | SaaS, IaaS, Office Suite |
| [T1213.001](https://attack.mitre.org/techniques/T1213/001) | &nbsp;&nbsp;↳ Confluence | SaaS |
| [T1213.002](https://attack.mitre.org/techniques/T1213/002) | &nbsp;&nbsp;↳ Sharepoint | Office Suite |
| [T1213.003](https://attack.mitre.org/techniques/T1213/003) | &nbsp;&nbsp;↳ Code Repositories | SaaS |
| [T1213.004](https://attack.mitre.org/techniques/T1213/004) | &nbsp;&nbsp;↳ Customer Relationship Management Software | SaaS |
| [T1213.005](https://attack.mitre.org/techniques/T1213/005) | &nbsp;&nbsp;↳ Messaging Applications | Office Suite, SaaS |
| [T1213.006](https://attack.mitre.org/techniques/T1213/006) | &nbsp;&nbsp;↳ Databases | IaaS, SaaS |
| [T1530](https://attack.mitre.org/techniques/T1530) | **Data from Cloud Storage** | IaaS, Office Suite, SaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
