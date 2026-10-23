# TA0005 – Stealth (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0005 Stealth**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to hide and conceal their actions, appearing as normal behavior.

Stealth consists of techniques that reduce the likelihood of detection by blending in with legitimate activity or minimizing observable signals. These techniques are characterized by concealment behaviors, such as avoiding, obfuscating, or mimicking normal operations, without modifying security controls or compromising collection and monitoring feeds. The goal is to remain indistinguishable from benign activity while leaving defensive systems intact.

> **Prowler config-check coverage (detective side):** AWS **16** checks tagged `TTPs/Stealth` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1070](https://attack.mitre.org/techniques/T1070) | **Indicator Removal** | Office Suite |
| [T1070.008](https://attack.mitre.org/techniques/T1070/008) | &nbsp;&nbsp;↳ Clear Mailbox Data | Office Suite |
| [T1078](https://attack.mitre.org/techniques/T1078) | **Valid Accounts** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1078.001](https://attack.mitre.org/techniques/T1078/001) | &nbsp;&nbsp;↳ Default Accounts | IaaS, Identity Provider, Office Suite, SaaS |
| [T1078.004](https://attack.mitre.org/techniques/T1078/004) | &nbsp;&nbsp;↳ Cloud Accounts | IaaS, Identity Provider, Office Suite, SaaS |
| [T1211](https://attack.mitre.org/techniques/T1211) | **Exploitation for Stealth** | SaaS, IaaS |
| [T1535](https://attack.mitre.org/techniques/T1535) | **Unused/Unsupported Cloud Regions** | IaaS |
| [T1564](https://attack.mitre.org/techniques/T1564) | **Hide Artifacts** | Office Suite |
| [T1564.008](https://attack.mitre.org/techniques/T1564/008) | &nbsp;&nbsp;↳ Email Hiding Rules | Office Suite |
| [T1684](https://attack.mitre.org/techniques/T1684) | **Social Engineering** | Office Suite, SaaS |
| [T1684.001](https://attack.mitre.org/techniques/T1684/001) | &nbsp;&nbsp;↳ Impersonation | Office Suite, SaaS |
| [T1684.002](https://attack.mitre.org/techniques/T1684/002) | &nbsp;&nbsp;↳ Email Spoofing | Office Suite |
| [T1696](https://attack.mitre.org/techniques/T1696) | **Anti-Automation Evasion** | SaaS |
| [T1696.001](https://attack.mitre.org/techniques/T1696/001) | &nbsp;&nbsp;↳ Automate CAPTCHA Completion | SaaS |
| [T1696.002](https://attack.mitre.org/techniques/T1696/002) | &nbsp;&nbsp;↳ Avoid CAPTCHA | SaaS |
| [T1036.010](https://attack.mitre.org/techniques/T1036/010) | ↳ Masquerade Account Name | IaaS, Identity Provider, Office Suite, SaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
