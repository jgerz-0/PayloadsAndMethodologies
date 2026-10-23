#!/usr/bin/env python3
"""Generate the _cloud-base/ framework-agnostic cloud-attack base.

Unlike the ASVS/MASVS bases, OWASP has no cloud verification standard, so this
base is anchored on **MITRE ATT&CK** (the Enterprise matrix filtered to cloud
platforms: IaaS, SaaS, Identity Provider, Office Suite) as the offensive spine,
cross-referenced to **Prowler** config checks (CIS-derived) as the defensive
"what should be configured" side.

Technique IDs/names/descriptions and tactic names are copied verbatim from the
ATT&CK STIX bundle; Prowler coverage is counted from the vendored submodule.
Only the chrome (header, tables, footer) is this repo's house style.

ATT&CK STIX is NOT vendored (the attack-stix-data repo is ~1.5 GB). Fetch the
single bundle once and pass its path:

    curl -sL -o /tmp/enterprise-attack.json \\
      https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json
    python3 methodologies/_cloud-base/generate.py /tmp/enterprise-attack.json
"""
import json, re, sys, pathlib, glob, collections

ROOT = pathlib.Path("/home/udc/Documents/PayloadsAndMethodologies")
PROWLER = ROOT / "upstream/prowler/prowler/providers"
OUT = ROOT / "methodologies/_cloud-base"
OUT.mkdir(parents=True, exist_ok=True)

CLOUD_PLATFORMS = {"IaaS", "SaaS", "Identity Provider", "Office Suite",
                   "Google Workspace", "Azure AD", "Office 365"}

# ATT&CK matrix (column) order, restricted to tactics that have cloud techniques.
# v20 split the former "Defense Evasion" into "Stealth" + "Defense Impairment".
TACTIC_ORDER = [
    "initial-access", "execution", "persistence", "privilege-escalation",
    "stealth", "defense-impairment", "credential-access", "discovery",
    "lateral-movement", "collection", "exfiltration", "impact",
]
# Prowler uses the pre-v20 tactic labels in its CheckType "TTPs/<name>" tags.
PROWLER_TTP_TO_TACTIC = {
    "Initial Access": "initial-access", "Execution": "execution",
    "Persistence": "persistence", "Privilege Escalation": "privilege-escalation",
    "Credential Access": "credential-access", "Discovery": "discovery",
    "Lateral Movement": "lateral-movement", "Collection": "collection",
    "Exfiltration": "exfiltration", "Impact": "impact",
    # pre-v20 "Defense Evasion" maps onto both v20 successor tactics
    "Defense Evasion": ("stealth", "defense-impairment"),
}
PROVIDERS = ("aws", "azure", "gcp")


def attack_id(o):
    for r in o.get("external_references", []):
        if r.get("source_name") == "mitre-attack":
            return r.get("external_id"), r.get("url")
    return None, None


def load_attack(path):
    d = json.load(open(path))
    objs = d["objects"]
    version = next((o.get("x_mitre_version") for o in objs
                    if o.get("type") == "x-mitre-collection"), "?")
    tactics = {}   # shortname -> (TAxxxx, name, description)
    for o in objs:
        if o.get("type") == "x-mitre-tactic":
            tid, _ = attack_id(o)
            tactics[o["x_mitre_shortname"]] = (tid, o["name"],
                                               o.get("description", "").strip())
    # techniques grouped by tactic shortname; keep parents + sub-techniques
    by_tactic = collections.defaultdict(list)
    for o in objs:
        if o.get("type") != "attack-pattern":
            continue
        if o.get("x_mitre_deprecated") or o.get("revoked"):
            continue
        if not (set(o.get("x_mitre_platforms", [])) & CLOUD_PLATFORMS):
            continue
        tid, url = attack_id(o)
        if not tid:
            continue
        plats = [p for p in o.get("x_mitre_platforms", []) if p in CLOUD_PLATFORMS]
        rec = {
            "id": tid, "name": o["name"], "url": url,
            "sub": o.get("x_mitre_is_subtechnique", False),
            "platforms": plats,
            "desc": o.get("description", "").split("\n")[0].strip(),
        }
        for ph in o.get("kill_chain_phases", []):
            if ph.get("kill_chain_name") == "mitre-attack":
                by_tactic[ph["phase_name"]].append(rec)
    for t in by_tactic:
        by_tactic[t].sort(key=lambda r: r["id"])
    return version, tactics, by_tactic


def prowler_ttp_counts():
    """provider -> tactic-shortname -> check count (AWS only has TTP tags)."""
    counts = {p: collections.Counter() for p in PROVIDERS}
    totals = {}
    for prov in PROVIDERS:
        n = 0
        for f in glob.glob(str(PROWLER / prov / "services/**/*.metadata.json"),
                           recursive=True):
            try:
                m = json.load(open(f))
            except Exception:
                continue
            n += 1
            for ct in m.get("CheckType", []):
                if not ct.startswith("TTPs/"):
                    continue
                label = ct.split("/", 1)[1].split("/", 1)[0]  # strip subvariant
                mapped = PROWLER_TTP_TO_TACTIC.get(label)
                if isinstance(mapped, tuple):
                    for t in mapped:
                        counts[prov][t] += 1
                elif mapped:
                    counts[prov][mapped] += 1
        totals[prov] = n
    return counts, totals


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: generate.py <path-to-enterprise-attack.json>  (see header)")
    version, tactics, by_tactic = load_attack(sys.argv[1])
    ttp_counts, totals = prowler_ttp_counts()

    manifest = []
    for short in TACTIC_ORDER:
        tid, tname, tdesc = tactics[short]
        techs = by_tactic.get(short, [])
        parents = [t for t in techs if not t["sub"]]
        subs = [t for t in techs if t["sub"]]
        out_name = f"{tid}-{short}.md"
        aws_n = ttp_counts["aws"].get(short, 0)
        manifest.append((tid, short, tname, len(techs), aws_n, out_name))

        b = []
        b.append(f"# {tid} – {tname} (cloud)\n")
        b.append(
            f"> **MITRE ATT&CK v{version} · tactic {tid} {tname}**, filtered to cloud "
            f"platforms (IaaS, SaaS, Identity Provider, Office Suite). Technique IDs, "
            f"names, and the tactic definition are verbatim from ATT&CK.\n"
            f">\n"
            f"> **Role in this repo:** framework-agnostic cloud base — the offensive "
            f"sibling of the [ASVS](../_asvs-base/README.md) / [MASVS](../_masvs-base/README.md) "
            f"bases. When a provider methodology is generated (AWS/GCP/Azure; see "
            f"[`_cloud-base/README.md`](README.md) and the `create-methodology` skill), "
            f"each technique below is projected onto that provider: the concrete service/"
            f"API/sink, how to test it (enumerate + attempt), CLI, and **positive (secure) "
            f"vs negative (vulnerable) evidence** — cross-referenced to the Prowler config "
            f"checks that detect the corresponding misconfiguration.\n"
        )
        b.append(f"> **Tactic goal:** {tdesc}\n")
        b.append(
            f"> **Prowler config-check coverage (detective side):** AWS **{aws_n}** checks "
            f"tagged `TTPs/{tname}` (Azure/GCP Prowler checks are service-tagged, not "
            f"tactic-tagged — see per-provider pages).\n"
        )

        b.append("## Techniques (cloud)\n")
        b.append("| ID | Technique | Cloud platforms |")
        b.append("| :-- | :-- | :-- |")
        # parents, each followed by its sub-techniques (matched by prefix)
        for p in parents:
            b.append(f"| [{p['id']}]({p['url']}) | **{p['name']}** | {', '.join(p['platforms'])} |")
            for s in subs:
                if s["id"].startswith(p["id"] + "."):
                    b.append(f"| [{s['id']}]({s['url']}) | &nbsp;&nbsp;↳ {s['name']} | {', '.join(s['platforms'])} |")
        # orphan sub-techniques whose parent isn't cloud-tagged
        covered = {s["id"] for p in parents for s in subs if s["id"].startswith(p["id"] + ".")}
        for s in subs:
            if s["id"] not in covered:
                b.append(f"| [{s['id']}]({s['url']}) | ↳ {s['name']} | {', '.join(s['platforms'])} |")
        b.append("")

        b.append("---\n")
        b.append(
            "### Provider projection (filled per provider, not here)\n\n"
            "This base page lists *what* an attacker does in this tactic against cloud. "
            "A provider methodology projects each relevant technique onto AWS / GCP / "
            "Azure with:\n\n"
            "- **Service / sink** — the concrete service, API, or resource (e.g. IAM, "
            "STS, S3, Metadata/IMDS, KMS, Entra ID, GCS).\n"
            "- **How to test** — enumerate then attempt; the CLI/API call or tool "
            "(awscli, `gcloud`, `az`, Pacu, ScoutSuite, Prowler) and payload.\n"
            "- **Positive evidence (secure)** — `AccessDenied` / guardrail blocks it.\n"
            "- **Negative evidence (vulnerable)** — the call succeeds / data returned — "
            "the confirmation signal, plus the Prowler check ID that flags it.\n"
        )

        text = re.sub(r"\n{3,}", "\n\n", "\n".join(b).rstrip() + "\n")
        (OUT / out_name).write_text(text, encoding="utf-8")
        print(f"wrote {out_name}  ({len(techs)} techniques, aws TTP checks {aws_n})")

    (OUT / ".manifest.json").write_text(
        json.dumps({"version": version, "tactics": manifest, "totals": totals}),
        encoding="utf-8")
    tot = sum(m[3] for m in manifest)
    print(f"\nATT&CK v{version}: {len(manifest)} cloud tactics, {tot} technique rows")
    print("Prowler checks:", totals)


if __name__ == "__main__":
    main()
