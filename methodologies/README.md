# Methodologies

Tech-stack-specific testing methodologies written to complement, not
duplicate, the generic vulnerability-class payloads in
[`PayloadsAllTheThings`](../upstream/PayloadsAllTheThings/) (tracked as a
submodule under `upstream/`). Each page here assumes you already know the
generic vulnerability class and focuses on what changes when that class
meets a specific framework: where the framework's own abstractions open new
sinks, which of its defaults are commonly misconfigured, and which of its
own CVEs matter.

## Available

Original write-ups (authored here, no equivalent existed upstream):

| Stack | Covers |
|---|---|
| [Angular](angular/README.md) | Angular 2–20: sinks, Trusted Types/sanitizer bypass, router/guard bypass, XSRF handling, prototype pollution, SSR/hydration, zoneless pitfalls |
| [Spring Boot](springboot/README.md) | Actuator abuse, SpEL/Thymeleaf SSTI, Spring4Shell & other critical CVEs, Spring Security misconfig, H2 console RCE, Spring Boot Admin, Spring Cloud Config, Spring Data REST IDOR |

Pointer pages to existing popular community methodologies/tools, pulled in
as submodules rather than re-authored:

| Stack | Points to |
|---|---|
| [.NET / ASP.NET Core](dotnet/README.md) | OWASP CheatSheetSeries' .NET sheet + `ysoserial.net` |
| [Node.js](nodejs/README.md) | `awesome-nodejs-security` |
| [GraphQL](graphql/README.md) | `graphql-threat-matrix` + `graphql-cop` |

## Adding a new stack

First check whether a well-regarded, actively-maintained methodology or
cheat-sheet repo already exists for the stack (GitHub stars, known security
researcher/org authorship, last-push date). If so, `git submodule add` it
under `upstream/` and add a short pointer page here (see
[`dotnet/`](dotnet/README.md), [`nodejs/`](nodejs/README.md),
[`graphql/`](graphql/README.md) for the pattern) — don't re-author content
that's already written and maintained elsewhere.

Only write an original page (like [Angular](angular/README.md) or
[Spring Boot](springboot/README.md)) when nothing suitable exists at that
level of depth. Each original methodology page should:

1. Open with a one-line scope statement and links to the relevant upstream
   `PayloadsAllTheThings` pages it complements (don't repeat generic
   payloads that already live there).
2. Lead with **fingerprinting** — how to confirm the stack/version from the
   outside.
3. Group findings by the stack's own abstractions (e.g. "Actuator", "the
   router", "the ORM layer"), not by generic OWASP category.
4. Call out **known CVEs** worth checking by exact version.
5. End with a **Tools** and **References** section, same as upstream's
   convention.

Add the new page under `methodologies/<stack>/README.md` and link it from
the table above and from the top-level [README](../README.md).
