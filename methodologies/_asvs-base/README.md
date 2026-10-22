# ASVS 5.0 Base

> Framework-agnostic **source of truth** for this repo's testing
> methodologies. One markdown per OWASP ASVS 5.0 chapter ("phase"), with every
> requirement ID, level, and text **verbatim** from the official standard
> (vendored as the [`upstream/ASVS`](../../upstream/ASVS/) submodule).
>
> This base is the *guide*. It says **what** must hold. A **framework
> methodology** (e.g. a generated `ruby/`, or [`springboot/`](../springboot/README.md))
> projects each requirement onto a specific stack and says **how to test it**,
> with payloads and positive/negative response examples.

## The workflow

```
            ASVS 5.0 base                 framework methodology
          (this folder, _asvs-base/)      (ruby/, dotnet/, node/, ...)
┌───────────────────────────────┐      ┌────────────────────────────────────┐
│ V6 Authentication             │      │ ruby/06-authentication.md           │
│   6.2.1  password length ...  │ ───▶ │   6.2.1 → Devise password_length,   │
│   6.2.2  breach check ...     │      │          test payload, secure vs    │
│   ...  (verbatim ASVS reqs)   │      │          insecure response example  │
└───────────────────────────────┘      └────────────────────────────────────┘
        what must hold                           how to test it here
```

When you ask to **"create a `<framework>` methodology"**, the
`create-methodology` skill (in [`.claude/skills/`](../../.claude/skills/))
walks these chapters in order and, for each requirement that is testable on
the target stack, emits:

1. **Mechanism / sink** — the framework API, config, or code pattern involved.
2. **How to test** — concrete black/grey-box steps; **payload(s)** when input
   is sent.
3. **Positive response (secure)** — what a correctly-configured app returns.
4. **Negative response (insecure)** — what a vulnerable app returns (the
   finding's confirmation signal).

## Levels

ASVS assigns each requirement a verification level. Scope an engagement by
the target level:

* **L1** — baseline, black-box testable; minimum for any app.
* **L2** — standard; the default target for most applications handling
  sensitive data.
* **L3** — high-assurance; critical systems.

An L2 engagement covers L1+L2 requirements, an L3 engagement covers all three.

## Chapters

| Chapter | Reqs | Base page |
|---|--:|---|
| V1 Encoding and Sanitization | 30 | [V01](V01-Encoding-and-Sanitization.md) |
| V2 Validation and Business Logic | 13 | [V02](V02-Validation-and-Business-Logic.md) |
| V3 Web Frontend Security | 31 | [V03](V03-Web-Frontend-Security.md) |
| V4 API and Web Service | 16 | [V04](V04-API-and-Web-Service.md) |
| V5 File Handling | 13 | [V05](V05-File-Handling.md) |
| V6 Authentication | 47 | [V06](V06-Authentication.md) |
| V7 Session Management | 19 | [V07](V07-Session-Management.md) |
| V8 Authorization | 13 | [V08](V08-Authorization.md) |
| V9 Self-contained Tokens | 7 | [V09](V09-Self-contained-Tokens.md) |
| V10 OAuth and OIDC | 36 | [V10](V10-OAuth-and-OIDC.md) |
| V11 Cryptography | 24 | [V11](V11-Cryptography.md) |
| V12 Secure Communication | 12 | [V12](V12-Secure-Communication.md) |
| V13 Configuration | 21 | [V13](V13-Configuration.md) |
| V14 Data Protection | 13 | [V14](V14-Data-Protection.md) |
| V15 Secure Coding and Architecture | 21 | [V15](V15-Secure-Coding-and-Architecture.md) |
| V16 Security Logging and Error Handling | 17 | [V16](V16-Security-Logging-and-Error-Handling.md) |
| V17 WebRTC | 12 | [V17](V17-WebRTC.md) |
| **Total** | **345** | |

## Regenerating from upstream

These pages are generated from the submodule — don't hand-edit them. When the
ASVS submodule is bumped, regenerate so requirement text stays verbatim:

```sh
git submodule update --remote upstream/ASVS
python3 methodologies/_asvs-base/generate.py
git add upstream/ASVS methodologies/_asvs-base
git commit -m "chore: bump ASVS submodule and regenerate base"
```

`generate.py` copies IDs/levels/text verbatim and only applies this repo's
header, table layout, and footer. A post-run check that requirement counts
match the source is in the commit history.

## References

* [OWASP ASVS project](https://owasp.org/www-project-application-security-verification-standard/)
* [ASVS 5.0 source](../../upstream/ASVS/5.0/en/) (vendored submodule)
* Framework methodologies generated from this base:
  [Angular](../angular/README.md) · [Spring Boot](../springboot/README.md)
  (and e.g. Ruby on Rails, produced via the `create-methodology` skill)
