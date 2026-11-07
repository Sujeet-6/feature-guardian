# main flow: checker -> recall -> reviewer -> decision -> update list + remember
import os, shutil
from . import features as feats
from .checker import run_checks, TEST_DIR
from .memory import remember, recall_memories
from .reviewer import review

NEW_TESTS_DIR = os.path.join("changes", "new_tests")

def _recall(claimed_names):
    query = ("What has broken protected features before, and what does the team expect in code reviews? "
             + " ".join(claimed_names))
    try:
        seen, out = set(), []
        for m in recall_memories(query).results:
            t = m.text.strip()
            if t and t not in seen:
                seen.add(t)
                out.append(t)
        return out[:8]
    except Exception as e:
        print("memory recall failed:", e)
        return []

def review_change(code, new_features, memory_on=True, apply=True):
    """new_features: list of {"name": ..., "test": <file in changes/new_tests>}"""
    claimed = [f["name"] for f in new_features]

    protected = run_checks(code, feats.load())
    broken = [p for p in protected if not p["passed"]]

    new_results = []
    if not broken:
        new_results = run_checks(code, new_features, test_dir=NEW_TESTS_DIR)
    new_broken = [n for n in new_results if not n["passed"]]

    if broken:
        decision = "REJECT"
        reason = "Broke protected feature(s): " + ", ".join(b["name"] for b in broken)
        note = f"A change was rejected because it broke the protected feature {', '.join(b['name'] for b in broken)}."
    elif new_broken:
        decision = "REJECT"
        reason = "Claimed feature(s) do not work: " + ", ".join(n["name"] for n in new_broken)
        note = f"A change claiming to add {', '.join(n['name'] for n in new_broken)} was rejected because the new feature's own test failed."
    else:
        decision = "ACCEPT"
        reason = "All protected features pass" + (" and new features verified." if claimed else ".")
        added = f"added {', '.join(claimed)} and was accepted" if claimed else "was accepted"
        note = f"A change that {added} because every protected feature still passed."

    memories = _recall(claimed) if memory_on else []
    summary = "\n".join(f"{'PASS' if r['passed'] else 'FAIL'}: {r['name']}" for r in protected + new_results)
    ai = review(code, claimed, memories, summary)

    if apply:
        if decision == "ACCEPT":
            os.makedirs(TEST_DIR, exist_ok=True)
            for f in new_features:
                shutil.copy(os.path.join(NEW_TESTS_DIR, f["test"]), os.path.join(TEST_DIR, f["test"]))
                feats.add(f["name"], f["test"])
        try:
            remember(note)
        except Exception as e:
            print("could not save memory:", e)

    return {"decision": decision, "reason": reason, "protected": protected,
            "new": new_results, "memories": memories, "ai": ai, "memory_on": memory_on}