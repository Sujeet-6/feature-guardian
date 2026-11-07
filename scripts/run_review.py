import argparse
from guardian.engine import review_change

p = argparse.ArgumentParser()
p.add_argument("file")
p.add_argument("--features", default="", help='"delete task:test_delete_task.py,mark done:test_mark_done.py"')
p.add_argument("--no-memory", action="store_true")
p.add_argument("--dry-run", action="store_true")
a = p.parse_args()

new = []
for part in filter(None, a.features.split(",")):
    name, test = part.split(":")
    new.append({"name": name.strip(), "test": test.strip()})

r = review_change(open(a.file).read(), new, memory_on=not a.no_memory, apply=not a.dry_run)

print("\nProtected features:")
for x in r["protected"]:
    print(f"  {'PASS' if x['passed'] else 'FAIL'}  {x['name']}")
if r["new"]:
    print("New features:")
    for x in r["new"]:
        print(f"  {'PASS' if x['passed'] else 'FAIL'}  {x['name']}")
print(f"\nDECISION: {r['decision']} - {r['reason']}")
print(f"\nMemories used ({'on' if r['memory_on'] else 'off'}): {len(r['memories'])}")
for m in r["memories"]:
    print("  -", m)
print("\nReview:", r["ai"]["summary"])
for c in r["ai"]["comments"]:
    print("  *", c)