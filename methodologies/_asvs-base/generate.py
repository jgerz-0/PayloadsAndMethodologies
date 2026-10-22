#!/usr/bin/env python3
"""Generate the _asvs-base/ framework-agnostic ASVS 5.0 base from the
upstream/ASVS submodule. Requirement IDs, levels, and text are copied
verbatim; only the chrome (header, table layout, footer) is our house style.
"""
import re, pathlib, sys

ROOT = pathlib.Path("/home/udc/Documents/PayloadsAndMethodologies")
SRC = ROOT / "upstream/ASVS/5.0/en"
OUT = ROOT / "methodologies/_asvs-base"
OUT.mkdir(parents=True, exist_ok=True)

chap_re = re.compile(r"^0x(?:1[0-9]|2[0-6])-V(\d+)-(.+)\.md$")
row_re = re.compile(r"^\|\s*\*\*([\d.]+)\*\*\s*\|(.*)\|\s*([123])\s*\|\s*$")
sep_re = re.compile(r"^\|[\s:|-]+\|$")

chapters = []
for f in sorted(SRC.glob("0x*-V*.md")):
    m = chap_re.match(f.name)
    if not m:
        continue
    vnum = int(m.group(1))
    slug = m.group(2)
    lines = f.read_text(encoding="utf-8").splitlines()
    # H1 title: "# V8 Authorization"
    h1 = next(l for l in lines if l.startswith("# "))
    title = h1[2:].strip()
    # strip leading "V8 "
    title_name = re.sub(r"^V\d+\s+", "", title)
    out_name = f"V{vnum:02d}-{slug}.md"
    chapters.append((vnum, title_name, out_name, f.name))

    body = []
    body.append(f"# V{vnum} – {title_name} (ASVS 5.0)\n")
    body.append(
        f"> **ASVS 5.0 · Chapter V{vnum}** · Requirement IDs, levels, and text are "
        f"verbatim from the official standard.\n"
        f"> Source: [`upstream/ASVS/5.0/en/{f.name}`](../../upstream/ASVS/5.0/en/{f.name})\n"
        f">\n"
        f"> **Role in this repo:** framework-agnostic base. When a framework "
        f"methodology is generated (see [`_asvs-base/README.md`](README.md) and the "
        f"`create-methodology` skill), every requirement below is projected onto the "
        f"target stack as: the concrete mechanism/sink, how to test it, payloads "
        f"(where applicable), and **positive (secure) vs negative (insecure) response "
        f"examples**.\n"
    )
    body.append(f"> **Level key:** `L1` baseline · `L2` standard (most apps) · `L3` high-assurance.\n")

    i = 0
    n = len(lines)
    # Walk the source, reproducing prose and reformatting requirement tables.
    while i < n:
        line = lines[i]
        if line.startswith("# "):  # drop original H1 (we wrote our own)
            i += 1
            continue
        # requirement table start?
        if line.startswith("| # ") and "Description" in line:
            # skip header + separator
            i += 1
            if i < n and sep_re.match(lines[i].strip()):
                i += 1
            body.append("| # | L | Requirement |")
            body.append("| :-- | :--: | :-- |")
            while i < n and lines[i].startswith("|"):
                rm = row_re.match(lines[i])
                if rm:
                    rid, desc, lvl = rm.group(1), rm.group(2).strip(), rm.group(3)
                    body.append(f"| **{rid}** | {lvl} | {desc} |")
                i += 1
            body.append("")
            continue
        body.append(line)
        i += 1

    # Footer
    body.append("\n---\n")
    body.append(
        "### Framework projection (filled per stack, not here)\n\n"
        "This base page lists *what* must hold. A framework methodology page answers "
        "*how to test it on that stack*. For each requirement above, the generated "
        f"page should provide, where testable black/grey-box:\n\n"
        "- **Mechanism / sink** — the framework API, config, or pattern that satisfies "
        "or violates the requirement.\n"
        "- **How to test** — concrete steps; **payload(s)** when an input is sent.\n"
        "- **Positive response (secure)** — what a correctly-configured app returns "
        "(status, headers, body, behaviour).\n"
        "- **Negative response (insecure)** — what a vulnerable app returns, i.e. the "
        "confirmation signal for the finding.\n"
    )

    text = "\n".join(body).rstrip() + "\n"
    # collapse 3+ blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    (OUT / out_name).write_text(text, encoding="utf-8")
    print("wrote", out_name)

print(f"\n{len(chapters)} chapters")
# emit a small manifest for the index builder
import json
(OUT / ".manifest.json").write_text(json.dumps(chapters), encoding="utf-8")
