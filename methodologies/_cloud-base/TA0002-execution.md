# TA0002 – Execution (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0002 Execution**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to run malicious code or instructions on a system.

Execution consists of techniques that result in adversary-controlled code running on a local or remote system. Techniques that run malicious code are often paired with techniques from all other tactics to achieve broader goals, like exploring a network or stealing data. For example, an adversary might use a remote access tool to run a PowerShell script that does Remote System Discovery.

> **Prowler config-check coverage (detective side):** AWS **1** checks tagged `TTPs/Execution` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1059](https://attack.mitre.org/techniques/T1059) | **Command and Scripting Interpreter** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1059.009](https://attack.mitre.org/techniques/T1059/009) | &nbsp;&nbsp;↳ Cloud API | IaaS, Identity Provider, Office Suite, SaaS |
| [T1072](https://attack.mitre.org/techniques/T1072) | **Software Deployment Tools** | SaaS |
| [T1204](https://attack.mitre.org/techniques/T1204) | **User Execution** | IaaS |
| [T1204.003](https://attack.mitre.org/techniques/T1204/003) | &nbsp;&nbsp;↳ Malicious Image | IaaS |
| [T1648](https://attack.mitre.org/techniques/T1648) | **Serverless Execution** | SaaS, IaaS, Office Suite |
| [T1651](https://attack.mitre.org/techniques/T1651) | **Cloud Administration Command** | IaaS |
| [T1677](https://attack.mitre.org/techniques/T1677) | **Poisoned Pipeline Execution** | SaaS |
| [T1698](https://attack.mitre.org/techniques/T1698) | **Indirect Prompt Injection** | SaaS |
| [T1699](https://attack.mitre.org/techniques/T1699) | **Direct Prompt Injection** | SaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
