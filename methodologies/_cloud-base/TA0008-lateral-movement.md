# TA0008 – Lateral Movement (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0008 Lateral Movement**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to move through your environment.

Lateral Movement consists of techniques that adversaries use to enter and control remote systems on a network. Following through on their primary objective often requires exploring the network to find their target, then pivoting through multiple systems and accounts to gain access to it. Adversaries might install their own remote access tools to accomplish Lateral Movement or use legitimate credentials with native network and operating system tools, which may be stealthier.

> **Prowler config-check coverage (detective side):** AWS **6** checks tagged `TTPs/Lateral Movement` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1021](https://attack.mitre.org/techniques/T1021) | **Remote Services** | IaaS |
| [T1021.007](https://attack.mitre.org/techniques/T1021/007) | &nbsp;&nbsp;↳ Cloud Services | IaaS, Identity Provider, Office Suite, SaaS |
| [T1021.008](https://attack.mitre.org/techniques/T1021/008) | &nbsp;&nbsp;↳ Direct Cloud VM Connections | IaaS |
| [T1072](https://attack.mitre.org/techniques/T1072) | **Software Deployment Tools** | SaaS |
| [T1080](https://attack.mitre.org/techniques/T1080) | **Taint Shared Content** | SaaS, Office Suite |
| [T1534](https://attack.mitre.org/techniques/T1534) | **Internal Spearphishing** | Office Suite, SaaS |
| [T1550](https://attack.mitre.org/techniques/T1550) | **Use Alternate Authentication Material** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1550.001](https://attack.mitre.org/techniques/T1550/001) | &nbsp;&nbsp;↳ Application Access Token | IaaS, Identity Provider, Office Suite, SaaS |
| [T1550.004](https://attack.mitre.org/techniques/T1550/004) | &nbsp;&nbsp;↳ Web Session Cookie | IaaS, Office Suite, SaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
