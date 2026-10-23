# TA0040 – Impact (cloud)

> **MITRE ATT&CK v20.0 · tactic TA0040 Impact**, filtered to cloud platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, names, and the tactic definition are verbatim from ATT&CK.
>
> **Role in this repo:** framework-agnostic cloud base — the offensive sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) bases. When a provider methodology is generated (AWS/GCP/Azure; see [`_cloud-base/README.md`](README.md) and the `create-methodology` skill), each technique below is projected onto that provider: the concrete service/API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) vs negative (vulnerable) evidence** — cross-referenced to the Prowler config checks that detect the corresponding misconfiguration.

> **Tactic goal:** The adversary is trying to manipulate, interrupt, or destroy your systems and data.
 
Impact consists of techniques that adversaries use to disrupt availability or compromise integrity by manipulating business and operational processes. Techniques used for impact can include destroying or tampering with data. In some cases, business processes can look fine, but may have been altered to benefit the adversaries’ goals. These techniques might be used by adversaries to follow through on their end goal or to provide cover for a confidentiality breach.

> **Prowler config-check coverage (detective side):** AWS **0** checks tagged `TTPs/Impact` (Azure/GCP Prowler checks are service-tagged, not tactic-tagged — see per-provider pages).

## Techniques (cloud)

| ID | Technique | Cloud platforms |
| :-- | :-- | :-- |
| [T1485](https://attack.mitre.org/techniques/T1485) | **Data Destruction** | IaaS |
| [T1485.001](https://attack.mitre.org/techniques/T1485/001) | &nbsp;&nbsp;↳ Lifecycle-Triggered Deletion | IaaS |
| [T1486](https://attack.mitre.org/techniques/T1486) | **Data Encrypted for Impact** | IaaS |
| [T1489](https://attack.mitre.org/techniques/T1489) | **Service Stop** | IaaS |
| [T1490](https://attack.mitre.org/techniques/T1490) | **Inhibit System Recovery** | IaaS |
| [T1491](https://attack.mitre.org/techniques/T1491) | **Defacement** | IaaS |
| [T1491.002](https://attack.mitre.org/techniques/T1491/002) | &nbsp;&nbsp;↳ External Defacement | IaaS |
| [T1496](https://attack.mitre.org/techniques/T1496) | **Resource Hijacking** | IaaS, SaaS |
| [T1496.001](https://attack.mitre.org/techniques/T1496/001) | &nbsp;&nbsp;↳ Compute Hijacking | IaaS |
| [T1496.002](https://attack.mitre.org/techniques/T1496/002) | &nbsp;&nbsp;↳ Bandwidth Hijacking | IaaS |
| [T1496.003](https://attack.mitre.org/techniques/T1496/003) | &nbsp;&nbsp;↳ SMS Pumping | SaaS |
| [T1496.004](https://attack.mitre.org/techniques/T1496/004) | &nbsp;&nbsp;↳ Cloud Service Hijacking | SaaS |
| [T1498](https://attack.mitre.org/techniques/T1498) | **Network Denial of Service** | IaaS |
| [T1498.001](https://attack.mitre.org/techniques/T1498/001) | &nbsp;&nbsp;↳ Direct Network Flood | IaaS |
| [T1498.002](https://attack.mitre.org/techniques/T1498/002) | &nbsp;&nbsp;↳ Reflection Amplification | IaaS |
| [T1499](https://attack.mitre.org/techniques/T1499) | **Endpoint Denial of Service** | IaaS |
| [T1499.002](https://attack.mitre.org/techniques/T1499/002) | &nbsp;&nbsp;↳ Service Exhaustion Flood | IaaS |
| [T1499.003](https://attack.mitre.org/techniques/T1499/003) | &nbsp;&nbsp;↳ Application Exhaustion Flood | IaaS |
| [T1499.004](https://attack.mitre.org/techniques/T1499/004) | &nbsp;&nbsp;↳ Application or System Exploitation | IaaS |
| [T1531](https://attack.mitre.org/techniques/T1531) | **Account Access Removal** | SaaS, IaaS, Office Suite |
| [T1657](https://attack.mitre.org/techniques/T1657) | **Financial Theft** | Office Suite, SaaS |
| [T1667](https://attack.mitre.org/techniques/T1667) | **Email Bombing** | Office Suite |

---

### Provider projection (filled per provider, not here)

This base page lists *what* an attacker does in this tactic against cloud. A provider methodology projects each relevant technique onto AWS / GCP / Azure with:

- **Service / sink** — the concrete service, API, or resource (e.g. IAM, STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).
- **How to test** — enumerate then attempt; the CLI/API call or tool (awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.
- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.
- **Negative evidence (vulnerable)** — the call succeeds / data returned — the confirmation signal, plus the Prowler check ID that flags it.
