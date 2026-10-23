# Google Workspace · Phase 2 — Access & Credentials

> ATT&CK [TA0001 Initial Access](../_cloud-base/TA0001-initial-access.md) +
> [TA0006 Credential Access](../_cloud-base/TA0006-credential-access.md),
> projected onto Google Workspace.

## Initial access
#### T1110.003 Password Spraying · T1078.004 Valid Accounts
- **Service/sink:** Google sign-in; **legacy/less-secure app** access and app
  passwords that bypass 2SV.
- **Positive (secure):** 2SV enforced per-OU (ideally security keys); less-secure
  apps disabled; no app passwords.
- **Negative (vulnerable):** creds work with **no 2SV**, or an app password / IMAP
  path bypasses 2SV → foothold.

#### T1566 Phishing → T1528 Steal Application Access Token (OAuth consent)  ⭐
- **Service/sink:** OAuth consent to a third-party app requesting Gmail/Drive
  scopes (`https://mail.google.com/`, `drive`).
- **Positive (secure):** app access restricted to allowlisted/verified apps;
  internal-only, admin-approved Marketplace.
- **Negative (vulnerable):** users can grant any app → attacker app gets a refresh
  token reading mail/Drive without a password.

## Credential access
#### T1552.005 Metadata (DWD pivot via GCP) · T1552 Unsecured Credentials
- **Service/sink:** a **GCP service account key with Domain-Wide Delegation**.
  With it you mint a user-impersonating token:
  ```python
  # SA JSON + DWD + scope https://mail.google.com/  -> impersonate any user
  creds = service_account.Credentials.from_service_account_file("sa.json",
            scopes=["https://mail.google.com/"], subject="ceo@target.com")
  ```
- **Positive (secure):** no SA has DWD, or DWD scopes are minimal and SA keys
  disabled (GCP `iam_sa_no_user_managed_keys`).
- **Negative (vulnerable):** a DWD SA key → read **any** user's mail/Drive
  tenant-wide. The signature Workspace↔GCP compromise.
- Secrets also live in Drive docs, Gmail, Apps Script projects.

---
*Base: [Initial Access](../_cloud-base/TA0001-initial-access.md) ·
[Credential Access](../_cloud-base/TA0006-credential-access.md). Next:
[Phase 3 — Privilege Escalation](03-privilege-escalation.md).*
