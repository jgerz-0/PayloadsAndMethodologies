# GraphQL

No original write-up here — pulled in as submodules rather than re-authored.
For generic injection payloads (query/mutation injection, introspection
abuse basics), see upstream `PayloadsAllTheThings`'
[GraphQL Injection](../../upstream/PayloadsAllTheThings/GraphQL%20Injection/README.md)
page first. The two repos below go deeper, into methodology and tooling:

* **[graphql-threat-matrix](../../upstream/graphql-threat-matrix/)** — a
  threat-modeling matrix (not just a payload list) mapping GraphQL-specific
  vulnerability classes against which popular server implementations
  (Apollo, GraphQL-Ruby, Hasura, etc.) are affected/mitigated by default.
  Use this to scope what's actually worth testing against a given
  implementation before diving in.
* **[graphql-cop](../../upstream/graphql-cop/)** — a security auditor tool
  (`graphql-cop.py`) that encodes concrete GraphQL testing techniques as
  runnable checks: introspection exposure, batching/alias-based DoS,
  field suggestion/debug mode leakage, CSRF via GET-based queries. Good for
  a fast automated first pass before manual testing.
