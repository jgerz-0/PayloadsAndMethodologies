# TA0003 – Persistence (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0003 Persistence**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to maintain their foothold.

Persistence consists of techniques that adversaries use to keep access to systems across restarts, changed credentials, and other interruptions that could cut off their access. Techniques used for persistence include any access, action, or configuration changes that let them maintain their foothold on systems, such as replacing or hijacking legitimate code or adding startup code.

> **Prowler config-check coverage (detective side):** AWS **1** checks tagged `TTPs/Persistence` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1078](https://attack.mitre.org/techniques/T1078) | **Valid Accounts** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1078.001](https://attack.mitre.org/techniques/T1078/001) | &nbsp;&nbsp;↳ Default Accounts | IaaS, Identity Provider, Office Suite, SaaS |
| [T1078.004](https://attack.mitre.org/techniques/T1078/004) | &nbsp;&nbsp;↳ Cloud Accounts | IaaS, Identity Provider, Office Suite, SaaS |
| [T1098](https://attack.mitre.org/techniques/T1098) | **Account Manipulation** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1098.001](https://attack.mitre.org/techniques/T1098/001) | &nbsp;&nbsp;↳ Additional Cloud Credentials | IaaS, Identity Provider, SaaS |
| [T1098.002](https://attack.mitre.org/techniques/T1098/002) | &nbsp;&nbsp;↳ Additional Email Delegate Permissions | Office Suite |
| [T1098.003](https://attack.mitre.org/techniques/T1098/003) | &nbsp;&nbsp;↳ Additional Cloud Roles | IaaS, Identity Provider, Office Suite, SaaS |
| [T1098.004](https://attack.mitre.org/techniques/T1098/004) | &nbsp;&nbsp;↳ SSH Authorized Keys | IaaS |
| [T1098.005](https://attack.mitre.org/techniques/T1098/005) | &nbsp;&nbsp;↳ Device Registration | Identity Provider |
| [T1136](https://attack.mitre.org/techniques/T1136) | **Create Account** | IaaS, SaaS, Office Suite, Identity Provider |
| [T1136.003](https://attack.mitre.org/techniques/T1136/003) | &nbsp;&nbsp;↳ Cloud Account | IaaS, SaaS, Office Suite, Identity Provider |
| [T1137](https://attack.mitre.org/techniques/T1137) | **Office Application Startup** | Office Suite |
| [T1137.001](https://attack.mitre.org/techniques/T1137/001) | &nbsp;&nbsp;↳ Office Template Macros | Office Suite |
| [T1137.002](https://attack.mitre.org/techniques/T1137/002) | &nbsp;&nbsp;↳ Office Test | Office Suite |
| [T1137.003](https://attack.mitre.org/techniques/T1137/003) | &nbsp;&nbsp;↳ Outlook Forms | Office Suite |
| [T1137.004](https://attack.mitre.org/techniques/T1137/004) | &nbsp;&nbsp;↳ Outlook Home Page | Office Suite |
| [T1137.005](https://attack.mitre.org/techniques/T1137/005) | &nbsp;&nbsp;↳ Outlook Rules | Office Suite |
| [T1137.006](https://attack.mitre.org/techniques/T1137/006) | &nbsp;&nbsp;↳ Add-ins | Office Suite |
| [T1525](https://attack.mitre.org/techniques/T1525) | **Implant Internal Image** | IaaS |
| [T1546](https://attack.mitre.org/techniques/T1546) | **Event Triggered Execution** | SaaS, IaaS, Office Suite |
| [T1556](https://attack.mitre.org/techniques/T1556) | **Modify Authentication Process** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.006](https://attack.mitre.org/techniques/T1556/006) | &nbsp;&nbsp;↳ Multi-Factor Authentication | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.007](https://attack.mitre.org/techniques/T1556/007) | &nbsp;&nbsp;↳ Hybrid Identity | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.009](https://attack.mitre.org/techniques/T1556/009) | &nbsp;&nbsp;↳ Conditional Access Policies | IaaS, Identity Provider |
| [T1671](https://attack.mitre.org/techniques/T1671) | **Cloud Application Integration** | Office Suite, SaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
