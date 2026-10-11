# .NET / ASP.NET Core

No original write-up here — this stack is covered well enough by existing
community references, pulled in as submodules under `upstream/` rather than
re-authored.

* **[OWASP CheatSheetSeries – .NET Security Cheat Sheet](../../upstream/CheatSheetSeries/cheatsheets/DotNet_Security_Cheat_Sheet.md)**
  ([repo](../../upstream/CheatSheetSeries/)) — general ASP.NET/.NET hardening
  and common pitfalls (request validation, machine keys, CORS, TLS pinning).
  The `CheatSheetSeries` repo also covers most other stack-agnostic OWASP
  Top 10 classes if you need a broader reference while testing a .NET app.
* **[ysoserial.net](../../upstream/ysoserial.net/)** — the standard tool/
  reference for .NET deserialization exploitation: ViewState MAC bypass,
  `BinaryFormatter`/`LosFormatter`/`NetDataContractSerializer` gadget chains,
  and ASP.NET model-binding RCE. Start with its `README.md` for the gadget
  list and `--test` usage; this is the first thing to reach for against any
  ASP.NET WebForms app (`__VIEWSTATE`) or app deserializing untrusted data.

See also upstream `PayloadsAllTheThings`'
[Insecure Deserialization](../../upstream/PayloadsAllTheThings/Insecure%20Deserialization/README.md)
page for the generic deserialization methodology that ysoserial.net's
payloads plug into.
