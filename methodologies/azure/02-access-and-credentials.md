# Azure · Phase 2 — Access & Credentials

> ATT&CK [TA0001 Initial Access](../_cloud-base/TA0001-initial-access.md) +
> [TA0006 Credential Access](../_cloud-base/TA0006-credential-access.md),
> projected onto Azure + Entra ID.

## Initial access

#### T1078.004 Valid Accounts · T1110.003 Password Spraying
- **Service/sink:** Entra ID sign-in; leaked app secrets.
  ```sh
  az login -u <user> -p <pass>
  az login --service-principal -u <appId> -p <secret> --tenant <tid>
  # spraying (authorized): MicroBurst / MSOLSpray against the login endpoint
  ```
- **Positive (secure):** MFA + Conditional Access block the sign-in / legacy auth
  disabled; spraying locked out.
- **Negative (vulnerable):** creds authenticate with **no MFA** / legacy auth
  (IMAP/SMTP) path bypasses CA → foothold. Prowler
  `entra_policy_mfa_required_for_management_api`, `entra_security_defaults_enabled`.

## Credential access

#### T1552.005 Cloud Instance Metadata API (managed identity)  ⭐
- **Service/sink:** IMDS on a VM/Function with a managed identity.
  ```sh
  curl -H "Metadata:true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"
  ```
- **Positive (secure):** no managed identity assigned, or IMDS unreachable
  (SSRF-bounded). **Negative:** returns a bearer token for the VM's managed
  identity → act as that identity against ARM/Graph (its RBAC decides blast
  radius). Classic Azure SSRF→token. Upstream
  [SSRF](../../upstream/PayloadsAllTheThings/Server%20Side%20Request%20Forgery/README.md).

#### T1552 Unsecured Credentials — Key Vault, secrets, Automation
- **Service/sink:** Key Vault, VM run-command output, Automation accounts,
  deployment templates.
  ```sh
  az keyvault secret list --vault-name <v>
  az keyvault secret show --vault-name <v> --name <s>
  ```
- **Positive (secure):** `Forbidden` (RBAC/access-policy scoped); vault private
  endpoint only (`keyvault_access_only_through_private_endpoints`); secret
  expiry set (`keyvault_rbac_secret_expiration_set`).
- **Negative (vulnerable):** secret value returned → downstream creds. Public
  vault network access is the finding.

#### T1528 Steal Application Access Token · T1606.002 Forge SAML (Golden SAML)
Refresh/access tokens from token cache (`.azure`, browser), FOCI family token
abuse; Golden SAML if the AD FS token-signing key is compromised.

---
*Base: [Initial Access](../_cloud-base/TA0001-initial-access.md) ·
[Credential Access](../_cloud-base/TA0006-credential-access.md). Next:
[Phase 3 — Privilege Escalation](03-privilege-escalation.md).*
