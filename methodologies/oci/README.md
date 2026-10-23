# OCI (Oracle Cloud Infrastructure) Testing Methodology (ATT&CK-aligned)

> Offensive testing methodology for **Oracle Cloud Infrastructure**, structured
> against the [cloud attack base](../_cloud-base/README.md) (MITRE ATT&CK cloud
> tactics + Prowler). Organized by **kill-chain phase**; ATT&CK techniques
> projected onto OCI services with the concrete API/sink, enumerate→attempt CLI,
> and **positive (secure, `NotAuthorizedOrNotFound`) vs negative (vulnerable,
> call succeeds)** evidence, tied to the **Prowler check ID** (provider
> `oraclecloud`, 52 checks).

> **Authorization.** OCI permits customer testing of your own tenancy per the
> [Oracle cloud testing policy](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_testing-policy.htm);
> assume an **authorized** engagement, prefer read/enumerate.

## OCI identity model (what you're attacking)

| Concept | Notes |
|---|---|
| Tenancy / **compartments** | hierarchical resource isolation; `root` compartment is the crown jewels |
| IAM users / groups | auth via console password or **API signing keys** (not passwords) |
| **Policies** | human-readable `Allow group <g> to <verb> <resource> in compartment <c>` |
| **Instance principals** / dynamic groups | compute gets creds via the **metadata service** (`169.254.169.254`) |
| Federation (IDCS / Entra) | SSO identities |

Authz = **IAM policy statements**. Danger: broad `Allow group X to manage
all-resources in tenancy`, policies at the root compartment, admin groups
without MFA. Attacker question: *what can this principal manage, and can it reach
a more privileged compartment or the root?*

## Starting points
- **External:** public Object Storage buckets, public compute IPs, exposed DBs.
- **Assumed-breach:** given an API key (`~/.oci/config`) or console creds. Start
  with `oci iam ...` enumeration.

## Tooling
- **oci CLI** — `oci <service> <action>`; config in `~/.oci/config` (key + fingerprint + tenancy OCID).
- **[Prowler](../../upstream/prowler/)** — `prowler oraclecloud` (52 checks); findings name the check ID.
- **ScoutSuite** (`scout oci`). OCI SDK scripting for bespoke enumeration.

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
Apps on OCI → [ASVS base](../_asvs-base/README.md). Shared concepts (IMDS→creds,
public storage, IAM privesc) mirror [AWS](../aws/README.md) — this page focuses
on OCI specifics.

## References
- [Cloud attack base](../_cloud-base/README.md) · [OCI security testing policy](https://docs.oracle.com/en-us/iaas/Content/Security/Concepts/security_testing-policy.htm)
- [HackTricks Cloud](https://cloud.hacktricks.xyz/)
