# Azure · Phase 4 — Lateral Movement & Persistence

> ATT&CK [TA0008 Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) +
> [TA0003 Persistence](../_cloud-base/TA0003-persistence.md) +
> [TA0002 Execution](../_cloud-base/TA0002-execution.md), projected onto Azure.

## Lateral movement

#### T1021 Remote Services / T1651 Cloud Administration Command (Run Command)
- **Service/sink:** VM Run Command / Custom Script Extension — run code on a VM
  with just Contributor, no network access needed.
  ```sh
  az vm run-command invoke -g <rg> -n <vm> --command-id RunShellScript \
    --scripts "id"                                   # RunPowerShellScript on Windows
  ```
- **Positive (secure):** `AuthorizationFailed`; Run Command restricted by
  custom role / resource lock.
- **Negative (vulnerable):** command runs as root/SYSTEM → on-box secrets +
  managed-identity token ([Phase 2](02-access-and-credentials.md)).

#### T1078 — cross-subscription / cross-tenant
Use a managed-identity or SP token against other subscriptions where it holds
RBAC; B2B guest access and multi-tenant apps enable cross-tenant movement.

## Persistence

#### T1098 Account Manipulation
- **App/SP credential backdoor** (survives user password resets, often ignored):
  ```sh
  az ad app credential reset --id <appId> --append       # add an extra secret/cert
  ```
  Negative: an unexpected secret/cert on a privileged app registration. Prowler
  `entra_*` credential checks; review app credentials regularly.
- **Add owner to an app / privileged group**, or assign a directory role via PIM
  made permanent.

#### T1136.003 Create Account: Cloud Account
Create a new Entra user/guest or a service principal and grant it a role — a
standing backdoor identity.

#### T1546 Event Triggered Execution
A Function App / Logic App / Automation runbook with a managed identity,
triggered on a schedule or event. Prowler `app_ensure_auth_is_set_up`,
Function-related checks.

---
*Base: [Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) ·
[Persistence](../_cloud-base/TA0003-persistence.md) ·
[Execution](../_cloud-base/TA0002-execution.md). Next: [Phase 5 — Evasion](05-evasion.md).*
