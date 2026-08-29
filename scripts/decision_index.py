#!/usr/bin/env python3
"""
Decision-record index generator + validator for Steelyard.

Scans reports/DEC-*.md, reads their YAML-ish frontmatter (dependency-free), and writes:
  - reports/decision-index.json   (machine-readable: records, derived reverse edges, clusters, queues)
  - reports/DECISIONS.md          (human-readable: principles first, clusters, per-area, queues)

Validates on every run. Exits non-zero on a hard error (dangling citation, edge cycle, a
non-proposed record missing its kind-gated fields) so it can gate a build. See
instructions/DECISION-RECORDS.md for the contract this enforces.

No third-party dependencies — runs on a bare python3, so it ports verbatim into any repo.
"""
import json, sys, hashlib, datetime, re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REPORTS = REPO / "reports"

ID_EDGE_FIELDS = ["supersedes", "refines", "governed_by", "depends_on"]
LIST_FIELDS = ID_EDGE_FIELDS + ["areas", "cites", "revisit"]
STANCE_REQUIRED = ["evidence_basis", "evidence_level", "lineage", "contested", "contested_note"]


def parse_value(raw):
    raw = raw.strip()
    if raw == "":
        return ""
    try:
        return json.loads(raw)
    except Exception:
        return raw.strip().strip('"')


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None
    fm = {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return fm
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        fm[key.strip()] = parse_value(rest)
    return fm  # unterminated frontmatter — tolerate


def load_records():
    records, problems = {}, []
    for path in sorted(REPORTS.glob("DEC-*.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not fm or not str(fm.get("id", "")).startswith("DEC-"):
            continue
        rid = fm["id"]
        # normalise list fields
        for f in LIST_FIELDS:
            v = fm.get(f)
            if v is None:
                fm[f] = []
            elif not isinstance(v, list):
                fm[f] = [v]
        fm["_file"] = f"reports/{path.name}"
        if rid in records:
            problems.append(f"DUPLICATE id {rid} ({path.name} and {records[rid]['_file']})")
        records[rid] = fm
    return records, problems


def parse_revisit(items):
    out = []
    for it in items:
        cls, _, when = str(it).partition("|")
        out.append({"class": cls.strip(), "when": when.strip()})
    return out


def validate(records):
    hard, soft = [], []
    for rid, r in records.items():
        # dangling id-edges
        for f in ID_EDGE_FIELDS:
            for target in r[f]:
                if target not in records:
                    hard.append(f"{rid}: {f} -> unknown record '{target}' (dangling)")
        kind = r.get("kind")
        status = r.get("status")
        stub = status == "proposed" or not str(r.get("decision", "")).strip()
        if stub:
            soft.append(f"{rid}: OPEN STUB (status={status})")
        # kind-gated required fields, enforced once a record is no longer a stub
        if not stub and kind == "stance":
            missing = [k for k in STANCE_REQUIRED if r.get(k) in (None, "")]
            if missing:
                hard.append(f"{rid}: stance missing required fields: {', '.join(missing)}")
            if not any(rv["class"] == "evidence" for rv in parse_revisit(r["revisit"])):
                hard.append(f"{rid}: stance needs at least one revisit trigger of class 'evidence'")
        if not stub and kind == "design" and not str(r.get("reversal_ritual", "")).strip():
            hard.append(f"{rid}: design record missing required 'reversal_ritual'")
        if kind not in ("engineering", "stance", "design"):
            hard.append(f"{rid}: invalid kind '{kind}'")
    # cycle detection over supersedes+refines+depends_on
    graph = {rid: [t for f in ("supersedes", "refines", "depends_on") for t in r[f] if t in records]
             for rid, r in records.items()}
    WHITE, GREY, BLACK = 0, 1, 2
    color = {rid: WHITE for rid in graph}

    def dfs(u, stack):
        color[u] = GREY
        for v in graph[u]:
            if color[v] == GREY:
                hard.append(f"CYCLE: {' -> '.join(stack + [u, v])}")
            elif color[v] == WHITE:
                dfs(v, stack + [u])
        color[u] = BLACK

    for rid in graph:
        if color[rid] == WHITE:
            dfs(rid, [])
    return hard, soft


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
    # clusters: connected components over all id-edges (undirected)
    adj = {rid: set() for rid in records}
    for rid, r in records.items():
        for f in ID_EDGE_FIELDS:
            for t in r[f]:
                if t in records:
                    adj[rid].add(t)
                    adj[t].add(rid)
    cluster_of, seen = {}, set()
    for rid in sorted(records):
        if rid in seen:
            continue
        comp, stack = [], [rid]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            comp.append(u)
            stack.extend(adj[u] - seen)
        name = min(comp)  # stable representative
        for u in comp:
            cluster_of[u] = name if len(comp) > 1 else None
    return rev, cluster_of


def placement(r):
    # Constitution membership is by invariant status only. Cross-cutting-ness is carried by
    # the area tags, not by promotion here — over-promotion inflates the principles ledger.
    return "principles" if r.get("binding") is True else "area"


def build_index(records, rev, cluster_of, hard, soft):
    idx = {"generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "record_count": len(records), "records": {}, "queues": {}, "lint": {}}
    areas, principles, human, stubs, stances, contested, superseded = {}, [], [], [], [], [], []
    for rid, r in sorted(records.items()):
        place = placement(r)
        entry = {"title": r.get("title", ""), "kind": r.get("kind"), "status": r.get("status"),
                 "binding": r.get("binding", False), "placement": place, "areas": r["areas"],
                 "human_input": r.get("human_input", False), "human_crux": r.get("human_crux", ""),
                 "governed_by": r["governed_by"], "depends_on": r["depends_on"],
                 "cluster": cluster_of.get(rid), "file": r["_file"], "flags": []}
        entry.update(rev[rid])
        if r.get("human_input") is True:
            entry["flags"].append("carries_human_judgment"); human.append(rid)
        for dep in r["depends_on"]:
            if records.get(dep, {}).get("status") == "proposed":
                entry["flags"].append(f"depends_on_open_stub:{dep}")
        idx["records"][rid] = entry
        for a in r["areas"]:
            areas.setdefault(a, []).append(rid)
        if place == "principles":
            principles.append(rid)
        if r.get("status") == "proposed" or not str(r.get("decision", "")).strip():
            stubs.append(rid)
        if r.get("kind") == "stance":
            stances.append(rid)
        if r.get("contested") is True:
            contested.append(rid)
        if r.get("status") == "superseded" or rev[rid]["superseded_by"]:
            superseded.append(rid)
    idx["queues"] = {"principles": principles, "by_area": areas, "open_stubs": stubs,
                     "stances": stances, "contested": contested, "superseded": superseded,
                     "carries_human_judgment": human}
    idx["lint"] = {"errors": hard, "warnings": soft}
    src = "".join(sorted((REPORTS / Path(r["_file"]).name).read_text(encoding="utf-8")
                         for r in records.values()))
    idx["input_hash"] = hashlib.sha256(src.encode()).hexdigest()[:16]
    return idx


def write_human(idx, records):
    L = []
    L.append(f"# {REPO.name} — Decisions (generated)\n")
    L.append(f"*Generated {idx['generated_at']} · {idx['record_count']} records · "
             f"input-hash `{idx['input_hash']}`. Do not edit — regenerate with "
             "`python3 scripts/decision_index.py`.*\n")
    err = idx["lint"]["errors"]
    if err:
        L.append("## ⚠ Lint errors (build-failing)\n")
        L += [f"- {e}" for e in err] + [""]
    if idx["queues"]["open_stubs"]:
        L.append("## ⚠ Open items\n")
        L += [f"- `{r}` — {idx['records'][r]['title']}" for r in idx["queues"]["open_stubs"]] + [""]

    def line(rid):
        e = idx["records"][rid]
        crux = f" — _human crux:_ {e['human_crux']}" if e["human_input"] and e["human_crux"] else ""
        return f"- `{rid}` **{e['title']}** · {e['kind']}/{e['status']}{crux}"

    L.append("## Principles (the constitution — read first)\n")
    L += [line(r) for r in idx["queues"]["principles"]] + [""]
    clusters = {}
    for rid, e in idx["records"].items():
        if e["cluster"]:
            clusters.setdefault(e["cluster"], []).append(rid)
    if clusters:
        L.append("## Clusters (read these together)\n")
        for name, ids in sorted(clusters.items()):
            L.append(f"**{name}**")
            L += [line(r) for r in sorted(ids)] + [""]
    L.append("## By area\n")
    for area, ids in sorted(idx["queues"]["by_area"].items()):
        L.append(f"**{area}** — " + ", ".join(f"`{r}`" for r in sorted(ids)))
    L.append("")
    if idx["queues"]["carries_human_judgment"]:
        L.append("## Carries human judgment (non-derivable — read before overturning)\n")
        L += [line(r) for r in idx["queues"]["carries_human_judgment"]] + [""]
    if idx["queues"]["stances"] or idx["queues"]["contested"]:
        L.append("## Stances / contested (weigh the evidence before relying)\n")
        for r in sorted(set(idx["queues"]["stances"] + idx["queues"]["contested"])):
            L.append(line(r))
        L.append("")
    return "\n".join(L)


def main():
    records, problems = load_records()
    hard, soft = validate(records)
    hard = problems + hard
    rev, cluster_of = derive(records)
    idx = build_index(records, rev, cluster_of, hard, soft)
    (REPORTS / "decision-index.json").write_text(json.dumps(idx, indent=2), encoding="utf-8")
    (REPORTS / "DECISIONS.md").write_text(write_human(idx, records), encoding="utf-8")
    print(f"Scanned {len(records)} records. "
          f"{len(idx['queues']['principles'])} principles, "
          f"{len(soft)} warnings, {len(hard)} errors.")
    for e in hard:
        print("  ERROR:", e)
    for w in soft:
        print("  warn :", w)
    print("Wrote reports/decision-index.json and reports/DECISIONS.md")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
