#!/usr/bin/env python3
# cruxton-managed: scripts/decision_index.py — regenerate/upgrade via bootstrap.py; local edits are overwritten.
"""
Cruxton — decision-record index generator + strict validator (dependency-free).

Scans reports/DEC-*.md, reads YAML-ish frontmatter AND body, and writes:
  - reports/decision-index.json   machine: records + derived reverse edges + clusters + queues
  - reports/DECISIONS.md          human: principles first, clusters, per-area, live vs superseded

Validates on every run and exits non-zero on any hard error, so it can gate a build.
Output is DETERMINISTIC (no wall-clock in the artifacts; identity is the input hash), written
atomically. Run with --check to verify committed artifacts are current without rewriting them
(for CI). See instructions/DECISION-RECORDS.md for the contract this enforces.

No third-party dependencies — runs on a bare python3, so it ports verbatim into any repo.
"""
import json, sys, re, hashlib, os, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORTS = REPO / "reports"
NAME_FILE = REPO / ".decision-records-name"  # committed project name for the ledger title


def project_name():
    """The ledger's project name, from a COMMITTED file — never the live checkout path, so the
    title is deterministic across machines and CI. bootstrap seeds it (default: the repo folder
    name); edit .decision-records-name to rename. Absent → a neutral, path-independent title."""
    try:
        return NAME_FILE.read_text(encoding="utf-8").strip() or None
    except OSError:
        return None

STATUSES = {"proposed", "accepted", "superseded", "rejected"}
KINDS = {"engineering", "stance", "design"}
CONFIDENCES = {"high", "moderate", "low"}
REVISIT_CLASSES = {"internal", "evidence", "values", "none"}
EVIDENCE_BASIS = {"causal", "predictive", "mechanistic", "measurement"}
EVIDENCE_LEVEL = {"guideline", "systematic-review", "single-study", "expert-opinion"}

ID_EDGE_FIELDS = ["supersedes", "refines", "governed_by", "depends_on"]
LIST_FIELDS = ID_EDGE_FIELDS + ["areas", "cites", "revisit"]
STANCE_REQUIRED = ["evidence_basis", "evidence_level", "lineage", "contested", "contested_note"]

REQUIRED_GENERIC = ["id", "question", "title", "status", "binding", "kind", "areas",
                    "decided_on", "decision", "confidence", "human_input", "revisit"]
KNOWN_KEYS = set(REQUIRED_GENERIC) | set(ID_EDGE_FIELDS) | {
    "human_crux", "cites", "enforced_by",
    "evidence_basis", "evidence_level", "lineage", "contested", "contested_note",
    "reversal_ritual"}

ID_RE = re.compile(r"^DEC-[a-z0-9]+(?:-[a-z0-9]+)*$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_BODY = ["Question", "Decision", "Why"]


def parse_value(raw):
    raw = raw.strip()
    if raw == "":
        return ""
    try:
        return json.loads(raw)
    except Exception:
        return raw.strip().strip('"')


def split_doc(text):
    """Return (frontmatter_dict, body_text, structural_errors). frontmatter is None if absent."""
    errs = []
    if not text.startswith("---"):
        return None, text, ["no frontmatter (file must start with '---')"]
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, text, ["no frontmatter (first line is not '---')"]
    fm, seen = {}, set()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errs.append(f"frontmatter line {i+1} has no 'key:' — orphan/continuation line: {line.strip()!r}")
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        if key in seen:
            errs.append(f"duplicate frontmatter key '{key}'")
        seen.add(key)
        fm[key] = parse_value(rest)
    if end is None:
        errs.append("frontmatter is not terminated with a closing '---'")
        body = ""
    else:
        body = "\n".join(lines[end + 1:])
    return fm, body, errs


def load_records():
    records, structural = {}, []
    for path in sorted(REPORTS.glob("DEC-*.md")):
        rel = f"reports/{path.name}"
        fm, body, errs = split_doc(path.read_text(encoding="utf-8"))
        for e in errs:
            structural.append(f"{rel}: {e}")
        if fm is None:
            continue
        rid = str(fm.get("id", ""))
        if not rid:
            structural.append(f"{rel}: missing 'id' — a DEC-*.md file with no id is invisible; fix or remove it")
            continue
        if not ID_RE.match(rid):
            structural.append(f"{rel}: id '{rid}' is not a valid slug id (^DEC-[a-z0-9-]+$)")
        expected = f"reports/{rid}.md"
        if rel != expected:
            structural.append(f"{rel}: filename does not match id '{rid}' (expected {expected})")
        for f in LIST_FIELDS:
            v = fm.get(f)
            if v is None:
                fm[f] = []
            elif not isinstance(v, list):
                fm[f] = [v]
        fm["_file"] = rel
        fm["_body"] = body
        if rid in records:
            structural.append(f"DUPLICATE id {rid} ({rel} and {records[rid]['_file']})")
        records[rid] = fm
    return records, structural


def parse_revisit(items):
    out = []
    for it in items:
        cls, _, when = str(it).partition("|")
        out.append({"class": cls.strip(), "when": when.strip()})
    return out


def is_stub(r):
    return r.get("status") == "proposed" or not str(r.get("decision", "")).strip()


def valid_date(s):
    if not isinstance(s, str) or not DATE_RE.match(s):
        return False
    try:
        datetime.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def has_section(body, name):
    return re.search(rf"(?m)^##\s+{re.escape(name)}\b", body or "") is not None


def validate(records, structural):
    hard = list(structural)
    soft = []
    superseded_by = {rid: [] for rid in records}
    for rid, r in records.items():
        for t in r["supersedes"]:
            if t in superseded_by:
                superseded_by[t].append(rid)

    for rid, r in sorted(records.items()):
        def err(m): hard.append(f"{rid}: {m}")
        def warn(m): soft.append(f"{rid}: {m}")

        for k in REQUIRED_GENERIC:
            if k not in r or (isinstance(r.get(k), str) and r.get(k).strip() == "" and k != "decision"):
                if k in ("areas", "revisit"):
                    if not r.get(k):
                        err(f"missing required field '{k}'")
                elif k not in r:
                    err(f"missing required field '{k}'")
        for k in r:
            if k.startswith("_"):
                continue
            if k not in KNOWN_KEYS:
                warn(f"unknown frontmatter key '{k}' (typo? or add it to the vocabulary)")

        if "question" in r and not SLUG_RE.match(str(r.get("question", "x"))):
            err(f"question '{r.get('question')}' is not a valid slug")
        if r.get("status") not in STATUSES:
            err(f"invalid status '{r.get('status')}' (must be one of {sorted(STATUSES)})")
        if not isinstance(r.get("binding"), bool):
            err(f"binding must be a boolean true/false, got {r.get('binding')!r}")
        if not isinstance(r.get("human_input"), bool):
            err(f"human_input must be a boolean true/false, got {r.get('human_input')!r}")
        kind = r.get("kind")
        if kind not in KINDS:
            err(f"invalid kind '{kind}' (must be one of {sorted(KINDS)})")
        if r.get("confidence") not in CONFIDENCES:
            err(f"invalid confidence '{r.get('confidence')}' (must be one of {sorted(CONFIDENCES)})")
        if not valid_date(r.get("decided_on")):
            err(f"decided_on '{r.get('decided_on')}' is not a valid YYYY-MM-DD date")
        if not all(isinstance(a, str) and SLUG_RE.match(a) for a in r.get("areas", [])):
            err(f"areas must be a non-empty list of slug strings, got {r.get('areas')!r}")
        for rv in parse_revisit(r["revisit"]):
            if rv["class"] not in REVISIT_CLASSES:
                err(f"revisit class '{rv['class']}' invalid (must be one of {sorted(REVISIT_CLASSES)})")

        stub = is_stub(r)
        if stub:
            soft.append(f"{rid}: OPEN STUB (status={r.get('status')})")
            if r.get("status") == "accepted":
                err("status is 'accepted' but 'decision' is empty")

        if not stub:
            for sec in REQUIRED_BODY:
                if not has_section(r["_body"], sec):
                    err(f"body is missing required section '## {sec}'")

        if r.get("human_input") is True:
            if not str(r.get("human_crux", "")).strip():
                err("human_input is true but human_crux is empty")
            if not has_section(r["_body"], "Human reasoning"):
                err("human_input is true but body has no '## Human reasoning' section")
        elif str(r.get("human_crux", "")).strip():
            warn("human_crux is set but human_input is false")

        # kind-gated
        if not stub and kind == "stance":
            missing = [k for k in STANCE_REQUIRED if r.get(k) in (None, "")]
            if missing:
                err(f"stance missing required fields: {', '.join(missing)}")
            if r.get("evidence_basis") not in EVIDENCE_BASIS | {None}:
                err(f"stance evidence_basis '{r.get('evidence_basis')}' invalid (one of {sorted(EVIDENCE_BASIS)})")
            if r.get("evidence_level") not in EVIDENCE_LEVEL | {None}:
                err(f"stance evidence_level '{r.get('evidence_level')}' invalid (one of {sorted(EVIDENCE_LEVEL)})")
            if r.get("contested") is True and not str(r.get("contested_note", "")).strip():
                err("stance is contested: true but contested_note is empty")
            if not any(rv["class"] == "evidence" for rv in parse_revisit(r["revisit"])):
                err("stance needs at least one revisit trigger of class 'evidence'")
        if not stub and kind == "design":
            if not str(r.get("reversal_ritual", "")).strip():
                err("design record missing required 'reversal_ritual'")
            if not r["governed_by"]:
                warn("design record has no governed_by — a design decision usually serves a principle")

        # edges
        for f in ID_EDGE_FIELDS:
            for t in r[f]:
                if t not in records:
                    err(f"{f} -> unknown record '{t}' (dangling)")
        for t in r["supersedes"]:
            if t in records and records[t].get("question") != r.get("question"):
                err(f"supersedes '{t}' but their questions differ "
                    f"({r.get('question')!r} vs {records[t].get('question')!r}) — a reversal answers the SAME question")
        # cites: free-form evidence, but a cite that looks like a record id must resolve
        for t in r["cites"]:
            if isinstance(t, str) and ID_RE.match(t) and t not in records:
                err(f"cites record '{t}' which does not exist")

    # one live decision per question (the silent-contradiction guard)
    by_q = {}
    for rid, r in records.items():
        by_q.setdefault(r.get("question"), []).append(rid)
    for q, ids in by_q.items():
        live = [i for i in ids if records[i].get("status") == "accepted" and not superseded_by.get(i)]
        if len(live) > 1:
            hard.append(f"question '{q}' has {len(live)} live accepted records ({', '.join(sorted(live))}) "
                        f"— supersede the older one, or they are different questions")

    # cycle detection over supersedes+refines+depends_on
    graph = {rid: [t for f in ("supersedes", "refines", "depends_on") for t in r[f] if t in records]
             for rid, r in records.items()}
    color = {rid: 0 for rid in graph}

    def dfs(u, stack):
        color[u] = 1
        for v in graph[u]:
            if color[v] == 1:
                hard.append(f"CYCLE: {' -> '.join(stack + [u, v])}")
            elif color[v] == 0:
                dfs(v, stack + [u])
        color[u] = 2

    for rid in graph:
        if color[rid] == 0:
            dfs(rid, [])
    return hard, soft, superseded_by


def derive(records):
    rev = {rid: {"superseded_by": [], "refined_by": [], "governs": [], "depended_on_by": [], "cited_by": []}
           for rid in records}
    back = {"supersedes": "superseded_by", "refines": "refined_by",
            "governed_by": "governs", "depends_on": "depended_on_by"}
    for rid, r in records.items():
        for f, bf in back.items():
            for t in r[f]:
                if t in rev:
                    rev[t][bf].append(rid)
        for t in r["cites"]:
            if t in rev:
                rev[t]["cited_by"].append(rid)
    adj = {rid: set() for rid in records}
    for rid, r in records.items():
        for f in ID_EDGE_FIELDS:
            for t in r[f]:
                if t in records:
                    adj[rid].add(t); adj[t].add(rid)
    cluster_of, seen = {}, set()
    for rid in sorted(records):
        if rid in seen:
            continue
        comp, stack = [], [rid]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u); comp.append(u)
            stack.extend(adj[u] - seen)
        name = min(comp)
        for u in comp:
            cluster_of[u] = name if len(comp) > 1 else None
    return rev, cluster_of


def placement(r):
    return "principles" if r.get("binding") is True else "area"


def build_index(records, rev, cluster_of, superseded_by, hard, soft):
    idx = {"schema": 2, "record_count": len(records), "records": {}, "queues": {}, "lint": {}}
    areas, principles, human, stubs, stances, contested, superseded, questions = {}, [], [], [], [], [], [], {}
    for rid, r in sorted(records.items()):
        place = placement(r)
        is_sup = r.get("status") == "superseded" or bool(superseded_by.get(rid))
        live = r.get("status") == "accepted" and not superseded_by.get(rid)
        entry = {"title": r.get("title", ""), "question": r.get("question"),
                 "kind": r.get("kind"), "status": r.get("status"),
                 "effective_status": "superseded" if is_sup else r.get("status"), "live": live,
                 "binding": r.get("binding", False), "placement": place, "areas": r["areas"],
                 "decision": r.get("decision", ""), "confidence": r.get("confidence"),
                 "decided_on": r.get("decided_on"),
                 "human_input": r.get("human_input", False), "human_crux": r.get("human_crux", ""),
                 "supersedes": r["supersedes"], "refines": r["refines"],
                 "governed_by": r["governed_by"], "depends_on": r["depends_on"],
                 "cites": r["cites"], "revisit": parse_revisit(r["revisit"]),
                 "cluster": cluster_of.get(rid), "file": r["_file"], "flags": []}
        for k in ("evidence_basis", "evidence_level", "lineage", "contested", "contested_note", "reversal_ritual"):
            if k in r:
                entry[k] = r[k]
        entry.update(rev[rid])
        if r.get("human_input") is True:
            entry["flags"].append("carries_human_judgment"); human.append(rid)
        for dep in r["depends_on"]:
            if records.get(dep, {}).get("status") == "proposed":
                entry["flags"].append(f"depends_on_open_stub:{dep}")
        idx["records"][rid] = entry
        for a in r["areas"]:
            areas.setdefault(a, []).append(rid)
        questions.setdefault(r.get("question"), []).append(rid)
        if place == "principles" and live:
            principles.append(rid)
        if is_stub(r):
            stubs.append(rid)
        if r.get("kind") == "stance":
            stances.append(rid)
        if r.get("contested") is True:
            contested.append(rid)
        if is_sup:
            superseded.append(rid)
    idx["queues"] = {"principles": principles, "by_area": areas, "by_question": questions,
                     "open_stubs": stubs, "stances": stances, "contested": contested,
                     "superseded": superseded, "carries_human_judgment": human}
    idx["lint"] = {"errors": hard, "warnings": soft}
    src = "".join(sorted((REPORTS / Path(r["_file"]).name).read_text(encoding="utf-8")
                         for r in records.values()))
    idx["input_hash"] = hashlib.sha256(src.encode()).hexdigest()[:16]
    return idx


def ledger_href(file):
    """A DEC record's href AS WRITTEN IN reports/DECISIONS.md. The `file` field is repo-root-
    relative (e.g. 'reports/DEC-foo.md') — correct for JSON consumers, who resolve from the repo
    root — but GitHub renders a relative link from the directory of the file it appears in, and
    DECISIONS.md itself lives in reports/, so a 'reports/…' href would resolve to reports/reports/…
    (404). Emit the path relative to reports/ instead: a bare 'DEC-foo.md', since the records are
    siblings of the ledger."""
    return os.path.relpath(REPO / file, REPORTS).replace(os.sep, "/")


def write_human(idx):
    R = idx["records"]
    name = project_name()
    L = [(f"# {name} — Decisions (generated)" if name else "# Decisions (generated)") + "\n"]
    L.append(f"*{idx['record_count']} records · input-hash `{idx['input_hash']}`. "
             "Generated by `scripts/decision_index.py` — do not edit; regenerate instead.*\n")
    err = idx["lint"]["errors"]
    if err:
        L.append("## ⚠ Lint errors (build-failing)\n")
        L += [f"- {e}" for e in err] + [""]
    if idx["queues"]["open_stubs"]:
        L.append("## ⚠ Open items\n")
        L += [f"- `{r}` — {R[r]['title']}" for r in idx["queues"]["open_stubs"]] + [""]

    def line(rid, show_decision=True):
        e = R[rid]
        mark = "" if e["live"] else " · _superseded_"
        crux = f"  \n  _human crux:_ {e['human_crux']}" if e["human_input"] and e["human_crux"] else ""
        dec = f"  \n  {e['decision']}" if show_decision and e["decision"] else ""
        return (f"- [`{rid}`]({ledger_href(e['file'])}) **{e['title']}** · {e['kind']}/{e['status']}"
                f" · conf:{e['confidence']}{mark}{dec}{crux}")

    L.append("## Principles (the constitution — read first)\n")
    L += ([line(r) for r in idx["queues"]["principles"]] or ["_none_"]) + [""]
    clusters = {}
    for rid, e in R.items():
        if e["cluster"]:
            clusters.setdefault(e["cluster"], []).append(rid)
    if clusters:
        L.append("## Clusters (read these together)\n")
        for name, ids in sorted(clusters.items()):
            L.append(f"**{name}**")
            L += [line(r, show_decision=False) for r in sorted(ids)] + [""]
    L.append("## By area\n")
    for area, ids in sorted(idx["queues"]["by_area"].items()):
        L.append(f"**{area}** — " + ", ".join(f"`{r}`" for r in sorted(ids)))
    L.append("")
    if idx["queues"]["carries_human_judgment"]:
        L.append("## Carries human judgment (non-derivable — read before overturning)\n")
        L += [line(r) for r in idx["queues"]["carries_human_judgment"]] + [""]
    if idx["queues"]["stances"] or idx["queues"]["contested"]:
        L.append("## Stances / contested (weigh the evidence before relying)\n")
        L += [line(r) for r in sorted(set(idx["queues"]["stances"] + idx["queues"]["contested"]))] + [""]
    if idx["queues"]["superseded"]:
        L.append("## Superseded (historical trail — kept, not live)\n")
        L += [line(r, show_decision=False) for r in idx["queues"]["superseded"]] + [""]
    return "\n".join(L)


def generate():
    records, structural = load_records()
    hard, soft, superseded_by = validate(records, structural)
    rev, cluster_of = derive(records)
    idx = build_index(records, rev, cluster_of, superseded_by, hard, soft)
    return idx, json.dumps(idx, indent=2, ensure_ascii=False) + "\n", write_human(idx), hard, soft


def atomic_write(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def main():
    check = "--check" in sys.argv[1:]
    idx, json_text, human_text, hard, soft = generate()
    json_path = REPORTS / "decision-index.json"
    md_path = REPORTS / "DECISIONS.md"

    if check:
        stale = []
        for p, want in ((json_path, json_text), (md_path, human_text)):
            have = p.read_text(encoding="utf-8") if p.exists() else None
            if have != want:
                stale.append(p.name)
        if stale:
            print(f"--check: STALE generated files: {', '.join(stale)}. Run: python3 scripts/decision_index.py")
            sys.exit(1)
        if hard:
            print(f"--check: {len(hard)} lint error(s).")
            for e in hard:
                print("  ERROR:", e)
            sys.exit(1)
        print(f"--check: OK — artifacts current, {len(records_count(idx))} records, 0 errors.")
        sys.exit(0)

    atomic_write(json_path, json_text)
    atomic_write(md_path, human_text)
    print(f"Scanned {idx['record_count']} records. "
          f"{len(idx['queues']['principles'])} live principles, {len(soft)} warnings, {len(hard)} errors.")
    for e in hard:
        print("  ERROR:", e)
    for w in soft:
        print("  warn :", w)
    print("Wrote reports/decision-index.json and reports/DECISIONS.md")
    sys.exit(1 if hard else 0)


def records_count(idx):
    return idx["records"]


if __name__ == "__main__":
    main()
