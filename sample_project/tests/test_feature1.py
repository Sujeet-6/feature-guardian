import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import add_task, tasks

def test_add_task():
    tasks.clear()
    result = add_task("buy milk")
    assert result[0]["text"] == "buy milk"
