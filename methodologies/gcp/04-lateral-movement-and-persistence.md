# GCP · Phase 4 — Lateral Movement & Persistence

> ATT&CK [TA0008 Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) +
> [TA0003 Persistence](../_cloud-base/TA0003-persistence.md) +
> [TA0002 Execution](../_cloud-base/TA0002-execution.md), projected onto GCP.

## Lateral movement

#### T1021 Remote Services / T1651 Cloud Administration Command
- **Service/sink:** OS Login / SSH via `gcloud compute ssh`, or set an SSH key in
  instance metadata, or run via startup-script.
  ```sh
  gcloud compute ssh <vm> --zone <z>
  gcloud compute instances add-metadata <vm> --metadata=startup-script='...'  # runs as root at boot
  ```
- **Positive (secure):** OS Login + IAM-gated; `compute.instances.setMetadata`
  denied; serial ports off (`compute_instance_serial_ports_in_use`).
- **Negative (vulnerable):** you add an SSH key / startup script → code execution
  on the VM as root, then metadata token → SA.

#### T1078 cross-project movement
Impersonate an SA that has bindings in **other projects/folders**; enumerate with
`gcloud projects list` + `asset search-all-iam-policies` at org scope.

## Persistence

#### T1098 Account Manipulation
- **SA key as a backdoor** (long-lived, survives password changes):
  ```sh
  gcloud iam service-accounts keys create backdoor.json --iam-account <sa>
  ```
  Prowler `iam_sa_no_user_managed_keys` / `iam_sa_user_managed_key_rotate_90_days`.
- **IAM binding backdoor:** bind your external Google account / SA to
  `roles/owner` or `roles/iam.serviceAccountTokenCreator`:
  ```sh
  gcloud projects add-iam-policy-binding <p> --member=user:you@ext --role=roles/owner
  ```
  Negative: an unexpected external member in the project IAM policy.

#### T1136.003 Create Account: Cloud Account
Create a new SA + grant it a powerful role — a standing programmatic backdoor.

#### T1546 Event Triggered Execution
A Cloud Function / Eventarc trigger running as a privileged SA, or a Cloud
Scheduler job invoking it. Prowler `cloudfunction_function_not_publicly_accessible`.

---
*Base: [Lateral Movement](../_cloud-base/TA0008-lateral-movement.md) ·
[Persistence](../_cloud-base/TA0003-persistence.md) ·
[Execution](../_cloud-base/TA0002-execution.md). Next: [Phase 5 — Evasion](05-evasion.md).*
