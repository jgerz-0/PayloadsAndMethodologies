# Angular Testing Methodology (Angular 2 – 20)

> Testing methodology for Angular applications (standalone components, signals,
> zoneless change detection, SSR/hydration). Complements the upstream
> [XSS in Angular and AngularJS](../../upstream/PayloadsAllTheThings/XSS%20Injection/5%20-%20XSS%20in%20Angular.md)
> page (full AngularJS CSTI payload list) and the general
> [XSS Injection](../../upstream/PayloadsAllTheThings/XSS%20Injection/README.md) page —
> this page is about what is *specific to modern Angular (2+)*, not generic web XSS.

## Summary

* [Fingerprinting](#fingerprinting)
* [Recon: Build Artifacts & Secrets](#recon-build-artifacts--secrets)
* [XSS Sinks in Angular](#xss-sinks-in-angular)
* [Sanitizer & Trusted Types Bypass](#sanitizer--trusted-types-bypass)
* [Client-Side Template Injection (Legacy)](#client-side-template-injection-legacy)
* [Router & Guard Bypass](#router--guard-bypass)
* [CSRF / XSRF-TOKEN Handling](#csrf--xsrf-token-handling)
* [Prototype Pollution](#prototype-pollution)
* [SSR / Hydration Issues (Angular Universal)](#ssr--hydration-issues-angular-universal)
* [Zoneless Change Detection & Signals Pitfalls](#zoneless-change-detection--signals-pitfalls)
* [Third-Party Library CVEs](#third-party-library-cves)
* [Tools](#tools)
* [References](#references)

## Fingerprinting

Angular apps are compiled (AOT by default since Angular 9), so there's no
template source to read directly, but version and build info still leak:

* `ng-version` attribute on the root component in the rendered DOM:
  ```html
  <app-root ng-version="20.0.0">
  ```
* `getAllAngularRootElements()` / `ng.getComponent($0)` in the browser devtools
  console (Angular DevTools debug APIs are exposed in dev builds, and
  sometimes accidentally in prod builds that forget to call
  `enableProdMode()` / omit `fileReplacements` for `environment.prod.ts`).
* Check whether dev mode is active: an accidental dev build logs an Angular
  warning banner ("Angular is running in development mode") and ships
  unminified code with full identifier names — grep for it in the bundle.
* `main.<hash>.js` / `polyfills.<hash>.js` / `vendor.<hash>.js` naming and the
  presence of `zone.js` in the vendor bundle tells you whether the app is
  zone-based (pre-Angular 18 default) or zoneless
  (`provideExperimentalZonelessChangeDetection()` / stable zoneless API in
  Angular 20 — no `zone.js` shipped at all).

## Recon: Build Artifacts & Secrets

* **Source maps**: `ng build` without `--source-map=false` ships
  `*.js.map` files. If they weren't stripped for the prod deploy, pull them
  down and reconstruct original TS source with tools like
  `source-map-explorer` or simply fetching `<file>.js.map` and feeding it to
  a de-mapper. Look for hardcoded API keys, internal endpoint paths, feature
  flags, and comments.
* **environment.ts / environment.prod.ts leakage**: these are inlined at
  build time, not runtime-secret — but devs routinely put real API keys,
  Firebase configs, Sentry DSNs, or internal hostnames in them. Search the
  bundled JS for `environment` object literals.
* `assets/` folder is served as static files verbatim — check for leftover
  `.git`, `config.json`, `.env`, Postman collections, or `license.txt` that
  reveals the exact Angular/library versions in use.
* Angular CLI default `angular.json` / `package.json` are not shipped, but
  CI misconfig sometimes leaves `/package.json`, `/package-lock.json` or
  `/.angular/cache/` reachable on the web root — check directly.

## XSS Sinks in Angular

Angular's default interpolation (`{{ }}`) and property binding (`[prop]`)
auto-escape/sanitize. The real attack surface is where a developer opts out
of that protection:

| Sink | Why it's dangerous |
|---|---|
| `[innerHTML]="userInput"` | Passed through `DomSanitizer.sanitize(SecurityContext.HTML, ...)` automatically, but sanitization is lossy — test bypasses below. |
| `bypassSecurityTrustHtml()` / `bypassSecurityTrustScript()` / `bypassSecurityTrustUrl()` / `bypassSecurityTrustResourceUrl()` / `bypassSecurityTrustStyle()` | Explicitly opts OUT of sanitization. If user input reaches any `bypassSecurityTrust*` call, that's a direct XSS unless the dev independently sanitized first. |
| `ElementRef.nativeElement.innerHTML = ...` | Bypasses Angular's sanitizer entirely — raw DOM API. |
| `Renderer2.setProperty(el, 'innerHTML', ...)` | Same — `Renderer2` does not sanitize `innerHTML` assignments. |
| `document.write`, `eval`, `new Function()`, `setTimeout('string', ...)` | Classic sinks, same as any JS app — grep bundle for these. |
| `[style]` / `[ngStyle]` bound to attacker data pre-Angular 14 | `javascript:` / `expression()` CSS vectors in old sanitizer versions (CVE-2021-22118-adjacent bugs); mostly patched, but worth testing against instances pinned to old versions. |
| Attribute bindings like `[attr.href]="userUrl"` | `SecurityContext.URL` sanitizer still allows `javascript:` on some browsers if the sanitizer regex is defeated by whitespace/encoding tricks — test. |

Practical testing flow:
1. Grep the deminified bundle for `bypassSecurityTrust`, `innerHTML`,
   `nativeElement`, `Renderer2`, `ElementRef`.
2. For every hit, trace the data source back to a route param, query string,
   form field, or API response rendered without server-side encoding.
3. Common sanitizer bypass payloads to throw at `[innerHTML]` sinks:
   ```html
   <svg onload=alert(document.domain)>
   <img src=x onerror=alert(document.domain)>
   <a href="javascript:alert(document.domain)">click</a>
   <svg><animate onbegin=alert(1) attributeName=x dur=1s>
   ```
   Angular's built-in HTML sanitizer strips `<script>` and most `on*`
   handlers, but SVG-based and `<style>`-based vectors have historically
   slipped through in older `@angular/platform-browser` releases — always
   check the exact `@angular/*` version against the Angular security
   advisories (GHSA) before assuming sanitization is airtight.

## Sanitizer & Trusted Types Bypass

Angular 20 apps increasingly ship with `Content-Security-Policy:
require-trusted-types-for 'script'` plus the CLI's auto-injected Trusted
Types policy (`angular#bundler`). This blocks raw `innerHTML` assignment
from untrusted strings at the browser level, independent of Angular's own
sanitizer.

* Check response headers / meta tags for `Content-Security-Policy` and
  whether `trusted-types` is enforced or report-only
  (`Content-Security-Policy-Report-Only`) — report-only means bypasses are
  still exploitable, just logged.
* If Trusted Types is enforced, look for:
  * Custom Trusted Types policies created with permissive
    `createHTML: (s) => s` (no-op passthrough) — grep for `trustedTypes.createPolicy`.
  * Angular's own `angular#bundler` policy, or `angular#unsafe-bypass`
    created by `bypassSecurityTrust*` calls — if attacker input reaches
    those calls, Trusted Types is irrelevant since Angular itself mints a
    trusted value.
  * DOM XSS sinks not covered by Trusted Types enforcement (e.g.
    `location.href`, `document.domain`, `eval` is still blocked by
    `require-trusted-types-for 'script'` only if `script` directive is
    included — check exact directive value).
* Use Chrome DevTools' **Trusted Types violation reports** in the console —
  they point directly at the sink and the offending call stack.

## Client-Side Template Injection (Legacy)

The classic Angular CSTI payload (`{{constructor.constructor('alert(1)')()}}`)
only works against **JIT-compiled** Angular (pre-Angular 9 default, or apps
explicitly built with `--aot=false` / using `JitCompilerFactory`). AOT
compilation (default since Angular 9, and universal by Angular 20) compiles
templates at build time, so there is no runtime `Function` constructor to
reach via interpolation.

Still worth testing because:
* Legacy AngularJS (1.x — a completely different framework, not "Angular")
  is still frequently confused with Angular 2+ and is **far more commonly
  vulnerable** to CSTI (`{{constructor.constructor('alert(1)')()}}` works
  out of the box on unsandboxed AngularJS ≥1.6). Fingerprint via `ng-app`,
  `ng-controller` attributes or `angular.min.js` vs `@angular/core` bundle
  naming before picking a payload set — see the upstream
  [XSS in Angular and AngularJS](../../upstream/PayloadsAllTheThings/XSS%20Injection/5%20-%20XSS%20in%20Angular.md)
  page for the full version-by-version AngularJS CSTI payload list.
* Some legacy enterprise apps still run Angular 2–8 with JIT mode enabled
  for dynamic template scenarios (CMS-driven template strings compiled at
  runtime via `Compiler.compileModuleSync`) — if you find a feature where
  user input becomes part of a *template string* (not just an interpolated
  *value*), test the JIT payload regardless of declared Angular version.

## Router & Guard Bypass

* **Route guards are client-side only** — `CanActivate` / `CanActivateFn`
  (functional guards, standard since Angular 15+) run in the browser and
  can be trivially bypassed by calling the API directly or by manipulating
  client-side state (e.g. a guard that checks a decoded JWT's `exp` client-side
  with no server validation). Always re-test every "protected" route's
  backing API endpoint directly, unauthenticated and with a tampered JWT.
* **Lazy-loaded modules/routes**: check `main.<hash>.js` for lazy chunk
  manifests (`__NG_LOADED_MODULES` or webpack/esbuild chunk maps) — route
  paths for admin panels or feature-flagged functionality are often present
  in the chunk graph even when not linked in the visible UI. Fetch the
  lazy chunk directly by filename to read admin-only component code.
* **Open redirect via router**: `routerLink` / `Router.navigateByUrl()`
  bound to a query parameter (`?returnUrl=`, `?next=`) without an allowlist
  check — standard open redirect, test with `//evil.com`,
  `/\evil.com`, `https:evil.com`.
* **Matrix/query param confusion**: Angular's router treats `;` as a matrix
  parameter delimiter (`/user;id=123`) — backends built on Spring or other
  frameworks that also treat `;` specially can produce request-smuggling-like
  path mismatches between what Angular's router matched client-side and what
  the server-side router/WAF matched.

## CSRF / XSRF-TOKEN Handling

Angular's `HttpClientXsrfModule` (classic) / `withXsrfConfiguration()`
(standalone `provideHttpClient()`, default since Angular 15+) implements the
double-submit cookie pattern: it reads a cookie (default name `XSRF-TOKEN`)
and echoes it back as a header (default name `X-XSRF-TOKEN`) on same-origin
requests.

Test for a broken implementation:
* Is the `XSRF-TOKEN` cookie set **`HttpOnly`**? If so, Angular's
  `HttpClient` cannot read it via `document.cookie`, and the header will
  never be sent — confirms the CSRF mechanism is silently broken (check
  whether the server still accepts requests missing the header entirely).
* Is the cookie scoped with `SameSite=None`/no `SameSite`, allowing
  cross-origin pages to still trigger the cookie-setting response and ride
  the double-submit check if the backend doesn't validate token freshness?
* Does the backend actually validate the `X-XSRF-TOKEN` header against the
  session, or just check for its *presence*? Many custom backends implement
  "does header exist" rather than "does header match cookie" — try sending
  an arbitrary/stale value.
* Custom `withXsrfConfiguration({ cookieName, headerName })` — confirm the
  configured names actually match what the backend expects; mismatches
  silently disable the protection without any error.

## Prototype Pollution

* Deep-merge utilities used for state management (NgRx `createReducer`
  custom merge logic, or hand-rolled `Object.assign`/spread-based state
  updates fed directly from `JSON.parse()` of a query string or API
  response) are a common prototype pollution vector — test with
  `?__proto__[polluted]=true` or JSON bodies containing
  `{"__proto__": {"polluted": true}}` against any endpoint whose response is
  deep-merged into app state.
* Angular itself has had prototype pollution advisories in `@angular/common`
  's `HttpParams`/`HttpUrlEncodingCodec` parsing paths historically — check
  the exact `@angular/common` version against published GHSA advisories.
* lodash (`_.merge`, `_.defaultsDeep`, `_.set`) is still extremely common as
  a transitive dependency in Angular enterprise apps for form-state
  merging — fingerprint the lodash version in the vendor bundle and check
  against known CVEs (CVE-2018-3721, CVE-2019-10744, CVE-2020-8203).

## SSR / Hydration Issues (Angular Universal)

Angular 17+ ships first-party SSR with **non-destructive hydration**
(stable by default from Angular 17, refined through 20) via
`provideClientHydration()`.

* **Hydration mismatch XSS**: if server-rendered HTML and client-rendered
  HTML diverge (e.g. a `[innerHTML]` value computed differently on server
  vs. client due to environment-dependent logic), Angular's hydration can
  end up attaching event listeners to attacker-controlled DOM nodes that
  were never actually sanitized client-side — test any SSR page where
  `[innerHTML]` content depends on request headers (`User-Agent`,
  `Accept-Language`) that differ between the initial SSR pass and
  client-side re-render.
* **Server-side template injection on the Node renderer**: if the Express/
  Node SSR server interpolates request data (URL, headers, cookies)
  directly into HTML *outside* of Angular's own rendering (e.g. a custom
  `index.html` templating step before/after `renderModule()`), that's a
  classic server-side injection point independent of Angular's client-side
  protections.
* **Cache poisoning**: SSR responses are often cached (CDN/Varnish/
  Cloudflare) keyed only on URL. If the SSR output varies by header
  (locale, auth state accidentally rendered server-side, A/B flags) and
  that header isn't part of the cache key, you get classic web cache
  poisoning / cache deception — see the upstream
  [Cache Deception](../../upstream/PayloadsAllTheThings/Web%20Cache%20Deception/README.md)
  page.
* **Environment/secret leakage via TransferState**: Angular Universal uses
  `TransferState` to pass server-fetched data to the client to avoid
  double-fetching. Inspect the inlined `<script id="ng-state">` JSON blob in
  the SSR'd HTML for over-fetched API responses that include fields the
  client-side view never renders (classic over-fetching/excessive data
  exposure — check for PII, internal IDs, or other users' data fetched
  server-side for a list view but trimmed only in the template).

## Zoneless Change Detection & Signals Pitfalls

Angular 20 treats zoneless change detection
(`provideExperimentalZonelessChangeDetection()` → stabilizing API) and
Signals as first-class. Security-relevant implications:

* Without `zone.js`, there is no automatic patching of async APIs
  (`setTimeout`, `XMLHttpRequest`, event listeners) — any custom security
  logic that previously relied on zone.js's monkeypatched async boundary
  (e.g. a guard re-checking auth state "whenever anything async settles")
  may silently stop firing in a zoneless app. Confirm authorization re-checks
  are still wired to explicit signal/effect updates rather than an implicit
  zone-triggered change detection cycle.
* `effect()` side effects that write to the DOM directly (bypassing
  template binding, e.g. `effect(() => el.nativeElement.innerHTML = data())`)
  reintroduce raw `innerHTML` sinks outside of Angular's binding/sanitizer
  pipeline — grep for `effect(` + `innerHTML`/`nativeElement` together.

## Third-Party Library CVEs

Angular apps commonly bundle UI libraries with their own XSS history —
fingerprint exact versions in the vendor bundle and check against public
advisories:

* **ngx-bootstrap** — multiple historic XSS advisories via `tooltip`/`popover`
  HTML content inputs.
* **PrimeNG** — XSS via `pTemplate`/`innerHTML`-based cell renderers in
  table components when bound directly to API data.
* **ngx-quill` / Quill.js** — rich text editor, classic stored-XSS surface if
  output isn't re-sanitized server-side before redisplay.
* **@swimlane/ngx-charts**, **ng2-charts** — SVG label rendering from
  untrusted data.
* **jQuery** (still pulled in by some Angular Material/legacy wrappers) —
  check for the `$.html()`/`.append()` sinks same as any jQuery app.

Always cross-reference exact versions against:
`https://github.com/angular/angular/security/advisories` and `npm audit` /
`osv-scanner` output on the extracted `package-lock.json` (if reachable) or
reconstructed dependency tree from the vendor bundle.

## Tools

* **Angular DevTools** (browser extension) — component tree, signal/state
  inspection in dev builds.
* **retire.js** — fingerprints vulnerable JS library versions in the bundle.
* **source-map-explorer** — visualize/extract original source from leaked
  `.js.map` files.
* **ngx-source-map-explorer** / manual `curl` of `*.js.map` + a JS
  source-map CLI de-bundler.
* **Burp/ZAP** passive scan + manual grep of deminified bundles for the sink
  list above (`bypassSecurityTrust`, `innerHTML`, `nativeElement`, `eval`).
* **CSP Evaluator** (Google) — validate the app's CSP/Trusted Types header
  for bypassable patterns.

## References

* [Angular Security Guide (official docs)](https://angular.dev/best-practices/security)
* [Angular Security Advisories (GitHub)](https://github.com/angular/angular/security/advisories)
* [Angular Trusted Types docs](https://angular.dev/best-practices/security#trusted-types)
* [Angular Hydration guide](https://angular.dev/guide/hydration)
* Upstream: [PayloadsAllTheThings – XSS in Angular and AngularJS](../../upstream/PayloadsAllTheThings/XSS%20Injection/5%20-%20XSS%20in%20Angular.md)
* Upstream: [PayloadsAllTheThings – XSS Injection](../../upstream/PayloadsAllTheThings/XSS%20Injection/README.md)
* Upstream: [PayloadsAllTheThings – Web Cache Deception](../../upstream/PayloadsAllTheThings/Web%20Cache%20Deception/README.md)
