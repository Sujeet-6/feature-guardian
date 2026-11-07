import glob, json, os

for f in glob.glob("feature_tests/*.py"):
    if os.path.basename(f) != "test_feature1.py":
        os.remove(f)
with open("features.json", "w") as f:
    json.dump([{"name": "add task", "test": "test_feature1.py"}], f, indent=2)
print("demo reset: protected list is back to 1 feature")