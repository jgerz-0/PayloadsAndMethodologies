# TA0004 – Privilege Escalation (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0004 Privilege Escalation**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to gain higher-level permissions.

Privilege Escalation consists of techniques that adversaries use to gain higher-level permissions on a system or network. Adversaries can often enter and explore a network with unprivileged access but require elevated permissions to follow through on their objectives. Common approaches are to take advantage of system weaknesses, misconfigurations, and vulnerabilities. Examples of elevated access include: 

* SYSTEM/root level
* local administrator
* user account with admin-like access 
* user accounts with access to specific system or perform specific function

These techniques often overlap with Persistence techniques, as OS features that let an adversary persist can execute in an elevated context.

> **Prowler config-check coverage (detective side):** AWS **25** checks tagged `TTPs/Privilege Escalation` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

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
| [T1484](https://attack.mitre.org/techniques/T1484) | **Domain or Tenant Policy Modification** | Identity Provider |
| [T1484.002](https://attack.mitre.org/techniques/T1484/002) | &nbsp;&nbsp;↳ Trust Modification | Identity Provider |
| [T1546](https://attack.mitre.org/techniques/T1546) | **Event Triggered Execution** | SaaS, IaaS, Office Suite |
| [T1548](https://attack.mitre.org/techniques/T1548) | **Abuse Elevation Control Mechanism** | IaaS, Office Suite, Identity Provider |
| [T1548.005](https://attack.mitre.org/techniques/T1548/005) | &nbsp;&nbsp;↳ Temporary Elevated Cloud Access | IaaS, Office Suite, Identity Provider |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
