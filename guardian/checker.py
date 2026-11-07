# runs the test of every protected feature on a submitted change
import os, shutil, subprocess, sys, tempfile

TEST_DIR = "feature_tests"

def run_test(code, test_file, test_dir=TEST_DIR, timeout=30):
    """Run one test file against the submitted code. Returns (passed, output)."""
    path = os.path.join(test_dir, test_file)
    if not os.path.exists(path):
        return False, f"test file not found: {path}"
    d = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(d, "tests"))
        with open(os.path.join(d, "app.py"), "w") as f:
            f.write(code)
        shutil.copy(path, os.path.join(d, "tests", test_file))
        p = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider",
             os.path.join("tests", test_file)],
            cwd=d, capture_output=True, text=True, timeout=timeout)
        out = "\n".join((p.stdout + p.stderr).strip().splitlines()[-6:])
        return p.returncode == 0, out
    except subprocess.TimeoutExpired:
        return False, "test timed out"
    finally:
        shutil.rmtree(d, ignore_errors=True)

def run_checks(code, items, test_dir=TEST_DIR):
    results = []
    for it in items:
        ok, out = run_test(code, it["test"], test_dir)
        results.append({"name": it["name"], "test": it["test"], "passed": ok, "output": out})
    return results