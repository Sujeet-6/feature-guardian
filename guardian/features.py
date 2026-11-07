# read/write features.json (the protected list)
import json, os

PATH = "features.json"

def load():
    if not os.path.exists(PATH):
        return []
    with open(PATH) as f:
        return json.load(f)

def save(items):
    with open(PATH, "w") as f:
        json.dump(items, f, indent=2)

def add(name, test):
    items = load()
    if not any(i["name"] == name for i in items):
        items.append({"name": name, "test": test})
        save(items)