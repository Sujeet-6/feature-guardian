import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import add_task, mark_done, tasks

def test_mark_done():
    tasks.clear()
    add_task("a")
    assert mark_done(0)[0]["done"] is True
