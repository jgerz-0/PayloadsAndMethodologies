# OCI · Phase 1 — Recon & Enumeration

> ATT&CK [TA0007 Discovery](../_cloud-base/TA0007-discovery.md) + external recon,
> projected onto OCI.

## Who am I / what can I do
#### T1087 Account Discovery · T1526 Cloud Service Discovery
```sh
oci iam region list
oci iam compartment list --compartment-id-in-subtree true --all   # the compartment tree
oci iam user list ; oci iam group list ; oci iam policy list --all # principals + policies
oci iam availability-domain list
```
- **Positive (secure):** scoped principal; `NotAuthorizedOrNotFound` on tenancy-wide reads.
- **Negative (vulnerable):** full compartment/policy listing → map every `Allow`
  statement, spot `manage all-resources in tenancy` and root-compartment policies.
  Prowler `identity_no_resources_in_root_compartment`, `identity_non_root_compartment_exists`.

## Public / unauthenticated attack surface
#### T1580 Cloud Infrastructure Discovery — external
- **Object Storage buckets:** pre-authenticated requests (PARs) / public buckets:
  `oci os object list -bn <bucket> -ns <namespace>`.
  - Negative: anonymous read → public bucket. Prowler
    `objectstorage_bucket_not_publicly_accessible`.
- **Public compute / DB:** instances with public IPs, open security lists
  (`0.0.0.0/0` to 22/3389/1521). Prowler network ingress checks.

## Enumerate credentials surface (set up privesc)
```sh
oci iam user api-key list --user-id <ocid>     # signing keys
oci iam auth-token list --user-id <ocid>
```
Long-lived API signing keys and auth tokens are liabilities. Prowler
`identity_user_api_keys_rotated_90_days`, `identity_tenancy_admin_users_no_api_keys`.

---
*Base: [TA0007 Discovery](../_cloud-base/TA0007-discovery.md). Next:
[Phase 2 — Access & Credentials](02-access-and-credentials.md).*
