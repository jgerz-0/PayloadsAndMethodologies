# TA0006 – Credential Access (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0006 Credential Access**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to steal account names and passwords.

Credential Access consists of techniques for stealing credentials like account names and passwords. Techniques used to get credentials include keylogging or credential dumping. Using legitimate credentials can give adversaries access to systems, make them harder to detect, and provide the opportunity to create more accounts to help achieve their goals.

> **Prowler config-check coverage (detective side):** AWS **39** checks tagged `TTPs/Credential Access` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1040](https://attack.mitre.org/techniques/T1040) | **Network Sniffing** | IaaS |
| [T1110](https://attack.mitre.org/techniques/T1110) | **Brute Force** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1110.001](https://attack.mitre.org/techniques/T1110/001) | &nbsp;&nbsp;↳ Password Guessing | IaaS, Identity Provider, Office Suite, SaaS |
| [T1110.002](https://attack.mitre.org/techniques/T1110/002) | &nbsp;&nbsp;↳ Password Cracking | Identity Provider, Office Suite |
| [T1110.003](https://attack.mitre.org/techniques/T1110/003) | &nbsp;&nbsp;↳ Password Spraying | IaaS, Identity Provider, Office Suite, SaaS |
| [T1110.004](https://attack.mitre.org/techniques/T1110/004) | &nbsp;&nbsp;↳ Credential Stuffing | IaaS, Identity Provider, Office Suite, SaaS |
| [T1212](https://attack.mitre.org/techniques/T1212) | **Exploitation for Credential Access** | Identity Provider |
| [T1528](https://attack.mitre.org/techniques/T1528) | **Steal Application Access Token** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1539](https://attack.mitre.org/techniques/T1539) | **Steal Web Session Cookie** | Office Suite, SaaS |
| [T1552](https://attack.mitre.org/techniques/T1552) | **Unsecured Credentials** | SaaS, IaaS, Office Suite, Identity Provider |
| [T1552.001](https://attack.mitre.org/techniques/T1552/001) | &nbsp;&nbsp;↳ Credentials In Files | IaaS |
| [T1552.005](https://attack.mitre.org/techniques/T1552/005) | &nbsp;&nbsp;↳ Cloud Instance Metadata API | IaaS |
| [T1552.008](https://attack.mitre.org/techniques/T1552/008) | &nbsp;&nbsp;↳ Chat Messages | SaaS, Office Suite |
| [T1555](https://attack.mitre.org/techniques/T1555) | **Credentials from Password Stores** | IaaS |
| [T1555.006](https://attack.mitre.org/techniques/T1555/006) | &nbsp;&nbsp;↳ Cloud Secrets Management Stores | IaaS |
| [T1556](https://attack.mitre.org/techniques/T1556) | **Modify Authentication Process** | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.006](https://attack.mitre.org/techniques/T1556/006) | &nbsp;&nbsp;↳ Multi-Factor Authentication | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.007](https://attack.mitre.org/techniques/T1556/007) | &nbsp;&nbsp;↳ Hybrid Identity | IaaS, Identity Provider, Office Suite, SaaS |
| [T1556.009](https://attack.mitre.org/techniques/T1556/009) | &nbsp;&nbsp;↳ Conditional Access Policies | IaaS, Identity Provider |
| [T1606](https://attack.mitre.org/techniques/T1606) | **Forge Web Credentials** | SaaS, IaaS, Office Suite, Identity Provider |
| [T1606.001](https://attack.mitre.org/techniques/T1606/001) | &nbsp;&nbsp;↳ Web Cookies | SaaS, IaaS |
| [T1606.002](https://attack.mitre.org/techniques/T1606/002) | &nbsp;&nbsp;↳ SAML Tokens | SaaS, IaaS, Office Suite, Identity Provider |
| [T1621](https://attack.mitre.org/techniques/T1621) | **Multi-Factor Authentication Request Generation** | IaaS, SaaS, Office Suite, Identity Provider |
| [T1649](https://attack.mitre.org/techniques/T1649) | **Steal or Forge Authentication Certificates** | Identity Provider |
| [T1697](https://attack.mitre.org/techniques/T1697) | **Steal Application Specific Passwords** | Office Suite, Identity Provider, SaaS |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
