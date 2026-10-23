# OCI · Phase 2 — Access & Credentials

> ATT&CK [TA0001 Initial Access](../_cloud-base/TA0001-initial-access.md) +
> [TA0006 Credential Access](../_cloud-base/TA0006-credential-access.md),
> projected onto OCI.

## Initial access
#### T1078.004 Valid Accounts: Cloud Accounts
- **Service/sink:** leaked API signing key (`~/.oci/config` with key + fingerprint
  + tenancy/user OCID), auth tokens, or console creds without MFA.
  ```sh
  oci iam user list --config-file ./found_config    # validate the key authenticates
  ```
- **Positive (secure):** key disabled; console MFA enforced
  (`identity_user_mfa_enabled_console_access`); admins have no API keys
  (`identity_tenancy_admin_users_no_api_keys`).
- **Negative (vulnerable):** key authenticates → foothold as that user.

## Credential access
#### T1552.005 Cloud Instance Metadata API  ⭐
- **Service/sink:** instance metadata on a compute VM using an **instance
  principal**.
  ```sh
  curl -H "Authorization: Bearer Oracle" http://169.254.169.254/opc/v2/instance/
  curl -H "Authorization: Bearer Oracle" http://169.254.169.254/opc/v2/identity/cert.pem
  ```
- **Positive (secure):** instance principal scoped by a tight dynamic-group +
  policy; metadata v2 (header-gated) reduces blind SSRF. Prowler
  `identity_instance_principal_used` (context — know where instance principals grant power).
- **Negative (vulnerable):** metadata yields instance-principal identity/certs →
  act with the dynamic group's policy grants. Classic SSRF→principal. Upstream
  [SSRF](../../upstream/PayloadsAllTheThings/Server%20Side%20Request%20Forgery/README.md).

#### T1552 Unsecured Credentials — Vault, secrets, config
- **Service/sink:** OCI Vault/KMS, instance metadata user-data, config files.
  ```sh
  oci vault secret list -c <compartment>
  oci secrets secret-bundle get --secret-id <ocid>
  ```
- **Positive (secure):** `NotAuthorizedOrNotFound`. **Negative:** secret bundle
  returned / plaintext creds in `user_data` → downstream access.

---
*Base: [Initial Access](../_cloud-base/TA0001-initial-access.md) ·
[Credential Access](../_cloud-base/TA0006-credential-access.md). Next:
[Phase 3 — Privilege Escalation](03-privilege-escalation.md).*
