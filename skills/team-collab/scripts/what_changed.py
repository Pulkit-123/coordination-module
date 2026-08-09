#!/usr/bin/env python3
"""Pull out the parts of a diff that change what the software can *do*.

Someone who can't read code can't review a diff — so they don't, and the
documented result is that security properties an experienced developer would
enforce by habit simply never get checked. The way round it isn't to teach them
to read diffs. It's to describe the change in terms they *can* judge: who can now
see what, what leaves the machine, what gets deleted.

This finds the signals. Turning them into a sentence someone can react to is the
model's job — "this now lets anyone with the link read every entry" is a review a
non-developer can actually perform.

Usage:
  what_changed.py                 unstaged + staged changes
  what_changed.py --staged        staged only
  what_changed.py --since <ref>   everything since a commit or branch
"""

import re
import subprocess
import sys

# Each signal is something a non-developer can form an opinion about, phrased as
# the question they should be asked. Anything they can't judge is left out —
# refactors, naming, formatting — because listing those trains them to skim.
SIGNALS = [
    ("who can get in", [
        (r"\bauth\w*\s*[:=(]|requireAuth|isAuthenticated|checkPermission|"
         r"authorize|\bcan[A-Z]\w*|\brole\b|\bisAdmin\b|middleware", None),
        (r"enable\s+row\s+level\s+security|create\s+policy|drop\s+policy", None),
        (r"\bpublic\b\s*[:=]\s*true|allowAnonymous|\bskipAuth\b", None),
    ]),
    ("what leaves this machine", [
        (r"\bfetch\s*\(|axios\.|requests\.(?:get|post|put|delete)|http\.request|"
         r"urllib|HttpClient|\bcurl\b", None),
        (r"https?://(?!localhost|127\.0\.0\.1)[a-z0-9.-]+", None),
    ]),
    ("what gets stored or deleted", [
        (r"create\s+table|alter\s+table|drop\s+table|add\s+column|drop\s+column", None),
        (r"\.(?:delete|destroy|remove|drop)\s*\(|DELETE\s+FROM|TRUNCATE", None),
        (r"localStorage|sessionStorage|\.cookie\b|document\.cookie", None),
    ]),
    ("money", [
        (r"stripe|paypal|checkout|\bprice\b|\bcharge\b|subscription|billing|invoice", None),
    ]),
    ("who can be contacted", [
        (r"sendmail|nodemailer|sendgrid|twilio|\bsms\b|push_notification|"
         r"webhook|\bnotify\b", None),
    ]),
    ("what runs on its own", [
        (r"cron|setInterval|schedule|\bqueue\b|worker|background_task|celery", None),
    ]),
]


def run(*args):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=25)
        return r.stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def get_diff():
    if "--since" in sys.argv:
        i = sys.argv.index("--since")
        ref = sys.argv[i + 1] if len(sys.argv) > i + 1 else "HEAD~1"
        return run("git", "diff", f"{ref}...HEAD", "-U0")
    if "--staged" in sys.argv:
        return run("git", "diff", "--cached", "-U0")
    d = run("git", "diff", "-U0")
    return d + run("git", "diff", "--cached", "-U0")


def main():
    diff = get_diff()
    if not diff.strip():
        print("no changes to describe")
        return 0

    added = []
    current_file = None
    files = set()
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue
        if line.startswith("+") and not line.startswith("+++"):
            body = line[1:].strip()
            if len(body) > 3 and not body.startswith(("//", "#", "*", "/*")):
                added.append((current_file, body))
                if current_file:
                    files.add(current_file)

    if not added:
        print("no added lines to describe")
        return 0

    found = {}
    for label, patterns in SIGNALS:
        hits = []
        for path, body in added:
            for pattern, _ in patterns:
                if re.search(pattern, body, re.I):
                    hits.append((path, body[:120]))
                    break
        if hits:
            found[label] = hits[:5]

    print(f"{len(added)} lines added across {len(files)} file(s).\n")

    if not found:
        print("Nothing here changes who can access what, what leaves the machine,")
        print("or what gets stored — looks like internal changes only.")
        return 0

    print("Things worth describing in plain language before this ships:\n")
    for label, hits in found.items():
        print(f"  {label}:")
        for path, body in hits:
            print(f"    {path}: {body}")
        print()

    print("Now say what this MEANS, not what it does. The test is whether someone")
    print("who can't read code could disagree with your sentence.")
    print()
    print("  good: \"anyone with the link can now read every entry, including")
    print("         other people's\"")
    print("  bad:  \"added a GET /entries route with no auth middleware\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
