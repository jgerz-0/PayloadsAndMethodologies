# OCI · Phase 4 — Lateral Movement & Persistence

> ATT&CK [TA0008 Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) +
> [TA0003 Persistence](../_cloud-base/TA0003-persistence.md) +
> [TA0002 Execution](../_cloud-base/TA0002-execution.md), projected onto OCI.

## Lateral movement
#### T1021 / T1651 Cloud Administration Command
- **Service/sink:** Run Command / Cloud Agent on compute, or SSH via injected key.
  ```sh
  oci instance-agent command create --compartment-id <c> --content ... --target <instance>
  ```
- **Positive (secure):** `NotAuthorizedOrNotFound`; agent command plugin disabled.
- **Negative (vulnerable):** command runs on the VM → on-box creds + instance
  principal token → pivot across compartments.

#### T1078 cross-compartment / cross-tenancy
Use a principal/instance-principal with policies spanning other compartments;
enumerate the subtree (`oci iam compartment list --compartment-id-in-subtree true`).

## Persistence
#### T1098 Account Manipulation
- **New API key / auth token** on a controlled or privileged user (quiet, survives
  password resets):
  ```sh
  oci iam user api-key upload --user-id <ocid> --key-file backdoor_pub.pem
  oci iam auth-token create --user-id <ocid> --description x
  ```
  Prowler `identity_user_api_keys_rotated_90_days` (extra/old keys stand out).
- **Policy backdoor:** an `Allow` statement granting a controlled group/dynamic
  group standing access.

#### T1136.003 Create Account: Cloud Account
`oci iam user create` + add to an admin group — standing backdoor identity.

#### T1546 Event Triggered Execution
OCI Functions / Events rule with a privileged dynamic group, triggered on an
innocuous event.

---
*Base: [Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) ·
[Persistence](../_cloud-base/TA0003-persistence.md) ·
[Execution](../_cloud-base/TA0002-execution.md). Next: [Phase 5 — Evasion](05-evasion.md).*
