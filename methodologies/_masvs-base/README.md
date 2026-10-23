# MASVS v2 Base

> Framework-agnostic **source of truth** for this repo's *mobile* testing
> methodologies — the client-side sibling of the
> [ASVS base](../_asvs-base/README.md). One markdown per OWASP **MASVS v2**
> category, with every control ID, statement, and description **verbatim** from
> the official standard (vendored as the [`upstream/MASVS`](../../upstream/MASVS/)
> submodule), each cross-referenced to the concrete testing procedures in the
> MAS Testing Guide ([`upstream/MASTG`](../../upstream/MASTG/)).
>
> This base is the *guide*: it says **what** must hold for a mobile app. A
> **mobile methodology** (e.g. a generated `flutter/`) projects each control
> onto a specific stack and says **how to test it**, with static + dynamic
> steps, tooling, and positive/negative evidence.

## ASVS vs MASVS — which base

OWASP split mobile out of ASVS. Use the right base for the target:

| Target | Base |
|---|---|
| Web app, HTTP API, backend framework | [ASVS 5.0 base](../_asvs-base/README.md) |
| Mobile app client (Flutter, React Native, native Android/iOS) | **this base (MASVS v2)** |

A real mobile engagement spans **both**: the on-device client is MASVS; its
REST/GraphQL **backend** is a normal ASVS target. The `create-methodology`
skill generates the client against this base and the backend against ASVS.

## The workflow

```
            MASVS v2 base                   mobile methodology
        (this folder, _masvs-base/)         (flutter/, react-native/, ...)
┌────────────────────────────────┐      ┌────────────────────────────────────┐
│ MASVS-STORAGE                  │      │ flutter/MASVS-STORAGE.md            │
│   STORAGE-1 securely stores... │ ───▶ │   STORAGE-1 → shared_preferences    │
│   STORAGE-2 prevents leakage   │      │     plaintext vs flutter_secure_    │
│   + MASTG-TEST-0200 ...        │      │     storage→Keystore; static+       │
│   (verbatim controls + tests)  │      │     dynamic evidence                │
└────────────────────────────────┘      └────────────────────────────────────┘
        what must hold                           how to test it here
```

When you ask to **"create a `<mobile stack>` methodology"**, the
`create-methodology` skill (in [`.claude/skills/`](../../.claude/skills/))
walks these categories in order and, for each control testable on the target,
emits:

1. **Mechanism / sink** — the platform/framework API, storage location,
   manifest/plist entry, or code pattern involved.
2. **How to test** — **static** (decompile, source, manifest) and **dynamic**
   (runtime instrumentation, filesystem, traffic) steps, with tooling.
3. **Positive evidence (secure)** — what a correctly-built app shows.
4. **Negative evidence (insecure)** — the finding's confirmation signal.

## Profiles

MASVS v2 drops numeric "levels" in favour of **security testing profiles**.
Scope an engagement by profile:

* **L1** — baseline security, applicable to all apps.
* **L2** — defense-in-depth, for apps handling sensitive data (finance, health).
* **R** — resilience against reverse engineering and tampering (the
  MASVS-RESILIENCE category); for apps with a real anti-tampering/anti-fraud/DRM
  threat model. Additive to L1/L2, not a substitute.

## Categories

| Category | Controls | MASTG tests | Base page |
|---|--:|--:|---|
| MASVS-STORAGE — Storage | 2 | 24 | [STORAGE](MASVS-STORAGE.md) |
| MASVS-CRYPTO — Cryptography | 2 | 20 | [CRYPTO](MASVS-CRYPTO.md) |
| MASVS-AUTH — Authentication and Authorization | 3 | 11 | [AUTH](MASVS-AUTH.md) |
| MASVS-NETWORK — Network Communication | 2 | 29 | [NETWORK](MASVS-NETWORK.md) |
| MASVS-PLATFORM — Platform Interaction | 3 | 47 | [PLATFORM](MASVS-PLATFORM.md) |
| MASVS-CODE — Code Quality | 4 | 23 | [CODE](MASVS-CODE.md) |
| MASVS-RESILIENCE — Reverse-engineering & tampering | 4 | 34 | [RESILIENCE](MASVS-RESILIENCE.md) |
| MASVS-PRIVACY — Privacy | 4 | 12 | [PRIVACY](MASVS-PRIVACY.md) |
| **Total** | **24** | **200** | |

## Regenerating from upstream

These pages are generated from the submodules — don't hand-edit them. When the
MASVS or MASTG submodule is bumped, regenerate so control text stays verbatim
and the test index stays current:

```sh
git submodule update --remote upstream/MASVS upstream/MASTG
python3 methodologies/_masvs-base/generate.py
git add upstream/MASVS upstream/MASTG methodologies/_masvs-base
git commit -m "chore: bump MASVS/MASTG submodules and regenerate base"
```

`generate.py` copies control IDs/statements/descriptions verbatim from
`OWASP_MASVS.yaml` and harvests the live MASTG **V2** test index (id, title,
platform, type) from `upstream/MASTG/tests-beta/`; it only applies this repo's
header, table layout, and footer.

## References

* [OWASP MASVS project](https://mas.owasp.org/MASVS/) · [MASTG](https://mas.owasp.org/MASTG/)
* [MASVS source](../../upstream/MASVS/) · [MASTG source](../../upstream/MASTG/) (vendored submodules)
* [OWASP Mobile App Security Cheat Sheet](../../upstream/CheatSheetSeries/cheatsheets/Mobile_Application_Security_Cheat_Sheet.md)
* Sibling base for the backend API: [ASVS 5.0 base](../_asvs-base/README.md)
