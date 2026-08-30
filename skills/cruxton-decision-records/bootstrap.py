#!/usr/bin/env python3
"""
Bootstrap the Cruxton decision-records system into a target repo — safely, then verify honestly.

    python3 bootstrap.py [TARGET_DIR] [--dry-run] [--force] [--upgrade-spec]

Guarantees:
  * Non-destructive. It only writes files it owns (marked `cruxton-managed`) or files that do
    not yet exist. A same-named file it does NOT own is a collision: it refuses and reports,
    rather than overwriting your work (override with --force).
  * Atomic. Every file is written to a temp path then moved into place.
  * Truthful. The self-check prints SELF-CHECK PASSED only when the generator exits 0 (machinery
    installed AND records valid). Lint errors in existing records are reported and exit non-zero.
  * Honest versioning. The version stamp reflects the spec actually present, never a newer number
    than the spec in the repo. Upgrade the spec explicitly with --upgrade-spec.

--dry-run prints the plan and writes nothing.
"""
import sys, re, shutil, subprocess, os
from pathlib import Path

METHOD = Path(__file__).resolve().parent
TEMPLATES = METHOD / "templates"
GEN_MARKER = "cruxton-managed"
POINTER_MARKER = "instructions/DECISION-RECORDS.md"
PI_MARKER = "Decision records — read this system first"
VERSION_RE = re.compile(r"cruxton-method-version:\s*([0-9]+\.[0-9]+\.[0-9]+)")


def spec_version(text):
    m = VERSION_RE.search(text or "")
    return m.group(1) if m else None


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    force = "--force" in args
    upgrade_spec = "--upgrade-spec" in args
    pos = [a for a in args if not a.startswith("--")]
    target = Path(pos[0]).resolve() if pos else Path.cwd()
    shipped = (METHOD / "METHOD-VERSION").read_text(encoding="utf-8").strip()
    spec_tmpl = (TEMPLATES / "DECISION-RECORDS.template.md").read_text(encoding="utf-8")
    shipped_spec_v = spec_version(spec_tmpl) or shipped

    print(f"Cruxton bootstrap (method v{shipped}) → {target}" + ("   [DRY RUN]" if dry else ""))
    actions, refusals = [], []

    def write(rel, text):
        p = target / rel
        if dry:
            actions.append(f"write {rel}"); return
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, p)
        actions.append(f"write {rel}")

    if not dry:
        for d in ("instructions", "scripts", "reports"):
            (target / d).mkdir(parents=True, exist_ok=True)

    # 1. Spec — never clobber a customised spec. Upgrade only on explicit request.
    spec = target / "instructions" / "DECISION-RECORDS.md"
    stamp_version = shipped_spec_v
    if not spec.exists():
        write("instructions/DECISION-RECORDS.md", spec_tmpl)
        actions[-1] += "  (customise section 9)"
    else:
        cur = spec.read_text(encoding="utf-8")
        cur_v = spec_version(cur)
        stamp_version = cur_v or shipped_spec_v
        if cur_v and cur_v != shipped_spec_v and upgrade_spec:
            if not dry:
                shutil.copyfile(spec, spec.with_suffix(".md.bak"))
                write("instructions/DECISION-RECORDS.md", spec_tmpl)
            actions.append(f"UPGRADE spec {cur_v} -> {shipped_spec_v} (backed up to .md.bak; re-apply your section 9)")
            stamp_version = shipped_spec_v
        elif cur_v and cur_v != shipped_spec_v:
            actions.append(f"skip  spec (v{cur_v}; upstream v{shipped_spec_v} — run --upgrade-spec to migrate)")
        else:
            actions.append("skip  instructions/DECISION-RECORDS.md (present)")

    # 2. Generator — cruxton-managed machinery: refresh if absent or owned; refuse a foreign file.
    gen = target / "scripts" / "decision_index.py"
    gen_tmpl = (TEMPLATES / "decision_index.py").read_text(encoding="utf-8")
    if gen.exists() and GEN_MARKER not in gen.read_text(encoding="utf-8") and not force:
        refusals.append("scripts/decision_index.py exists and is not Cruxton-managed — refusing to overwrite "
                        "(use --force to replace it)")
    else:
        write("scripts/decision_index.py", gen_tmpl)

    # 3 & 4. Pointer files for both agent surfaces — create, or append the pointer once.
    for fname, tmpl in (("CLAUDE.md", "CLAUDE.md.template"), ("AGENTS.md", "AGENTS.md.template")):
        p = target / fname
        pointer = (TEMPLATES / tmpl).read_text(encoding="utf-8")
        if not p.exists():
            write(fname, pointer)
        elif POINTER_MARKER not in p.read_text(encoding="utf-8"):
            if not dry:
                write(fname, p.read_text(encoding="utf-8").rstrip() + "\n\n" + pointer)
            else:
                actions.append(f"append {fname} (pointer)")
        else:
            actions.append(f"skip  {fname} (pointer present)")

    # 5. project-instructions.md — prepend the pointer once, only if the file exists.
    pi = target / "instructions" / "project-instructions.md"
    if pi.exists():
        text = pi.read_text(encoding="utf-8")
        if PI_MARKER not in text:
            snippet = (TEMPLATES / "project-instructions-snippet.md").read_text(encoding="utf-8")
            write("instructions/project-instructions.md", snippet.rstrip() + "\n\n" + text)
        else:
            actions.append("skip  project-instructions.md (pointer present)")

    # 5.5 Project name for the ledger title — write once (default: the repo folder name), never
    #     clobber. Keeps the DECISIONS.md title deterministic across checkouts (it is read from this
    #     committed file, not the live path). Edit .decision-records-name to rename the ledger.
    name_file = target / ".decision-records-name"
    if not name_file.exists():
        write(".decision-records-name", target.name + "\n")
    else:
        actions.append("skip  .decision-records-name (present)")

    # 6. Version stamp — reflects the spec actually present.
    write(".decision-records-version", stamp_version + "\n")
    actions[-1] = f"stamp .decision-records-version = {stamp_version}"

    for a in actions:
        print("  ", a)
    for r in refusals:
        print("   REFUSED:", r)
    if refusals and not force:
        print("Bootstrap stopped without writing over your files. Resolve the collisions above or re-run with --force.")
        sys.exit(3)
    if dry:
        print("Dry run — nothing written.")
        sys.exit(0)

    # 7. Honest self-check: install is proven by running the generator.
    print("Self-check: running the generator ...")
    r = subprocess.run([sys.executable, str(gen)], cwd=str(target), capture_output=True, text=True)
    out = (r.stdout.strip() or r.stderr.strip())
    print("   " + out.replace("\n", "\n   "))
    index_ok = (target / "reports" / "decision-index.json").exists() and \
               (target / "reports" / "DECISIONS.md").exists()
    if not index_ok or r.returncode >= 2:
        print("SELF-CHECK FAILED — generator did not produce the index. Nothing was left partially "
              "written; inspect scripts/decision_index.py and re-run.")
        sys.exit(2)
    if r.returncode == 1:
        print(f"SETUP OK — Cruxton v{stamp_version} machinery is installed, but existing records have lint "
              "errors (above). Fix them, then commit. (This is not a bootstrap failure.)")
        sys.exit(1)
    print(f"SELF-CHECK PASSED — Cruxton v{stamp_version} is live in {target.name}.")
    print("Next: read reports/DECISIONS.md, then record decisions per instructions/DECISION-RECORDS.md.")
    sys.exit(0)


if __name__ == "__main__":
    main()
