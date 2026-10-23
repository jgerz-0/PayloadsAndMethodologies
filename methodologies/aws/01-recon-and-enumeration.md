# AWS · Phase 1 — Recon & Enumeration

> ATT&CK [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) (+ external
> attack-surface recon). Projected onto AWS. Goal: know *who you are*, *what you
> can do*, and *what is public* before touching anything.

## Who am I / what can I do

#### T1087 Account Discovery · T1526 Cloud Service Discovery
- **Service/sink:** STS, IAM.
- **How to test:**
  ```sh
  aws sts get-caller-identity                       # your principal ARN + account id
  aws iam get-account-authorization-details         # whole IAM graph (if allowed)
  cloudfox aws --profile p all-checks               # attacker view of permissions
  # no iam:Get*? brute your effective perms:
  pacu > run iam__enum_permissions ; enumerate-iam --access-key ... --secret-key ...
  ```
- **Positive (secure):** scoped principal, `iam:Get*/List*` denied → you must
  infer permissions by probing.
- **Negative (vulnerable):** `get-account-authorization-details` returns the full
  policy graph → you map every privesc path offline. Over-broad read is flagged
  around `iam_aws_attached_policy_no_administrative_privileges`.

#### Region / service enumeration
```sh
aws ec2 describe-regions --query 'Regions[].RegionName' --output text
for r in $(…); do aws ec2 describe-instances --region $r; done   # sweep regions
```
Attackers hide resources in unused regions — sweep all, not just the default.

## Public / unauthenticated attack surface (no creds needed)

#### T1580 Cloud Infrastructure Discovery · T1526 — external
- **S3 buckets:** guess/resolve bucket names; `aws s3 ls s3://<name> --no-sign-request`.
  - Negative: listing/objects returned unauthenticated → **public bucket**.
    Prowler `s3_bucket_public_access`, `s3_bucket_policy_public_write_access`.
- **Public EBS snapshots / AMIs:**
  ```sh
  aws ec2 describe-snapshots --restorable-by-user-ids all --owner-ids <acct> --region r
  aws ec2 describe-images --executable-users all --owners <acct>
  ```
  Negative: snapshots/AMIs shared with `all` → mount to read data. Prowler
  `ec2_ebs_public_snapshot`, `ec2_ami_public`.
- **ECR, RDS snapshots, OpenSearch, API Gateway, CloudFront** — check public
  policies/endpoints. Prowler `ecr_repositories_not_publicly_accessible`,
  `rds_snapshots_public_access`.

## Enumerate principals & trust (set up privesc)

```sh
aws iam list-users ; aws iam list-roles                 # principals
aws iam list-attached-user-policies --user-name <u>
aws iam get-role --role-name <r>                        # trust policy
```
Look for role **trust policies** with loose `Principal` (`"AWS":"*"`, another
account, or a role you control) → an assumable foothold (see
[Phase 3/4](03-privilege-escalation.md)).

---
*Base: [TA0007 Discovery](../_cloud-base/TA0007-discovery.md). Next:
[Phase 2 — Access & Credentials](02-access-and-credentials.md).*
