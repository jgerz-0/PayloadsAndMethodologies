#!/usr/bin/env python3
"""Generate the _kubernetes-base/ from the OWASP Kubernetes Top 10 (2025).

Kubernetes is not an IaaS cloud provider, so it gets its own base anchored on
the recognized standard — the **OWASP Kubernetes Top 10 (2025)** (vendored at
`upstream/kubernetes-top-ten`) — cross-referenced to **Prowler** kubernetes
checks (`upstream/prowler`) and the **MITRE ATT&CK Containers** matrix.

Risk IDs, titles, and the Overview text are copied verbatim from the OWASP
source; the ATT&CK-tactic and Prowler-service mappings are this repo's curation.
Only the chrome is house style.
"""
import re, pathlib, json, glob

ROOT = pathlib.Path("/home/udc/Documents/PayloadsAndMethodologies")
SRC = ROOT / "upstream/kubernetes-top-ten/2025/en/src"
PROWLER_K8S = ROOT / "upstream/prowler/prowler/providers/kubernetes/services"
OUT = ROOT / "methodologies/_kubernetes-base"
OUT.mkdir(parents=True, exist_ok=True)

# Risk id -> (Prowler k8s services that detect it, ATT&CK Containers tactics)
RISK_MAP = {
    "K01": (["core", "rbac"], ["Privilege Escalation", "Execution"]),
    "K02": (["rbac"], ["Privilege Escalation", "Lateral Movement"]),
    "K03": (["apiserver", "etcd", "core"], ["Credential Access"]),
    "K04": (["apiserver"], ["Defense Impairment", "Stealth"]),
    "K05": (["core"], ["Lateral Movement"]),
    "K06": (["apiserver", "kubelet", "etcd"], ["Initial Access", "Discovery"]),
    "K07": (["kubelet", "scheduler", "controllermanager", "apiserver"],
            ["Initial Access", "Privilege Escalation"]),
    "K08": ([], ["Lateral Movement", "Credential Access"]),  # cross-ref cloud base
    "K09": (["apiserver"], ["Initial Access", "Credential Access"]),
    "K10": (["apiserver"], ["Stealth", "Defense Impairment"]),
}


def prowler_checks(services, keyword_filter=None, limit=6):
    ids = []
    for svc in services:
        for d in sorted(glob.glob(str(PROWLER_K8S / svc / "*"))):
            name = pathlib.Path(d).name
            if not pathlib.Path(d).is_dir() or name in ("lib", "__pycache__"):
                continue
            ids.append(name)
    return ids


def extract(md_path):
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'title:\s*"([^"]+)"', text)
    title = m.group(1) if m else md_path.stem
    # Overview = text between "## Overview" and the next "## " / "Description"
    ov = ""
    mo = re.search(r"##\s*Overview\s*(.+?)(?:\n##\s|\nDescription\b)", text, re.DOTALL)
    if mo:
        ov = mo.group(1).strip()
    # keep first 2 paragraphs, collapse
    paras = [p.strip() for p in re.split(r"\n\s*\n", ov) if p.strip()]
    overview = "\n\n".join(paras[:2])
    return title, overview


def main():
    files = sorted(SRC.glob("K*.md"))
    manifest = []
    for f in files:
        kid = f.name.split("-")[0].upper()          # K01..K10
        title, overview = extract(f)
        services, tactics = RISK_MAP.get(kid, ([], []))
        checks = prowler_checks(services)
        out_name = f"{kid}-{f.name.split('-',1)[1]}"  # keep slug
        manifest.append((kid, title, len(checks), out_name))

        b = []
        b.append(f"# {title} (Kubernetes)\n")
        b.append(
            f"> **OWASP Kubernetes Top 10 (2025) · {kid}** · ID, title, and Overview "
            f"are verbatim from the official standard.\n"
            f"> Source: [`upstream/kubernetes-top-ten/2025/en/src/{f.name}`]"
            f"(../../upstream/kubernetes-top-ten/2025/en/src/{f.name})\n"
            f">\n"
            f"> **Role in this repo:** framework-agnostic Kubernetes base (a sibling of "
            f"the [cloud base](../_cloud-base/README.md)). A generated methodology "
            f"(`kubernetes/`) projects this risk onto a real cluster: the component/"
            f"sink, how to test with `kubectl`/tooling, and **positive (secure) vs "
            f"negative (vulnerable)** evidence, tied to the Prowler check that detects "
            f"it.\n"
        )
        if tactics:
            b.append(f"> **ATT&CK Containers tactics:** {', '.join(tactics)}.\n")

        b.append("## Overview (verbatim)\n")
        b.append(overview + "\n")

        b.append("## Detective coverage — Prowler `kubernetes` checks\n")
        if checks:
            b.append(f"Relevant Prowler checks (service(s): {', '.join(services)}):\n")
            b.append("| Check ID |")
            b.append("| :-- |")
            for c in checks:
                b.append(f"| `{c}` |")
            b.append("")
        else:
            b.append(
                "_No direct Prowler `kubernetes` check — this risk (cluster→cloud "
                "movement) is detected on the **cloud** side; cross-reference the "
                "[cloud base](../_cloud-base/README.md) (IMDS / instance credentials).\n")

        b.append("---\n")
        b.append(
            "### Methodology projection (filled in `kubernetes/`, not here)\n\n"
            "- **Component / sink** — the cluster object/config (Pod `securityContext`, "
            "RBAC binding, admission controller, NetworkPolicy, kubelet/apiserver flag).\n"
            "- **How to test** — `kubectl`/`kubectl-who-can`/`kube-hunter`/`kube-bench`/"
            "Peirates/`kubeletctl` enumerate then attempt.\n"
            "- **Positive (secure)** — request denied / control present.\n"
            "- **Negative (vulnerable)** — breakout/escalation succeeds; the Prowler "
            "check above flags the misconfig.\n"
        )

        text = re.sub(r"\n{3,}", "\n\n", "\n".join(b).rstrip() + "\n")
        (OUT / out_name).write_text(text, encoding="utf-8")
        print(f"wrote {out_name}  ({len(checks)} prowler checks)")

    (OUT / ".manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    print(f"\n{len(manifest)} OWASP K8s Top 10 (2025) risks")


if __name__ == "__main__":
    main()
