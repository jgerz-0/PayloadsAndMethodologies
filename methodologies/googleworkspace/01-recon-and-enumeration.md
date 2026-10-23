# Google Workspace · Phase 1 — Recon & Enumeration

> ATT&CK [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) + external recon,
> projected onto Google Workspace.

## Unauthenticated recon
#### T1590/T1589 — external
- **Public Google Groups:** `groups.google.com/a/<domain>` — publicly listable
  groups/messages leak names, emails, sometimes credentials/internal threads.
- **Public Drive links:** "anyone with the link" documents indexed/guessable.
- **Account OSINT:** GHunt against a Google account (services, photos, reviews).
- **User format:** infer `first.last@domain` from OSINT for spraying.

## Authenticated directory enumeration
#### T1087 Account Discovery · T1526 Cloud Service Discovery
```sh
gam print users ; gam print groups
gam print admins                         # super admins + delegated admin roles
gam print tokens                         # OAuth tokens/apps authorized by users
gam all users print filters              # Gmail filters (forwarding → exfil)
```
- **Positive (secure):** few super admins (`directory_super_admin_count`,
  `directory_super_admin_only_admin_roles`); member directory access limited.
- **Negative (vulnerable):** many super admins, broad directory visibility →
  map admin targets and risky OAuth grants.

## Surface: OAuth apps, DWD, sharing
```sh
gam print tokens                         # third-party app scopes per user
# Domain-Wide Delegation clients (Admin console > API controls) — GCP SAs that can impersonate users
```
- **Negative (vulnerable):** an OAuth app with broad Gmail/Drive scopes, or a
  **DWD** client ID with `https://mail.google.com/` scope → tenant-wide
  impersonation ([Phase 3](03-privilege-escalation.md)).

---
*Base: [TA0007 Discovery](../_cloud-base/TA0007-discovery.md). Next:
[Phase 2 — Access & Credentials](02-access-and-credentials.md).*
