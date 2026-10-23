# Google Workspace · Phase 5 — Evasion

> ATT&CK [TA0005 Stealth](../_cloud-base/TA0005-stealth.md) +
> [TA0112 Defense Impairment](../_cloud-base/TA0112-defense-impairment.md),
> projected onto Workspace. **Confirm non-destructively where possible.**

#### T1562.008 Disable or Modify Cloud Logs
- **Service/sink:** Admin audit / login / Drive / Gmail logs (Reports API),
  investigation tool, log export to BigQuery.
  ```sh
  gam report admin ; gam report login       # read audit events
  ```
- **Positive (secure):** audit logs exported to BigQuery/SIEM (tamper-resistant),
  alerts on admin changes. **Negative:** disabling log export / rules → telemetry
  gaps. (Read config to confirm; don't disable in prod.)

#### T1564.008 Email Hiding Rules
Gmail filters that archive/delete Google security alerts ("new sign-in",
"less-secure app") to hide compromise. Audit `gam all users print filters` for
delete/skip-inbox rules on security senders.

#### T1562.001 Disable Security Tools
Weakening 2SV enforcement for an OU, disabling advanced phishing/malware
protection, or relaxing Marketplace restrictions. Prowler
`gmail_domain_spoofing_protection_enabled` and related Gmail-protection checks
flag weakened posture.

#### T1550 Use Alternate Authentication Material
Stolen OAuth refresh tokens / app passwords reused to avoid re-auth + 2SV —
valid-token access evades login alerts.

---
*Base: [Stealth](../_cloud-base/TA0005-stealth.md) ·
[Defense Impairment](../_cloud-base/TA0112-defense-impairment.md). Next:
[Phase 6 — Collection, Exfil & Impact](06-collection-exfil-impact.md).*
