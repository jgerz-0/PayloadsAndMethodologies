# TA0010 – Exfiltration (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0010 Exfiltration**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to steal data.

Exfiltration consists of techniques that adversaries may use to steal data from your network. Once they’ve collected data, adversaries often package it to avoid detection while removing it. This can include compression and encryption. Techniques for getting data out of a target network typically include transferring it over their command and control channel or an alternate channel and may also include putting size limits on the transmission.

> **Prowler config-check coverage (detective side):** AWS **0** checks tagged `TTPs/Exfiltration` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1048](https://attack.mitre.org/techniques/T1048) | **Exfiltration Over Alternative Protocol** | IaaS, Office Suite, SaaS |
| [T1537](https://attack.mitre.org/techniques/T1537) | **Transfer Data to Cloud Account** | IaaS, Office Suite, SaaS |
| [T1567](https://attack.mitre.org/techniques/T1567) | **Exfiltration Over Web Service** | Office Suite, SaaS |
| [T1567.004](https://attack.mitre.org/techniques/T1567/004) | &nbsp;&nbsp;↳ Exfiltration Over Webhook | Office Suite, SaaS |
| [T1700](https://attack.mitre.org/techniques/T1700) | **AI-Enabled Exfiltration** | SaaS |
| [T1020.001](https://attack.mitre.org/techniques/T1020/001) | ↳ Traffic Duplication | IaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
