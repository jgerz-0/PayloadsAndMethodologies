# Payloads and Methodologies

Personal security testing reference. Combines the upstream
[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
payload library with original testing methodologies for specific tech
stacks that it doesn't go deep on.

## Layout

* **[`upstream/PayloadsAllTheThings/`](upstream/PayloadsAllTheThings/)** — git
  submodule tracking the upstream repo. Pulled in read-only; don't edit
  inside it directly (see [Updating](#updating-upstream) below).
* **[`methodologies/`](methodologies/README.md)** — original, stack-specific
  testing methodologies that complement the upstream payload library:
  * [Angular](methodologies/angular/README.md)
  * [Spring Boot](methodologies/springboot/README.md)

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
