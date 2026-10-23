# Microsoft 365 Testing Methodology (ATT&CK-aligned)

> Offensive testing methodology for **Microsoft 365** (Exchange Online,
> SharePoint/OneDrive, Teams, Entra ID), structured against the
> [cloud attack base](../_cloud-base/README.md). M365 maps to ATT&CK's
> **Office Suite** + **Identity Provider** platforms. Organized by kill-chain
> phase; techniques projected onto M365 services with CLI/PowerShell, and
> **positive (secure) vs negative (vulnerable)** evidence, tied to **Prowler**
> check IDs (provider `m365`, 149 checks).

> **Authorization.** Test only your own tenant; assume an **authorized**
> engagement. Phishing/spray against real users needs explicit sign-off.

## M365 identity & surface
- **Entra ID** is the identity plane (shared with [Azure](../azure/README.md) —
  directory-role escalation, app consent, service principals, Conditional Access
  all apply here). This page focuses on the **productivity services**.
- **Exchange Online** — mailboxes, transport rules, mail-forwarding (exfil).
- **SharePoint / OneDrive** — document stores, external sharing.
- **Teams** — chat/files, external access/federation.
- **Tokens** — OAuth access/refresh tokens; **illicit app consent** is the
  signature M365 attack (an attacker app granted Graph scopes to read mail/files).

## Starting points
- **External:** tenant recon (does the tenant exist, federation type, user
  enumeration), password spraying, phishing/consent grants.
- **Assumed-breach:** a user token/creds or an app registration secret.

## Tooling
- **Microsoft Graph PowerShell** (`Connect-MgGraph`), **ExchangeOnlineManagement**,
  **az cli** / **Microsoft Graph API**.
- **[Prowler](../../upstream/prowler/)** — `prowler m365` (149 checks).
- **[ROADtools](https://github.com/dirkjanm/ROADtools)** / **AADInternals** /
  **GraphRunner** / **o365creeper** (user enum) / **MFASweep** / **TokenTactics**.

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
Entra/Azure RBAC escalation → [Azure methodology](../azure/README.md). This page
and Azure's share the Entra plane; test them together for a tenant.

## References
- [Cloud attack base](../_cloud-base/README.md) · [ATT&CK Cloud](https://attack.mitre.org/matrices/enterprise/cloud/)
- [Microsoft pentest RoE](https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement) · [HackTricks Cloud – Azure/M365](https://cloud.hacktricks.xyz/)
