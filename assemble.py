#!/usr/bin/env python3
"""Merge AB research JSON files in .research/ into data/ab-motion-control-data.json.

Each research file holds {"families": [...], "module": {...}} except
studio5000-motion.json, which is a bare module object. The merged file is the
single source of truth for the app; www/index.html gets the data inlined at
build time so the app works offline from file://.

Seed check: the 9 Allen-Bradley seed components from the 20-platform build
(.research/ab-seed.json) must have their catalog numbers present in the
deepened family records; any missing one is appended to the family's
catalogNumbers and reported.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT / ".research"
OUT = ROOT / "data" / "ab-motion-control-data.json"

CATEGORY_ORDER = ["servo-drive", "vfd", "servo-motor", "starter"]
CATEGORY_LABELS = {
    "servo-drive": "Servo Drives",
    "vfd": "VFDs",
    "servo-motor": "Servo Motors",
    "starter": "Starters & Protection",
}
STRING_FIELDS = ["whatItIs", "whenToUse", "selection", "tuning", "manualUrl"]
LIST_FIELDS = ["catalogNumbers", "commissioning", "faults", "sources", "tbd"]
DICT_FIELDS = ["wiring"]
CONFIG_FIELDS = ["step", "screen", "parameter", "value", "source"]
FAULT_FIELDS = ["code", "meaning", "fix"]


CATEGORY_MAP = {"contactor": "starter", "protection": "starter"}


def norm_component(comp, source_file):
    comp = dict(comp)
    raw_cat = comp.get("category")
    if raw_cat in CATEGORY_MAP:
        comp["subcategory"] = raw_cat
        comp["category"] = CATEGORY_MAP[raw_cat]
    for f in STRING_FIELDS:
        if not comp.get(f):
            comp[f] = "TBD"
    for f in LIST_FIELDS:
        if not isinstance(comp.get(f), list):
            comp[f] = []
    if not isinstance(comp.get("wiring"), dict):
        comp["wiring"] = {}
    for k in ("power", "feedback", "safety", "network"):
        comp["wiring"].setdefault(k, "TBD")
    cfg = []
    for step in comp.get("configuration", []):
        step = dict(step)
        for f in CONFIG_FIELDS:
            step.setdefault(f, "TBD")
        cfg.append(step)
    comp["configuration"] = cfg
    faults = []
    for fault in comp.get("faults", []):
        fault = dict(fault)
        for f in FAULT_FIELDS:
            fault.setdefault(f, "TBD")
        faults.append(fault)
    comp["faults"] = faults
    comp["sourceFile"] = source_file
    return comp


def main():
    components, modules = [], []
    seen_ids = set()
    for fname in ("kinetix.json", "powerflex.json", "servo-motors.json",
                  "starters.json", "studio5000-motion.json"):
        path = RESEARCH / fname
        data = json.loads(path.read_text())
        if "families" in data:
            for comp in data["families"]:
                comp = norm_component(comp, fname)
                assert comp["id"] not in seen_ids, f"duplicate id {comp['id']}"
                seen_ids.add(comp["id"])
                assert comp["category"] in CATEGORY_ORDER, comp["id"]
                components.append(comp)
            modules.append(data["module"])
        else:
            modules.append(data)  # bare module (studio 5000)
    components.sort(key=lambda c: (CATEGORY_ORDER.index(c["category"]),
                                   c["family"]))

    # Seed cross-check: every seed catalog number must appear in a family.
    seed = json.loads((RESEARCH / "ab-seed.json").read_text())
    missing_seed = []
    for comp in seed["components"]:
        cat = comp.get("catalogNumber")
        if not cat:
            continue
        found = False
        for fam in components:
            if cat in fam.get("catalogNumbers", []):
                found = True
                break
        if not found:
            missing_seed.append((comp["id"], cat))
            # Attach to the family of the same name if one exists.
            for fam in components:
                if fam["family"] == comp["family"]:
                    fam["catalogNumbers"].append(cat)
                    fam.setdefault("notes", []).append(
                        f"Seed catalog number {cat} carried over from "
                        f"20-platform build (not in researcher list).")
                    found = True
                    break
            if not found:
                missing_seed[-1] = (comp["id"], cat + " (NO FAMILY MATCH)")

    stats = {
        "families": len(components),
        "modules": len(modules),
        "lessons": sum(len(m.get("lessons", [])) for m in modules),
        "quizQuestions": sum(len(m.get("quiz", [])) for m in modules),
        "configSteps": sum(len(c["configuration"]) for c in components),
        "faults": sum(len(c["faults"]) for c in components),
        "tbdItems": sum(len(c["tbd"]) for c in components)
                    + sum(len(m.get("tbd", [])) for m in modules),
        "byCategory": {cat: sum(1 for c in components if c["category"] == cat)
                       for cat in CATEGORY_ORDER},
    }
    merged = {
        "appName": "AB Motion Control App",
        "version": "1.0.0",
        "generatedFrom": ["kinetix.json", "powerflex.json",
                          "servo-motors.json", "starters.json",
                          "studio5000-motion.json"],
        "categories": [{"id": c, "label": CATEGORY_LABELS[c]}
                       for c in CATEGORY_ORDER],
        "components": components,
        "modules": modules,
        "stats": stats,
    }
    OUT.write_text(json.dumps(merged, indent=1))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print("stats:", json.dumps(stats, indent=1))
    print("missing seed catalog numbers:", missing_seed or "none")


if __name__ == "__main__":
    main()
