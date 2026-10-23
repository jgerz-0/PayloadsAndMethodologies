# AWS · Phase 3 — Privilege Escalation

> ATT&CK [TA0004 Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md).
> Projected onto AWS IAM. Almost all AWS privesc is a **permission that lets you
> grant yourself more permissions** or **pass/assume a more privileged role**.

#### T1548 Abuse Elevation Control / T1098 Account Manipulation — IAM privesc paths
- **Service/sink:** IAM. The canonical [Rhino Security privesc paths](https://rhinosecuritylabs.com/aws/aws-privilege-escalation-methods-mitigation/).
- **How to test:** enumerate your effective permissions, then match to a path:
  ```sh
  pacu > run iam__privesc_scan            # automates detection + exploitation
  cloudfox aws permissions --profile p
  ```

| Permission you hold | Escalation |
|---|---|
| `iam:CreatePolicyVersion` | set a new **default** policy version granting `*:*` |
| `iam:AttachUserPolicy` / `AttachRolePolicy` | attach `AdministratorAccess` to self |
| `iam:PutUserPolicy` / `PutRolePolicy` | inline an admin policy |
| `iam:CreateAccessKey` (on another user) | mint keys for a privileged user |
| `iam:UpdateLoginProfile` | set a console password on a privileged user |
| `iam:PassRole` + `ec2:RunInstances` | launch EC2 with an admin role, read its creds via IMDS |
| `iam:PassRole` + `lambda:CreateFunction` + `lambda:InvokeFunction` | run code as an admin role |
| `sts:AssumeRole` on an over-trusting role | become that role |
| `glue`/`cloudformation`/`datapipeline` + `PassRole` | service proxies to an admin role |

- **How to test (example — CreatePolicyVersion):**
  ```sh
  aws iam create-policy-version --policy-arn <arn> \
    --policy-document file://admin.json --set-as-default
  ```
- **Positive (secure):** `AccessDenied` — no `iam:*` write; permission boundary
  caps effective perms. Prowler `iam_policy_allows_privilege_escalation`,
  `iam_aws_attached_policy_no_administrative_privileges`,
  `iam_inline_policy_no_administrative_privileges`.
- **Negative (vulnerable):** the write succeeds and a re-check
  (`aws iam list-attached-user-policies`) shows admin attached → you are now
  admin. `iam_policy_allows_privilege_escalation` flags the exact permission.

#### T1078 Valid Accounts — role chaining
- **Service/sink:** STS. A role whose trust policy lets your principal assume it:
  ```sh
  aws sts assume-role --role-arn <arn> --role-session-name x
  # export the returned ASIA… creds, repeat (chain)
  ```
- **Negative (vulnerable):** a role trusts `"AWS":"*"` or a broad principal and
  grants more than you have → assume it. Prowler
  `iam_role_cross_service_confused_deputy_prevention`,
  `iam_role_cross_account_readonlyaccess_policy`.

---
*Base: [Privilege Escalation](../_cloud-base/TA0004-privilege-escalation.md).
Next: [Phase 4 — Lateral Movement & Persistence](04-lateral-movement-and-persistence.md).*
