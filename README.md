# Payloads and Methodologies

Personal security testing reference. Combines the upstream
[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
payload library with original testing methodologies for specific tech
stacks that it doesn't go deep on.

## Layout

* **[`upstream/`](upstream/)** — git submodules tracking external repos,
  read-only (see [Updating](#updating-upstream) below):
  * [PayloadsAllTheThings](upstream/PayloadsAllTheThings/) — the core payload library
  * [CheatSheetSeries](upstream/CheatSheetSeries/) (OWASP)
  * [ASVS](upstream/ASVS/) (OWASP Application Security Verification Standard)
  * [MASVS](upstream/MASVS/) (OWASP Mobile Application Security Verification Standard)
  * [MASTG](upstream/MASTG/) (OWASP Mobile Application Security Testing Guide)
  * [prowler](upstream/prowler/) (cloud security scanner — CIS-derived checks for AWS/GCP/Azure/…)
  * [ysoserial.net](upstream/ysoserial.net/)
  * [awesome-nodejs-security](upstream/awesome-nodejs-security/)
  * [graphql-threat-matrix](upstream/graphql-threat-matrix/)
  * [graphql-cop](upstream/graphql-cop/)
* **[`methodologies/`](methodologies/README.md)** — stack-specific testing
  methodologies that complement the upstream payload library.
  * [**ASVS 5.0 base**](methodologies/_asvs-base/README.md) — framework-agnostic
    source of truth for **web/API** stacks, one page per ASVS chapter (V1–V17).
  * [**MASVS v2 base**](methodologies/_masvs-base/README.md) — the **mobile**
    sibling, one page per MASVS category (8), controls verbatim + linked MASTG
    test procedures.
  * [**Cloud attack base**](methodologies/_cloud-base/README.md) — the **cloud**
    sibling (OWASP has no cloud standard), one page per MITRE ATT&CK cloud tactic
    (12), techniques verbatim + cross-referenced Prowler config checks.

    The framework methodologies below are generated from the right base by
    projecting each ASVS requirement / MASVS control / ATT&CK technique onto the
    stack, via the `create-methodology` skill
    ([`.claude/skills/create-methodology`](.claude/skills/create-methodology/SKILL.md)).

  Originally authored for stacks with no good existing equivalent:
  * [Angular](methodologies/angular/README.md)
  * [Flutter](methodologies/flutter/README.md) — MASVS v2-aligned mobile client
    (one page per MASVS category); backend API tested against the ASVS base
  * [Ruby on Rails](methodologies/ruby/README.md) — ASVS 5.0-aligned (one page per ASVS chapter)
  * [Spring Boot](methodologies/springboot/README.md)

  Cloud (generated from the cloud attack base, by kill-chain phase):
  * [AWS](methodologies/aws/README.md)
  * [GCP](methodologies/gcp/README.md)
  * [Azure](methodologies/azure/README.md)
  * [OCI (Oracle Cloud)](methodologies/oci/README.md)
  * [Microsoft 365](methodologies/m365/README.md)
  * [Google Workspace](methodologies/googleworkspace/README.md)

  Pointer pages into the other submodules above, for stacks where a popular
  community methodology/tool already covers it well:
  * [.NET / ASP.NET Core](methodologies/dotnet/README.md)
  * [Node.js](methodologies/nodejs/README.md)
  * [GraphQL](methodologies/graphql/README.md)

## Updating upstream

```sh
git submodule update --remote upstream/PayloadsAllTheThings
git add upstream/PayloadsAllTheThings
git commit -m "chore: bump PayloadsAllTheThings submodule"
```

## Cloning this repo elsewhere

```sh
git clone --recurse-submodules <this-repo-url>
# or, if already cloned without submodules:
git submodule update --init --recursive
```
