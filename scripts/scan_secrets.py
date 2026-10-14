"""High-signal local secret scan. Reports locations, never matching values.

This is a repository/history check, not a substitute for deployed secret audits.
"""

import re
import subprocess
from pathlib import Path

PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(
        r"(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,})"
    ),
    "supabase-secret": re.compile(r"sb_secret_[A-Za-z0-9_-]{20,}"),
    "aws-access-key": re.compile(r"AKIA[A-Z0-9]{16}"),
    "openai-secret": re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{40,}"),
    "jwt-literal": re.compile(
        r"eyJ[A-Za-z0-9_-]{12,}\.eyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{20,}"
    ),
}


def main():
    findings = []
    files = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
        )
        .decode()
        .split("\0")
    )
    for name in files:
        path = Path(name)
        if not name or not path.is_file() or path.is_symlink():
            continue
        for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            for kind, pattern in PATTERNS.items():
                if pattern.search(line):
                    findings.append(f"{name}:{number}: {kind}")
    history = subprocess.check_output(
        ["git", "log", "--all", "-p", "--no-ext-diff", "--format=commit:%H"]
    ).decode(errors="replace")
    commit = "unknown"
    for line in history.splitlines():
        if line.startswith("commit:"):
            commit = line[7:19]
        for kind, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append(f"history {commit}: {kind}")
    for finding in sorted(set(findings)):
        print(finding)
    print(f"Secret-pattern scan: {len(set(findings))} findings (values redacted)")
    return bool(findings)


if __name__ == "__main__":
    raise SystemExit(main())
