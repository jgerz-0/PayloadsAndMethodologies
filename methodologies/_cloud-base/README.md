# Cloud Attack Base (MITRE ATT&CK Cloud + Prowler)

> Framework-agnostic **source of truth** for this repo's *cloud* testing
> methodologies — the offensive sibling of the
> [ASVS](../_asvs-base/README.md) (web) and [MASVS](../_masvs-base/README.md)
> (mobile) bases.
>
> **Why not OWASP?** OWASP publishes no cloud verification standard (the nearest,
> the Cloud-Native App Security Top 10, is a stalled ~2022 risk list, not an
> enumerable control set). So this base is anchored on the two real,
> enumerable, cloud-specific standards an offensive tester works from:
> **MITRE ATT&CK** (Enterprise matrix filtered to cloud platforms) as the
> attacker spine, cross-referenced to **Prowler** config checks (CIS-derived) as
> the detective "what should be configured" side.

One markdown per ATT&CK **cloud tactic**, with the techniques (IDs/names/
platforms) **verbatim** from ATT&CK. The base is the *guide* — it says **what**
an attacker does. A **provider methodology** (`aws/`, `gcp/`, `azure/`) projects
each technique onto a specific provider and says **how to test it**, with CLI,
the Prowler check that flags the misconfiguration, and positive/negative
evidence.

## Which base — web / mobile / cloud

| Target | Base |
|---|---|
| Web app, HTTP API, backend framework | [ASVS 5.0](../_asvs-base/README.md) |
| Mobile app client | [MASVS v2](../_masvs-base/README.md) |
| Cloud environment / control plane (AWS, GCP, Azure) | **this base** |

A cloud engagement often spans all three: the **control plane** (this base), the
**apps** running on it (ASVS), and any **mobile clients** (MASVS).

## Sources (vendored vs fetched)

- **Prowler** — vendored submodule [`upstream/prowler`](../../upstream/prowler/);
  665 AWS / 200 Azure / 115 GCP checks with IDs, severity, risk, remediation.
  Only AWS checks carry ATT&CK `TTPs/<tactic>` tags; Azure/GCP are service-tagged.
- **MITRE ATT&CK STIX** — **not** vendored (the `attack-stix-data` repo is
  ~1.5 GB). `generate.py` reads a one-off download of the single
  `enterprise-attack.json` bundle (see [Regenerating](#regenerating)). Current
  build: **ATT&CK v20.0**.

## The workflow

```
          cloud base (_cloud-base/)              provider methodology
        MITRE ATT&CK cloud tactics              (aws/, gcp/, azure/)
┌──────────────────────────────────┐      ┌────────────────────────────────────┐
│ TA0006 Credential Access         │      │ aws/01-access-and-credentials.md    │
│   T1552.005 Instance Metadata    │ ───▶ │   T1552.005 → IMDSv1 creds via SSRF │
│   T1555.006 Cloud Secrets Stores │      │     curl 169.254.169.254/...        │
│   ... (verbatim ATT&CK)          │      │     AccessDenied vs creds returned; │
│   x Prowler TTP checks           │      │     Prowler ec2_imdsv2_enabled      │
└──────────────────────────────────┘      └────────────────────────────────────┘
        what the attacker does                     how to test it here
```

## Tactics (cloud)

ATT&CK matrix order, restricted to tactics with cloud techniques. Provider
methodologies group these into **kill-chain phases** (below) for engagement flow.

| Tactic | Techniques | AWS Prowler checks | Base page |
|---|--:|--:|---|
| TA0001 Initial Access | 10 | 117 | [TA0001](TA0001-initial-access.md) |
| TA0002 Execution | 10 | 1 | [TA0002](TA0002-execution.md) |
| TA0003 Persistence | 25 | 1 | [TA0003](TA0003-persistence.md) |
| TA0004 Privilege Escalation | 14 | 25 | [TA0004](TA0004-privilege-escalation.md) |
| TA0005 Stealth | 16 | 16 | [TA0005](TA0005-stealth.md) |
| TA0112 Defense Impairment | 18 | 16 | [TA0112](TA0112-defense-impairment.md) |
| TA0006 Credential Access | 25 | 39 | [TA0006](TA0006-credential-access.md) |
| TA0007 Discovery | 19 | 8 | [TA0007](TA0007-discovery.md) |
| TA0008 Lateral Movement | 9 | 6 | [TA0008](TA0008-lateral-movement.md) |
| TA0009 Collection | 14 | 2 | [TA0009](TA0009-collection.md) |
| TA0010 Exfiltration | 6 | 0 | [TA0010](TA0010-exfiltration.md) |
| TA0040 Impact | 22 | 0 | [TA0040](TA0040-impact.md) |

> v20 note: the former **Defense Evasion** tactic was split into **Stealth
> (TA0005)** and **Defense Impairment (TA0112)**; Prowler's `TTPs/Defense Evasion`
> tags are counted under both.

## Kill-chain phases (how provider pages are organized)

An offensive cloud test runs as a chain, not 12 isolated tactics. Provider
methodologies group the tactics into phases:

1. **Recon & enumeration** — Discovery (TA0007) + unauthenticated attack surface.
2. **Access & credentials** — Initial Access (TA0001) + Credential Access (TA0006).
3. **Privilege escalation** — Privilege Escalation (TA0004).
4. **Lateral movement & persistence** — Lateral Movement (TA0008) + Persistence
   (TA0003) + Execution (TA0002).
5. **Evasion** — Stealth (TA0005) + Defense Impairment (TA0112).
6. **Collection, exfiltration & impact** — Collection (TA0009) + Exfiltration
   (TA0010) + Impact (TA0040).

## Regenerating

Prowler is a submodule; ATT&CK is fetched once. Don't hand-edit the tactic pages.

```sh
git submodule update --remote upstream/prowler
curl -sL -o /tmp/enterprise-attack.json \
  https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json
python3 methodologies/_cloud-base/generate.py /tmp/enterprise-attack.json
git add upstream/prowler methodologies/_cloud-base
git commit -m "chore: regenerate cloud base (ATT&CK + Prowler bump)"
```

`generate.py` copies ATT&CK technique IDs/names/platforms and tactic definitions
verbatim and counts Prowler coverage; it only applies this repo's chrome.

## References

* [MITRE ATT&CK Cloud matrices](https://attack.mitre.org/matrices/enterprise/cloud/)
* [Prowler](https://github.com/prowler-cloud/prowler) (vendored) ·
  [ScoutSuite](https://github.com/nccgroup/ScoutSuite) ·
  [Pacu](https://github.com/RhinoSecurityLabs/pacu) (AWS exploitation)
* [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) (the control source Prowler implements; not redistributable)
* Sibling bases: [ASVS 5.0](../_asvs-base/README.md) · [MASVS v2](../_masvs-base/README.md)
