import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import add_task, delete_task, tasks

def test_delete_task():
    tasks.clear()
    add_task("a"); add_task("b")
    assert [t["text"] for t in delete_task(0)] == ["b"]
