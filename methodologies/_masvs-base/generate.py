#!/usr/bin/env python3
"""Generate the _masvs-base/ framework-agnostic MASVS v2 base from the
upstream/MASVS and upstream/MASTG submodules.

Control IDs, statements, and descriptions are copied verbatim from
upstream/MASVS/OWASP_MASVS.yaml; the MASTG test index (id, title, platform,
type) is harvested from the live MASTG V2 tests in upstream/MASTG/tests-beta/.
Only the chrome (header, table layout, footer) is this repo's house style.

MASVS is the mobile analogue of ASVS: it verifies the mobile *client*, whereas
ASVS verifies the server/API it talks to. The two bases are siblings; the
`create-methodology` skill picks ASVS for a web/backend target and MASVS for a
mobile app (e.g. Flutter), and generates the backend half against ASVS.
"""
import re, pathlib, json
import yaml

ROOT = pathlib.Path("/home/udc/Documents/PayloadsAndMethodologies")
MASVS_YAML = ROOT / "upstream/MASVS/OWASP_MASVS.yaml"
MASTG_TESTS = ROOT / "upstream/MASTG/tests-beta"     # live MASTG V2 tests
OUT = ROOT / "methodologies/_masvs-base"
OUT.mkdir(parents=True, exist_ok=True)

PLATFORMS = ("android", "ios")


def read_frontmatter(path: pathlib.Path) -> dict:
    """Return the YAML frontmatter block of a MASTG test file as a dict."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def harvest_tests() -> dict:
    """category-id -> list of (test-id, platform, title, type, relpath)."""
    by_cat: dict[str, list] = {}
    for plat in PLATFORMS:
        base = MASTG_TESTS / plat
        if not base.is_dir():
            continue
        for cat_dir in sorted(base.iterdir()):
            if not cat_dir.is_dir() or not cat_dir.name.startswith("MASVS-"):
                continue
            for f in sorted(cat_dir.glob("MASTG-TEST-*.md")):
                fm = read_frontmatter(f)
                tid = fm.get("id", f.stem)
                title = str(fm.get("title", "")).strip()
                typ = fm.get("type") or []
                if isinstance(typ, str):
                    typ = [typ]
                rel = f.relative_to(ROOT).as_posix()
                by_cat.setdefault(cat_dir.name, []).append(
                    (tid, plat, title, typ, rel)
                )
    for cat in by_cat:
        by_cat[cat].sort(key=lambda r: (r[0], r[1]))
    return by_cat


def main() -> None:
    data = yaml.safe_load(MASVS_YAML.read_text(encoding="utf-8"))
    groups = data["groups"]
    tests_by_cat = harvest_tests()

    manifest = []
    for g in groups:
        gid = g["id"]                       # e.g. MASVS-STORAGE
        title = g["title"].strip()
        index = g.get("index")
        controls = g.get("controls", [])
        tests = tests_by_cat.get(gid, [])
        out_name = f"{gid}.md"
        manifest.append((gid, title, index, len(controls), len(tests), out_name))

        body = []
        body.append(f"# {gid} – {title} (MASVS v2)\n")
        body.append(
            f"> **OWASP MASVS v2 · {gid}** · Control IDs, statements, and "
            f"descriptions are verbatim from the official standard.\n"
            f"> Source: [`upstream/MASVS/OWASP_MASVS.yaml`](../../upstream/MASVS/OWASP_MASVS.yaml)"
            f" · controls: [`upstream/MASVS/controls/`](../../upstream/MASVS/controls/)\n"
            f">\n"
            f"> **Role in this repo:** framework-agnostic mobile base (the client-side "
            f"sibling of the [ASVS base](../_asvs-base/README.md), which covers the "
            f"backend API). When a mobile methodology is generated (see "
            f"[`_masvs-base/README.md`](README.md) and the `create-methodology` skill), "
            f"each control below is projected onto the target stack (e.g. Flutter) as: "
            f"the concrete mechanism/sink, how to test it (static + dynamic), tooling, "
            f"and **positive (secure) vs negative (insecure) evidence**.\n"
        )
        body.append(
            "> **Profiles:** MASVS v2 controls are tested at security-testing "
            "*profiles* — `L1` baseline, `L2` defense-in-depth, and `R` resilience "
            "(anti-reversing/tampering, i.e. the MASVS-RESILIENCE category). Scope an "
            "engagement by profile.\n"
        )

        # --- Controls (verbatim) ---
        body.append("## Controls\n")
        body.append("| Control | Statement | Description |")
        body.append("| :-- | :-- | :-- |")
        for c in controls:
            cid = c["id"]
            stmt = str(c.get("statement", "")).strip().replace("\n", " ")
            desc = str(c.get("description", "")).strip().replace("\n", " ")
            # escape pipes so the table stays intact
            stmt = stmt.replace("|", "\\|")
            desc = desc.replace("|", "\\|")
            body.append(f"| **{cid}** | {stmt} | {desc} |")
        body.append("")

        # --- MASTG test index (how it is verified) ---
        body.append("## MASTG v2 tests covering this category\n")
        if tests:
            body.append(
                "Concrete testing procedures from the MAS Testing Guide (live V2 "
                "tests). Each links to the upstream procedure with commands/evidence.\n"
            )
            body.append("| MASTG test | Platform | Title | Type |")
            body.append("| :-- | :-- | :-- | :-- |")
            for tid, plat, ttitle, typ, rel in tests:
                typ_s = ", ".join(typ)
                ttitle = ttitle.replace("|", "\\|")
                body.append(
                    f"| [{tid}](../../{rel}) | {plat} | {ttitle} | {typ_s} |"
                )
            body.append("")
        else:
            body.append(
                "_No platform-specific MASTG V2 test is mapped to this category yet "
                "(e.g. MASVS-PRIVACY is largely process/▸design-verified). Verify the "
                "controls above by design review and the generic techniques._\n"
            )

        # --- Footer: projection contract ---
        body.append("---\n")
        body.append(
            "### Framework / app projection (filled per stack, not here)\n\n"
            "This base page lists *what* must hold for the mobile client. A generated "
            "mobile methodology page answers *how to test it on that stack*. For each "
            "control above, the generated page should provide, where testable:\n\n"
            "- **Mechanism / sink** — the platform or framework API, storage location, "
            "config, or code pattern that satisfies or violates the control.\n"
            "- **How to test** — concrete **static** (decompile / source / manifest) and "
            "**dynamic** (runtime, instrumentation, traffic) steps, with tooling and "
            "commands.\n"
            "- **Positive evidence (secure)** — what a correctly-built app shows.\n"
            "- **Negative evidence (insecure)** — the confirmation signal for the "
            "finding.\n"
        )

        text = re.sub(r"\n{3,}", "\n\n", "\n".join(body).rstrip() + "\n")
        (OUT / out_name).write_text(text, encoding="utf-8")
        print("wrote", out_name, f"({len(controls)} controls, {len(tests)} tests)")

    (OUT / ".manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    tot_c = sum(m[3] for m in manifest)
    tot_t = sum(m[4] for m in manifest)
    print(f"\n{len(manifest)} categories, {tot_c} controls, {tot_t} MASTG tests")


if __name__ == "__main__":
    main()
