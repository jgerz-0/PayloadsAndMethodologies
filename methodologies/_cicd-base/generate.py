#!/usr/bin/env python3
"""Generate the _cicd-base/ from the OWASP Top 10 CI/CD Security Risks.

CI/CD / SCM platforms (GitHub, GitLab, Jenkins, ...) aren't covered by ASVS,
MASVS, ATT&CK-cloud, or the K8s Top 10, so they get their own base anchored on
the recognized standard — the **OWASP Top 10 CI/CD Security Risks** (vendored at
`upstream/cicd-top-10`) — cross-referenced to **Prowler** `github` checks where
the platform is GitHub.

Risk IDs, titles, and the Definition text are copied verbatim from OWASP; the
Prowler-check mapping is this repo's curation. Only the chrome is house style.
"""
import re, pathlib, json, glob

ROOT = pathlib.Path("/home/udc/Documents/PayloadsAndMethodologies")
SRC = ROOT / "upstream/cicd-top-10"
PROWLER_GH = ROOT / "upstream/prowler/prowler/providers/github/services"
OUT = ROOT / "methodologies/_cicd-base"
OUT.mkdir(parents=True, exist_ok=True)

# CICD-SEC number -> Prowler github check IDs that evidence it (GitHub only)
GH_MAP = {
    "1": ["repository_default_branch_protection_enabled",
          "repository_default_branch_requires_multiple_approvals",
          "repository_default_branch_status_checks_required",
          "organization_actions_pull_request_approval_disabled"],
    "2": ["organization_members_mfa_required",
          "organization_default_repository_permission_strict",
          "repository_default_branch_protection_applies_to_admins"],
    "3": ["repository_dependency_scanning_enabled"],
    "4": ["organization_default_workflow_permissions_read_only",
          "repository_default_workflow_permissions_read_only",
          "githubactions_workflow_security_scan"],
    "5": ["repository_default_workflow_permissions_read_only",
          "organization_default_workflow_permissions_read_only"],
    "6": ["repository_secret_scanning_enabled"],
    "7": ["repository_default_branch_requires_signed_commits",
          "repository_default_branch_requires_linear_history",
          "repository_default_branch_disallows_force_push"],
    "8": ["organization_repository_creation_limited",
          "organization_default_repository_permission_strict"],
    "9": ["repository_default_branch_requires_signed_commits",
          "repository_immutable_releases_enabled"],
    "10": [],   # audit logging — no direct Prowler github check
}


def extract(md_path):
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'title:\s*"([^"]+)"', text)
    title = m.group(1).strip() if m else md_path.stem
    md = re.search(r"##\s*Definition\s*(.+?)(?:\n##\s)", text, re.DOTALL)
    definition = ""
    if md:
        paras = [p.strip() for p in re.split(r"\n\s*\n", md.group(1).strip()) if p.strip()]
        definition = "\n\n".join(paras[:2])
    return title, definition


def main():
    files = sorted(SRC.glob("CICD-SEC-*.md"))
    manifest = []
    for f in files:
        num = re.search(r"CICD-SEC-0?(\d+)", f.name).group(1)
        sec = f"CICD-SEC-{num}"
        title, definition = extract(f)
        checks = GH_MAP.get(num, [])
        out_name = f.name
        manifest.append((sec, title, len(checks), out_name))

        b = []
        b.append(f"# {title} (CI/CD)\n")
        b.append(
            f"> **OWASP Top 10 CI/CD Security Risks · {sec}** · ID, title, and "
            f"Definition are verbatim from the official standard.\n"
            f"> Source: [`upstream/cicd-top-10/{f.name}`](../../upstream/cicd-top-10/{f.name})\n"
            f">\n"
            f"> **Role in this repo:** framework-agnostic CI/CD base. A generated "
            f"methodology ([`github/`](../github/README.md), [`gitlab/`](../gitlab/README.md)) "
            f"projects this risk onto the platform: the concrete setting/sink, how to "
            f"test it, and **positive (secure) vs negative (vulnerable)** evidence, tied "
            f"to the Prowler `github` check where applicable.\n"
        )
        b.append("## Definition (verbatim)\n")
        b.append(definition + "\n")
        b.append("## Detective coverage — Prowler `github` checks\n")
        if checks:
            b.append("| Check ID |")
            b.append("| :-- |")
            for c in checks:
                b.append(f"| `{c}` |")
            b.append("")
        else:
            b.append("_No direct Prowler `github` check — verify via platform audit-log "
                     "settings / API._\n")
        b.append("---\n")
        b.append(
            "### Methodology projection (filled per platform, not here)\n\n"
            "- **Setting / sink** — the concrete platform control (branch protection, "
            "runner config, token scope, OIDC trust, webhook, workflow permissions).\n"
            "- **How to test** — the API/UI check or attack (e.g. open a PR that edits "
            "the pipeline file; request the repo's secrets via a poisoned workflow).\n"
            "- **Positive (secure)** — control enforced / action blocked.\n"
            "- **Negative (vulnerable)** — pipeline runs attacker code / secret exfils; "
            "the Prowler check above (GitHub) flags the gap.\n"
        )

        text = re.sub(r"\n{3,}", "\n\n", "\n".join(b).rstrip() + "\n")
        (OUT / out_name).write_text(text, encoding="utf-8")
        print(f"wrote {out_name}  ({len(checks)} github checks)")

    (OUT / ".manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    print(f"\n{len(manifest)} OWASP CI/CD Security Risks")


if __name__ == "__main__":
    main()
