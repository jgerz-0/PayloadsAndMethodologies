# Google Workspace Testing Methodology (ATT&CK-aligned)

> Offensive testing methodology for **Google Workspace** (Gmail, Drive, Admin
> Console / Directory, Groups, Marketplace), structured against the
> [cloud attack base](../_cloud-base/README.md). Workspace maps to ATT&CK's
> **Office Suite** / **SaaS** / **Identity Provider** platforms. Organized by
> kill-chain phase, with **positive (secure) vs negative (vulnerable)** evidence
> tied to **Prowler** check IDs (provider `googleworkspace`, 65 checks).

> **Authorization.** Test only your own tenant; phishing/spray against real users
> needs sign-off. Assume an **authorized** engagement.

## Workspace identity & surface
- **Super Admins** — the crown; **OUs** scope policy; delegated admin roles.
- **2-Step Verification (2SV)** — the MFA control; enforcement varies by OU.
- **OAuth apps & Marketplace** — third-party app access to Gmail/Drive (consent).
- **Domain-Wide Delegation (DWD)**  ⭐ — a **GCP service account** can be granted
  DWD to impersonate **any** Workspace user and read their mail/Drive. The
  signature Workspace↔GCP pivot (see [GCP](../gcp/README.md)).
- **Gmail / Drive** — mail and document stores; external sharing = exfil surface.

## Starting points
- **External:** public Google Groups, public Drive share links, user enumeration,
  OAuth consent phishing.
- **Assumed-breach:** a user session/token, or a GCP SA key **with DWD**.

## Tooling
- **GAM / GAMADV-XTD3** (admin CLI), **Google Admin SDK / Gmail / Drive APIs**,
  **gcloud** (for the SA/DWD pivot).
- **[Prowler](../../upstream/prowler/)** — `prowler googleworkspace` (65 checks).
- **GHunt** (account OSINT), **DeHashed**/cred reuse for spraying.

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
The DWD pivot crosses into **GCP** — test [GCP](../gcp/README.md) alongside.

## References
- [Cloud attack base](../_cloud-base/README.md) · [ATT&CK Cloud](https://attack.mitre.org/matrices/enterprise/cloud/)
- [HackTricks Cloud – Workspace/GCP](https://cloud.hacktricks.xyz/)
