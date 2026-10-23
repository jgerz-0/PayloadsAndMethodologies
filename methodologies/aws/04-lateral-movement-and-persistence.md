# AWS · Phase 4 — Lateral Movement & Persistence

> ATT&CK [TA0008 Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) +
> [TA0003 Persistence](../_cloud-base/TA0003-persistence.md) +
> [TA0002 Execution](../_cloud-base/TA0002-execution.md). Projected onto AWS.

## Lateral movement

#### T1021 Remote Services / T1651 Cloud Administration Command (SSM)
- **Service/sink:** SSM Run Command — run commands on EC2 **without SSH** if you
  hold `ssm:SendCommand` and the instance has the SSM agent + a profile.
  ```sh
  aws ssm send-command --document-name AWS-RunShellScript \
    --targets Key=instanceIds,Values=<id> --parameters 'commands=["id"]'
  aws ssm start-session --target <id>        # interactive
  ```
- **Positive (secure):** `AccessDenied`; SSM scoped by tags/SCP.
- **Negative (vulnerable):** command runs as root on the instance → on-box creds,
  pivot. Prowler `ssm_managed_compliant_patching`, `ec2_instance_managed_by_ssm`
  (context).

#### T1078 Valid Accounts — cross-account AssumeRole
Chain into other accounts via trust relationships (see
[Phase 3](03-privilege-escalation.md)); enumerate org accounts with
`aws organizations list-accounts` if you land in the management account.

## Persistence

#### T1098 Account Manipulation
- **New access key for a user you control/compromised:**
  ```sh
  aws iam create-access-key --user-name <u>      # second key = quiet persistence
  ```
  Prowler `iam_user_two_active_access_key` flags the extra key.
- **Login profile / console password:** `aws iam create-login-profile`.
- **Backdoor a role trust policy** to add your external account as a trusted
  principal:
  ```sh
  aws iam update-assume-role-policy --role-name <r> --policy-document file://trust.json
  ```
  Negative: an unexpected external account in a trust policy → persistent
  cross-account access. Prowler `iam_role_cross_account_readonlyaccess_policy`.

#### T1136.003 Create Account: Cloud Account
`aws iam create-user` + attach admin — a standing backdoor principal.

#### T1546 Event Triggered Execution (Lambda/EventBridge backdoor)
A Lambda with an admin role triggered by an innocuous event, or a resource
policy allowing public invoke. Prowler `awslambda_function_not_publicly_accessible`,
`awslambda_function_no_secrets_in_code`.

---
*Base: [Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) ·
[Persistence](../_cloud-base/TA0003-persistence.md) ·
[Execution](../_cloud-base/TA0002-execution.md). Next:
[Phase 5 — Evasion](05-evasion.md).*
