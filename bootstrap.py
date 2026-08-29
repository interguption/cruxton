#!/usr/bin/env python3
"""
Bootstrap the decision-records system into a target repo — deterministically, then self-verify.

    python3 bootstrap.py [TARGET_DIR]      # default: current directory

Idempotent: safe to re-run. It refreshes the generator (machinery, safe to update) and
re-stamps the method version, but never clobbers an existing spec or any record. The
"can't be done wrong" guarantee is that setup is executed and then checked, not transcribed:
the final self-check fails loudly if anything is missing.
"""
import sys
import shutil
import subprocess
from pathlib import Path

METHOD = Path(__file__).resolve().parent
TEMPLATES = METHOD / "templates"


def main():
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    version = (METHOD / "METHOD-VERSION").read_text(encoding="utf-8").strip()
    print(f"Bootstrapping decision-records v{version} into {target}")

    for d in ("instructions", "scripts", "reports"):
        (target / d).mkdir(parents=True, exist_ok=True)

    actions = []

    # 1. Spec — never clobber (it is customised per repo, section 9).
    spec = target / "instructions" / "DECISION-RECORDS.md"
    if spec.exists():
        actions.append("skip  instructions/DECISION-RECORDS.md (exists)")
    else:
        shutil.copyfile(TEMPLATES / "DECISION-RECORDS.template.md", spec)
        actions.append("write instructions/DECISION-RECORDS.md  (customise section 9)")

    # 2. Generator — always refresh; it is machinery, and updating it is intended on re-run.
    shutil.copyfile(TEMPLATES / "decision_index.py", target / "scripts" / "decision_index.py")
    actions.append("write scripts/decision_index.py")

    # 3. CLAUDE.md — create, or append the pointer once (idempotent via a marker).
    claude = target / "CLAUDE.md"
    pointer = (TEMPLATES / "CLAUDE.md.template").read_text(encoding="utf-8")
    marker = "instructions/DECISION-RECORDS.md"
    if not claude.exists():
        claude.write_text(pointer, encoding="utf-8")
        actions.append("write CLAUDE.md")
    elif marker not in claude.read_text(encoding="utf-8"):
        claude.write_text(claude.read_text(encoding="utf-8").rstrip() + "\n\n" + pointer, encoding="utf-8")
        actions.append("append CLAUDE.md (pointer)")
    else:
        actions.append("skip  CLAUDE.md (pointer present)")

    # 4. project-instructions.md — prepend the pointer once, only if the file exists.
    pi = target / "instructions" / "project-instructions.md"
    if pi.exists():
        text = pi.read_text(encoding="utf-8")
        if "Decision records — read this system first" not in text:
            snippet = (TEMPLATES / "project-instructions-snippet.md").read_text(encoding="utf-8")
            pi.write_text(snippet.rstrip() + "\n\n" + text, encoding="utf-8")
            actions.append("prepend instructions/project-instructions.md (pointer)")
        else:
            actions.append("skip  project-instructions.md (pointer present)")

    # 5. Version stamp.
    (target / ".decision-records-version").write_text(version + "\n", encoding="utf-8")
    actions.append(f"stamp .decision-records-version = {version}")

    for a in actions:
        print("  ", a)

    # 6. Self-check: run the generator. It exits 0 (clean) or 1 (record-level lint errors);
    #    either means it ran. A crash (>=2) or a missing index is a bootstrap failure.
    print("Self-check: running the generator ...")
    gen = target / "scripts" / "decision_index.py"
    r = subprocess.run([sys.executable, str(gen)], cwd=str(target), capture_output=True, text=True)
    print("   " + (r.stdout.strip() or r.stderr.strip()).replace("\n", "\n   "))
    index_ok = (target / "reports" / "decision-index.json").exists() and \
               (target / "reports" / "DECISIONS.md").exists()
    ran_ok = r.returncode in (0, 1)
    if ran_ok and index_ok:
        print(f"SELF-CHECK PASSED — decision-records v{version} is live in {target.name}.")
        print("Next: read reports/DECISIONS.md, then record decisions per instructions/DECISION-RECORDS.md.")
        sys.exit(0)
    print("SELF-CHECK FAILED — generator did not produce the index. Nothing partial was left in an "
          "unusable state; inspect scripts/decision_index.py and re-run.")
    sys.exit(2)


if __name__ == "__main__":
    main()
