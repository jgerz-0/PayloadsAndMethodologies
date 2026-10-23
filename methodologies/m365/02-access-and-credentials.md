# M365 · Phase 2 — Access & Credentials

> ATT&CK [TA0001 Initial Access](../_cloud-base/TA0001-initial-access.md) +
> [TA0006 Credential Access](../_cloud-base/TA0006-credential-access.md),
> projected onto M365.

## Initial access
#### T1110.003 Password Spraying · T1078.004 Valid Accounts
- **Service/sink:** Entra sign-in; legacy auth endpoints (EWS/IMAP/POP/SMTP,
  Autodiscover) that **bypass Conditional Access/MFA**.
  ```
  MailSniper / MSOLSpray / TokenTactics against the login endpoint
  ```
- **Positive (secure):** MFA + CA for all apps/users; legacy auth blocked;
  smart-lockout. Prowler `entra_conditional_access_policy_all_apps_all_users`,
  `entra_admin_users_mfa_enabled`, `entra_admin_users_phishing_resistant_mfa_enabled`.
- **Negative (vulnerable):** creds work with **no MFA** or via legacy-auth path →
  foothold. Legacy-auth bypass of CA is a top finding.

#### T1566 Phishing → T1528 Steal Application Access Token (illicit consent)  ⭐
- **Service/sink:** OAuth consent. An attacker app requests Graph scopes
  (`Mail.Read`, `Files.ReadWrite.All`, `offline_access`); a user consents.
- **Positive (secure):** user consent disabled / admin-consent-workflow required
  (`entra_admin_consent_workflow_enabled`); only verified publishers.
- **Negative (vulnerable):** user can consent to any app → attacker gets a refresh
  token reading mail/files **without a password** (survives password reset).
  GraphRunner demonstrates it.

## Credential access
#### T1552 Unsecured Credentials / T1114 (prep)
- Secrets in SharePoint/OneDrive docs, Teams messages, mailbox; app registration
  client secrets/certs:
  ```powershell
  Get-MgApplication -All | % { Get-MgApplicationPassword -ApplicationId $_.Id }
  ```
- **Negative (vulnerable):** long-lived app secret recovered → sign in as the SP
  ([Phase 3](03-privilege-escalation.md)). Prowler `entra_app_registration_*`.

#### T1606.002 Forge SAML (Golden SAML) · T1556.007 Hybrid Identity
On-prem AD FS token-signing key or AADConnect/PTA agent compromise → forge
federated tokens / sync backdoors (AADInternals).

---
*Base: [Initial Access](../_cloud-base/TA0001-initial-access.md) ·
[Credential Access](../_cloud-base/TA0006-credential-access.md). Next:
[Phase 3 — Privilege Escalation](03-privilege-escalation.md).*
