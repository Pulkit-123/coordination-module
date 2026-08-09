#!/usr/bin/env python3
"""Catch the handful of things that are catastrophic and unrecoverable.

Aimed at someone who cannot review code. Rescue engineers who rebuild AI-built
apps report the same seven patterns over and over: exposed keys, fake auth, zero
error handling, race conditions, broken payments, unvalidated inputs,
unmaintainable code. Most of those are judgment calls. A few are not, and those
few are the ones that end up in the news:

  - a real credential committed to git (irreversible the moment it is pushed)
  - Supabase tables with row-level security never switched on (this exact
    mistake exposed 1.5M API tokens and 35k email addresses in Feb 2026)
  - a migration that drops or truncates without a filter
  - an auth check that returns true no matter what

Deliberately narrow. Everything here is either a genuine emergency or silence —
a checker that cries wolf gets ignored, and then the real one is ignored too.

Usage:
  safety_check.py            check staged changes, or the working tree
  safety_check.py --all      check every tracked file
"""

import os
import re
import subprocess
import sys

SKIP_DIRS = {".git", "node_modules", "dist", "build", "target", ".next",
             "venv", ".venv", "__pycache__", "vendor", ".terraform"}
TEXT_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".rs", ".go", ".rb", ".java",
            ".kt", ".swift", ".php", ".vue", ".svelte", ".sql", ".env", ".yml",
            ".yaml", ".json", ".toml", ".sh", ".tf", ".md", ""}

# Real-looking credentials. Prefixes are provider-specific on purpose: generic
# "password=" patterns match test fixtures constantly and train people to ignore
# the output.
SECRETS = [
    (r"sk-[A-Za-z0-9]{20,}", "an OpenAI-style secret key"),
    (r"sk-ant-[A-Za-z0-9_-]{20,}", "an Anthropic API key"),
    (r"ghp_[A-Za-z0-9]{30,}", "a GitHub personal access token"),
    (r"gho_[A-Za-z0-9]{30,}", "a GitHub OAuth token"),
    (r"AKIA[0-9A-Z]{16}", "an AWS access key id"),
    (r"AIza[0-9A-Za-z_-]{30,}", "a Google API key"),
    (r"xox[baprs]-[0-9A-Za-z-]{10,}", "a Slack token"),
    (r"sk_live_[0-9A-Za-z]{20,}", "a live Stripe secret key"),
    (r"rk_live_[0-9A-Za-z]{20,}", "a live Stripe restricted key"),
    # Supabase replaced JWT service-role keys with these. Found by running this
    # against a real project whose most dangerous credential was invisible to
    # every pattern above. `sb_publishable_` is deliberately public and is NOT
    # listed — flagging it would be a false alarm.
    (r"sb_secret_[A-Za-z0-9_-]{16,}", "a Supabase secret key (full database access)"),
    (r"gsk_[A-Za-z0-9]{30,}", "a Groq API key"),
    (r"hf_[A-Za-z0-9]{30,}", "a Hugging Face token"),
    (r"xai-[A-Za-z0-9]{30,}", "an xAI API key"),
    (r"pplx-[A-Za-z0-9]{30,}", "a Perplexity API key"),
    (r"glpat-[A-Za-z0-9_-]{15,}", "a GitLab personal access token"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "a private key"),
    (r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
     "a JWT (check whether it's a real service token)"),
]

PLACEHOLDER = re.compile(
    r"your[_-]?key|example|placeholder|xxx+|<[^>]+>|change[_-]?me|dummy|sample|"
    r"todo|fake|test[_-]?key|\.\.\.",
    re.I,
)


def run(*args):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=20)
        return r.stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def in_repo():
    return bool(run("git", "rev-parse", "--git-dir").strip())


def files_to_check(check_all):
    if not in_repo():
        out = []
        for dp, dn, fn in os.walk("."):
            dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".")]
            out += [os.path.join(dp, f) for f in fn]
        return out
    if check_all:
        names = run("git", "ls-files").splitlines()
    else:
        names = run("git", "diff", "--cached", "--name-only").splitlines()
        if not names:
            names = run("git", "diff", "--name-only").splitlines()
        if not names:
            names = run("git", "ls-files").splitlines()
    return [n for n in names if n]


def readable(path):
    if not os.path.isfile(path):
        return None
    base = os.path.basename(path)
    # Extension matching alone misses the single most important file: for
    # `.env.local` splitext returns `.local`, so the place Next.js actually keeps
    # secrets was being skipped silently. Check the name too.
    env_like = base.startswith(".env") or base in (
        "credentials", "secrets", ".npmrc", ".netrc", ".pypirc",
    )
    if not env_like and os.path.splitext(path)[1] not in TEXT_EXT:
        return None
    try:
        if os.path.getsize(path) > 400_000:
            return None
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return None


def is_env_file(path):
    b = os.path.basename(path)
    return b.startswith(".env") or b in ("credentials", "secrets", ".npmrc",
                                         ".netrc", ".pypirc")


def check_secrets(path, text, stop, warn):
    # An env file is *where secrets are supposed to live*. Flagging one for
    # containing a key blocks correct work, which is how a checker teaches people
    # to ignore it — verified against a real project whose keys were properly
    # stored and gitignored. The genuine risk is the file being committed, and
    # that's checked separately.
    if is_env_file(path):
        return
    for pattern, what in SECRETS:
        for m in re.finditer(pattern, text):
            line_no = text[:m.start()].count("\n") + 1
            line = text.splitlines()[line_no - 1] if line_no <= len(text.splitlines()) else ""
            if PLACEHOLDER.search(line):
                continue
            snippet = m.group(0)[:12] + "…"
            stop.append(
                f"{path}:{line_no} looks like {what} ({snippet}).\n"
                f"      Once this is pushed it is public forever — rotating the key is the\n"
                f"      only real fix, deleting the commit is not enough. Move it to .env\n"
                f"      and make sure .env is in .gitignore."
            )
            return


def check_env_unignored(stop):
    """An env file git isn't ignoring is one bad `git add .` from being public."""
    if not in_repo():
        return
    for dp, dn, fn in os.walk("."):
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".")]
        for f in fn:
            if not is_env_file(f) or "example" in f or "sample" in f or "template" in f:
                continue
            path = os.path.join(dp, f)
            out = run("git", "check-ignore", path).strip()
            if out:
                continue
            if run("git", "ls-files", "--error-unmatch", path).strip():
                continue  # already tracked; reported by the other check
            stop.append(
                f"{path} is not in .gitignore.\n"
                f"      It holds your keys and git isn't ignoring it, so one `git add .`\n"
                f"      puts them on GitHub permanently. Add this line to .gitignore:\n"
                f"        {f}"
            )


def check_env_tracked(stop):
    if not in_repo():
        return
    tracked = run("git", "ls-files").splitlines()
    for f in tracked:
        base = os.path.basename(f)
        if base == ".env" or (base.startswith(".env.") and "example" not in base
                              and "sample" not in base and "template" not in base):
            stop.append(
                f"{f} is tracked by git.\n"
                f"      That file is meant to hold your secrets and stay off GitHub.\n"
                f"      Add it to .gitignore and run: git rm --cached {f}"
            )


def check_supabase_rls(path, text, stop, warn):
    if not path.endswith(".sql"):
        return
    creates = re.findall(r"create\s+table\s+(?:if\s+not\s+exists\s+)?"
                         r"[\"']?(?:public\.)?([A-Za-z_][\w]*)", text, re.I)
    if not creates:
        return
    enabled = {t.lower() for t in re.findall(
        r"alter\s+table\s+[\"']?(?:public\.)?([A-Za-z_][\w]*)[\"']?\s+enable\s+row\s+level\s+security",
        text, re.I)}
    missing = [t for t in creates if t.lower() not in enabled]
    if missing and re.search(r"supabase|auth\.uid\(\)|anon|service_role", text, re.I):
        stop.append(
            f"{path} creates {', '.join(missing[:4])} without enabling row level security.\n"
            f"      On Supabase this means anyone holding the public anon key can read and\n"
            f"      write those tables directly, bypassing your app entirely. This exact\n"
            f"      mistake leaked 1.5M API tokens and 35k emails in February 2026.\n"
            f"      Fix: alter table <name> enable row level security; then add policies."
        )


def check_destructive_sql(path, text, warn):
    if os.path.splitext(path)[1] not in {".sql", ".py", ".js", ".ts", ".rb", ".go"}:
        return
    for pattern, what in (
        (r"\bdrop\s+table\b(?!\s+if\s+exists\s+\w*temp)", "drops a table"),
        (r"\btruncate\s+table\b", "empties a table completely"),
        (r"\bdelete\s+from\s+[\w.\"']+\s*;", "deletes every row (no WHERE clause)"),
        (r"\bupdate\s+[\w.\"']+\s+set\b(?![^;]*\bwhere\b)", "updates every row (no WHERE clause)"),
    ):
        m = re.search(pattern, text, re.I)
        if m:
            line_no = text[:m.start()].count("\n") + 1
            warn.append(
                f"{path}:{line_no} {what}.\n"
                f"      Fine against a fresh database, unrecoverable against a real one\n"
                f"      with people's data in it. Check which you're pointed at."
            )
            break


def check_fake_auth(path, text, warn):
    if os.path.splitext(path)[1] not in {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rb"}:
        return
    for m in re.finditer(
        r"(?:function|def|const|async)\s+\w*(?:auth|login|verify|isAdmin|"
        r"checkPermission|requireAuth|authorize)\w*\s*[\(=][^\n]{0,80}",
        text, re.I,
    ):
        tail = text[m.end():m.end() + 260]
        if re.search(r"^\s*[\{:\)]?\s*(?:return\s+)?(?:true|True|1)\s*[;\n}]", tail) or \
           re.search(r"return\s+(?:true|True)\s*[;\n}]\s*\}", tail[:80]):
            line_no = text[:m.start()].count("\n") + 1
            warn.append(
                f"{path}:{line_no} an auth check that always succeeds.\n"
                f"      Often a placeholder from early development that never got replaced.\n"
                f"      If this is live, everyone is an admin."
            )
            return


def main():
    check_all = "--all" in sys.argv
    stop, warn = [], []

    check_env_tracked(stop)
    check_env_unignored(stop)
    for path in files_to_check(check_all):
        text = readable(path)
        if text is None:
            continue
        check_secrets(path, text, stop, warn)
        check_supabase_rls(path, text, stop, warn)
        check_destructive_sql(path, text, warn)
        check_fake_auth(path, text, warn)

    if not stop and not warn:
        return 0

    if stop:
        print("STOP — these are not recoverable once shipped:\n")
        for s in stop:
            print(f"  !!  {s}\n")
    if warn:
        print("Worth a look before this goes anywhere real:\n")
        for w in warn:
            print(f"  ?   {w}\n")

    return 2 if stop else 0


if __name__ == "__main__":
    sys.exit(main())
