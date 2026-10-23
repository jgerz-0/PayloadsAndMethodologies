# TA0007 – Discovery (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0007 Discovery**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to figure out your environment.

Discovery consists of techniques an adversary may use to gain knowledge about the system and internal network. These techniques help adversaries observe the environment and orient themselves before deciding how to act. They also allow adversaries to explore what they can control and what’s around their entry point in order to discover how it could benefit their current objective. Native operating system tools are often used toward this post-compromise information-gathering objective.

> **Prowler config-check coverage (detective side):** AWS **8** checks tagged `TTPs/Discovery` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1040](https://attack.mitre.org/techniques/T1040) | **Network Sniffing** | IaaS |
| [T1046](https://attack.mitre.org/techniques/T1046) | **Network Service Discovery** | IaaS |
| [T1049](https://attack.mitre.org/techniques/T1049) | **System Network Connections Discovery** | IaaS |
| [T1069](https://attack.mitre.org/techniques/T1069) | **Permission Groups Discovery** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1069.003](https://attack.mitre.org/techniques/T1069/003) | &nbsp;&nbsp;↳ Cloud Groups | SaaS, IaaS, Office Suite, Identity Provider |
| [T1082](https://attack.mitre.org/techniques/T1082) | **System Information Discovery** | IaaS |
| [T1087](https://attack.mitre.org/techniques/T1087) | **Account Discovery** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1087.003](https://attack.mitre.org/techniques/T1087/003) | &nbsp;&nbsp;↳ Email Account | Office Suite |
| [T1087.004](https://attack.mitre.org/techniques/T1087/004) | &nbsp;&nbsp;↳ Cloud Account | IaaS, Identity Provider, Office Suite, SaaS |
| [T1201](https://attack.mitre.org/techniques/T1201) | **Password Policy Discovery** | IaaS, Identity Provider, SaaS, Office Suite |
| [T1518](https://attack.mitre.org/techniques/T1518) | **Software Discovery** | IaaS |
| [T1518.001](https://attack.mitre.org/techniques/T1518/001) | &nbsp;&nbsp;↳ Security Software Discovery | IaaS |
| [T1526](https://attack.mitre.org/techniques/T1526) | **Cloud Service Discovery** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1538](https://attack.mitre.org/techniques/T1538) | **Cloud Service Dashboard** | IaaS, SaaS, Office Suite, Identity Provider |
| [T1580](https://attack.mitre.org/techniques/T1580) | **Cloud Infrastructure Discovery** | IaaS |
| [T1614](https://attack.mitre.org/techniques/T1614) | **System Location Discovery** | IaaS |
| [T1619](https://attack.mitre.org/techniques/T1619) | **Cloud Storage Object Discovery** | IaaS |
| [T1654](https://attack.mitre.org/techniques/T1654) | **Log Enumeration** | IaaS |
| [T1680](https://attack.mitre.org/techniques/T1680) | **Local Storage Discovery** | IaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
