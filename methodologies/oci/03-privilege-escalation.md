# OCI · Phase 3 — Privilege Escalation

> ATT&CK [TA0004 Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md),
> projected onto OCI IAM. OCI privesc = **editing IAM policies**, **adding
> credentials to a privileged user**, or **abusing group membership / dynamic
> groups**.

#### T1548 Abuse Elevation Control / T1098 Account Manipulation — OCI privesc paths

| Permission you hold | Escalation |
|---|---|
| `manage policies` (in tenancy/compartment) | write `Allow group <mine> to manage all-resources in tenancy` |
| `use users` / `manage users` | add an **API key** or **auth token** to a privileged user |
| `manage groups` | add yourself to an admin group |
| `manage dynamic-groups` + `manage policies` | craft a dynamic group matching a VM you control, grant it admin, read its instance-principal token |

- **How to test (policy write):**
  ```sh
  oci iam policy create -c <tenancy> --name esc \
    --statements '["Allow group myteam to manage all-resources in tenancy"]' \
    --description x
  oci iam user api-key upload --user-id <priv-user> --key-file pub.pem   # cred-add path
  ```
- **Positive (secure):** `NotAuthorizedOrNotFound`; no `manage policies`/`users`/
  `groups`; admin policies confined to root with MFA
  (`identity_iam_admins_cannot_update_tenancy_admins`, `identity_service_level_admins_exist`).
- **Negative (vulnerable):** policy/key-add/group-add succeeds and a re-check
  (`oci iam policy list`) shows elevated grants → you now manage the tenancy.

---
*Base: [Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md).
Next: [Phase 4 — Lateral Movement & Persistence](04-lateral-movement-and-persistence.md).*
