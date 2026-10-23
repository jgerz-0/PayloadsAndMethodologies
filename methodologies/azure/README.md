# Azure Cloud Testing Methodology (ATT&CK-aligned)

> Offensive testing methodology for **Microsoft Azure + Entra ID**, structured
> against the [cloud attack base](../_cloud-base/README.md) (MITRE ATT&CK +
> Prowler). Organized by **kill-chain phase**; ATT&CK techniques projected onto
> Azure services with the concrete API/sink, enumerate→attempt CLI, and
> **positive (secure, `AuthorizationFailed`) vs negative (vulnerable, call
> succeeds)** evidence, each tied to the **Prowler check ID**.

> **Authorization.** Microsoft's
> [pentest rules of engagement](https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement)
> permit testing your own tenants/resources (no prior approval) but forbid DoS
> and testing shared infra. Assume an **authorized** engagement; prefer
> read/enumerate.

## Azure identity model (what you're attacking)

Two **distinct** authorization planes — test both:

| Plane | Roles | Scope |
|---|---|---|
| **Azure RBAC** (resource mgmt) | Owner, Contributor, **User Access Administrator** | mgmt group → subscription → resource group → resource |
| **Entra ID** (directory) | Global Admin, Privileged Role Admin, Application Admin | the tenant/directory |

| Principal | Credential |
|---|---|
| Entra user | password (+ MFA / Conditional Access) |
| **Service principal** / app registration | client secret or certificate |
| **Managed identity** (VM/Function/etc.) | token via **IMDS** (`169.254.169.254`) |

The two planes diverge: a user can be **Owner** on every subscription yet have no
Entra role, or **Global Admin** yet (by default) no resource access until they
elevate. Attackers pivot *between* the planes.

## Starting points
- **External:** tenant recon (federation, user enumeration), public blob
  containers, public endpoints, leaked app secrets.
- **Assumed-breach:** a user or service-principal credential. `az login` /
  `az login --service-principal`, then enumerate role assignments.

## Tooling
- **az cli** — `az <svc> ...`; `az login --service-principal -u <appId> -p <secret> --tenant <t>`.
- **[Prowler](../../upstream/prowler/)** — `prowler azure` (200 checks); findings name the check ID.
- **[ROADtools](https://github.com/dirkjanm/ROADtools)** (`roadrecon`) — Entra ID enumeration.
- **[AzureHound](https://github.com/BloodHoundAD/AzureHound)** / BloodHound — attack-path graphing across both planes.
- **[MicroBurst](https://github.com/NetSPI/MicroBurst)**, **[Stormspotter](https://github.com/Azure/Stormspotter)**, **ScoutSuite** (`scout azure`).

## Phases → ATT&CK tactics

| Phase | Page | ATT&CK tactic(s) |
|---|---|---|
| Recon & enumeration | [01](01-recon-and-enumeration.md) | [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) |
| Access & credentials | [02](02-access-and-credentials.md) | [TA0001](../_cloud-base/TA0001-initial-access.md) · [TA0006](../_cloud-base/TA0006-credential-access.md) |
| Privilege escalation | [03](03-privilege-escalation.md) | [TA0004](../_cloud-base/TA0004-privilege-escalation.md) |
| Lateral movement & persistence | [04](04-lateral-movement-and-persistence.md) | [TA0008](../_cloud-base/TA0008-lateral-movement.md) · [TA0003](../_cloud-base/TA0003-persistence.md) · [TA0002](../_cloud-base/TA0002-execution.md) |
| Evasion | [05](05-evasion.md) | [TA0005](../_cloud-base/TA0005-stealth.md) · [TA0112](../_cloud-base/TA0112-defense-impairment.md) |
| Collection, exfil & impact | [06](06-collection-exfil-impact.md) | [TA0009](../_cloud-base/TA0009-collection.md) · [TA0010](../_cloud-base/TA0010-exfiltration.md) · [TA0040](../_cloud-base/TA0040-impact.md) |

## Adjacent scope
Apps on Azure → [ASVS base](../_asvs-base/README.md). AKS → Kubernetes (Prowler
`kubernetes`). M365/Entra identity attacks overlap with the Entra sections here.

## References
- [Cloud attack base](../_cloud-base/README.md) · [ATT&CK Cloud](https://attack.mitre.org/matrices/enterprise/cloud/)
- [Microsoft pentest RoE](https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement) · [HackTricks Cloud – Azure](https://cloud.hacktricks.xyz/)
