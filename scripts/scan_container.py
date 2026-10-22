"""Scan a local image without mounting the Docker socket or application credentials."""

import argparse
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Trivy 0.75.0, from the official release; refresh deliberately with reviewed evidence.
SCANNER = "aquasec/trivy:0.75.0@sha256:af6acf9a6b85dfe389a1941505c0ce9efef52a4719635e1a962f022a3d855daa"


def run(command):
    subprocess.run(command, cwd=ROOT, check=True, timeout=900)


def findings_markdown(manifest):
    grouped = {}
    for finding in manifest["blockers"]:
        group = grouped.setdefault(
            finding["id"],
            {"severity": finding["severity"], "packages": set(), "fixed": set()},
        )
        group["packages"].add(finding["package"] or finding["target"])
        if finding["fixed"]:
            group["fixed"].add(finding["fixed"])
    lines = [
        "# Container security findings",
        "",
        f"Scan: {manifest['generated_at']}.",
        f"Image: `{manifest['image_id']}`.",
        f"Scanner: `{manifest['scanner']}`.",
        "",
        f"Gate: {'PASS' if manifest['passed'] else 'FAIL'}. "
        f"{len(manifest['blockers'])} high/critical package findings; {len(grouped)} distinct finding IDs.",
        "These are scanner classifications, not independently established application exploit paths.",
        "No exceptions are accepted. No reported fixed version does not mean that no upstream patch exists.",
        "",
        "| Severity | Finding | Affected packages | Fixed versions reported |",
        "|---|---|---|---|",
    ]
    for key, group in sorted(
        grouped.items(), key=lambda item: (item[1]["severity"] != "CRITICAL", item[0])
    ):
        lines.append(
            f"| {group['severity']} | {key} | {', '.join(sorted(group['packages']))} | {', '.join(sorted(group['fixed'])) or 'None for this release'} |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="enat:release")
    args = parser.parse_args()
    output = ROOT / "artifacts/security"
    cache = ROOT / ".cache/trivy"
    output.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)
    metadata = json.loads(
        subprocess.check_output(["docker", "image", "inspect", args.image], text=True)
    )[0]
    if metadata["Config"].get("User") != "10001:10001":
        raise SystemExit("Runtime must run as the dedicated non-root user")
    with tempfile.TemporaryDirectory(prefix="enat-image-") as temporary:
        archive = Path(temporary) / "image.tar"
        run(["docker", "image", "save", args.image, "-o", str(archive)])
        scanner = [
            "docker",
            "run",
            "--rm",
            "--user",
            f"{os.getuid()}:{os.getgid()}",
            "--cap-drop=ALL",
            "--security-opt=no-new-privileges",
            "-v",
            f"{temporary}:/work:ro",
            "-v",
            f"{output}:/reports",
            "-v",
            f"{cache}:/cache",
            SCANNER,
        ]
        run(
            [
                *scanner,
                "image",
                "--cache-dir",
                "/cache",
                "--timeout",
                "12m",
                "--input",
                "/work/image.tar",
                "--scanners",
                "vuln,secret",
                "--format",
                "json",
                "--output",
                "/reports/container.json",
            ]
        )
        run(
            [
                *scanner,
                "convert",
                "--format",
                "cyclonedx",
                "--output",
                "/reports/container.cdx.json",
                "/reports/container.json",
            ]
        )
    report = json.loads((output / "container.json").read_text())
    if not report.get("Metadata", {}).get("OS", {}).get("Family"):
        raise SystemExit("Container OS scan evidence missing")
    blockers = []
    for result in report.get("Results", []):
        for finding in result.get("Vulnerabilities", []) + result.get("Secrets", []):
            if finding.get("Severity") in ("HIGH", "CRITICAL"):
                blockers.append(
                    {
                        "target": result["Target"],
                        "id": finding.get("VulnerabilityID", finding.get("RuleID")),
                        "package": finding.get("PkgName"),
                        "installed": finding.get("InstalledVersion"),
                        "fixed": finding.get("FixedVersion"),
                        "severity": finding["Severity"],
                    }
                )
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "image_id": metadata["Id"],
        "scanner": SCANNER,
        "passed": not blockers,
        "blockers": blockers,
    }
    (output / "container-gate.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (output / "container-findings.md").write_text(findings_markdown(manifest))
    print(
        f"Container scan: {len(blockers)} high/critical blockers; reports in {output}"
    )
    raise SystemExit(int(bool(blockers)))


if __name__ == "__main__":
    main()
