# TA0001 – Initial Access (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0001 Initial Access**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to get into your network.

Initial Access consists of techniques that use various entry vectors to gain their initial foothold within a network. Techniques used to gain a foothold include targeted spearphishing and exploiting weaknesses on public-facing web servers. Footholds gained through initial access may allow for continued access, like valid accounts and use of external remote services, or may be limited-use due to changing passwords.

> **Prowler config-check coverage (detective side):** AWS **117** checks tagged `TTPs/Initial Access` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1078](https://attack.mitre.org/techniques/T1078) | **Valid Accounts** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1078.001](https://attack.mitre.org/techniques/T1078/001) | &nbsp;&nbsp;↳ Default Accounts | IaaS, Identity Provider, Office Suite, SaaS |
| [T1078.004](https://attack.mitre.org/techniques/T1078/004) | &nbsp;&nbsp;↳ Cloud Accounts | IaaS, Identity Provider, Office Suite, SaaS |
| [T1189](https://attack.mitre.org/techniques/T1189) | **Drive-by Compromise** | Identity Provider |
| [T1190](https://attack.mitre.org/techniques/T1190) | **Exploit Public-Facing Application** | IaaS |
| [T1195](https://attack.mitre.org/techniques/T1195) | **Supply Chain Compromise** | SaaS |
| [T1199](https://attack.mitre.org/techniques/T1199) | **Trusted Relationship** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1566](https://attack.mitre.org/techniques/T1566) | **Phishing** | Identity Provider, Office Suite, SaaS |
| [T1566.002](https://attack.mitre.org/techniques/T1566/002) | &nbsp;&nbsp;↳ Spearphishing Link | Identity Provider, Office Suite, SaaS |
| [T1566.004](https://attack.mitre.org/techniques/T1566/004) | &nbsp;&nbsp;↳ Spearphishing Voice | Identity Provider |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
