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
  * [ysoserial.net](upstream/ysoserial.net/)
  * [awesome-nodejs-security](upstream/awesome-nodejs-security/)
  * [graphql-threat-matrix](upstream/graphql-threat-matrix/)
  * [graphql-cop](upstream/graphql-cop/)
* **[`methodologies/`](methodologies/README.md)** — stack-specific testing
  methodologies that complement the upstream payload library. Originally
  authored for stacks with no good existing equivalent:
  * [Angular](methodologies/angular/README.md)
  * [Spring Boot](methodologies/springboot/README.md)

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
