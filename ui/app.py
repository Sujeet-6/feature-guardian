# simple page for the demo (built last)
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import streamlit as st
from guardian.engine import review_change
from guardian import features as feats

st.set_page_config(page_title="Feature Guardian", layout="wide")

SAMPLES = {
    "v2": ("changes/version2_app.py", "delete task:test_delete_task.py, mark done:test_mark_done.py"),
    "v3": ("changes/version3_app.py", ""),
}

def load_sample(key):
    path, fts = SAMPLES[key]
    with open(path) as f:
        st.session_state.code = f.read()
    st.session_state.features = fts
    st.session_state.pop("result", None)

def reset_demo():
    import glob
    for f in glob.glob("feature_tests/*.py"):
        if os.path.basename(f) != "test_feature1.py":
            os.remove(f)
    feats.save([{"name": "add task", "test": "test_feature1.py"}])
    st.session_state.pop("result", None)

def parse(s):
    out = []
    for part in [p.strip() for p in s.split(",") if p.strip()]:
        name, test = part.split(":")
        out.append({"name": name.strip(), "test": test.strip()})
    return out

st.session_state.setdefault("code", "")
st.session_state.setdefault("features", "")

st.title("Feature Guardian")
st.caption("A code review agent that remembers your team's history and protects the features that already work. Team ABSTRACT..!")

with st.sidebar:
    st.header("Controls")
    memory_on = st.toggle("Use Hindsight memory", value=True)
    apply = st.checkbox("Save outcome (update protected list and memory)", value=True)
    st.button("Reset demo", on_click=reset_demo)
    st.divider()
    protected_box = st.container()

st.write("**Load a sample change:**")
b1, b2, _ = st.columns([1, 1, 4])
b1.button("Version 2 (adds features)", on_click=load_sample, args=("v2",))
b2.button("Version 3 (breaks a feature)", on_click=load_sample, args=("v3",))

st.text_area("Submitted code", key="code", height=260)
st.text_input("Features this change adds (name:testfile, comma separated)", key="features")

if st.button("Review change", type="primary"):
    try:
        new = parse(st.session_state.features)
    except ValueError:
        st.error("Use the format  name:testfile, name:testfile")
        new = None
    if new is not None and st.session_state.code.strip():
        with st.spinner("Checking protected features and recalling memory..."):
            st.session_state.result = review_change(
                st.session_state.code, new, memory_on=memory_on, apply=apply)

r = st.session_state.get("result")
if r:
    if r["decision"] == "ACCEPT":
        st.success(f"ACCEPTED - {r['reason']}")
    else:
        st.error(f"REJECTED - {r['reason']}")
    left, right = st.columns(2)
    with left:
        st.subheader("Feature checklist")
        for x in r["protected"]:
            st.write(("✅ " if x["passed"] else "❌ ") + x["name"] + " (protected)")
        for x in r["new"]:
            st.write(("✅ " if x["passed"] else "❌ ") + x["name"] + " (new)")
        for x in r["protected"] + r["new"]:
            if not x["passed"]:
                with st.expander(f"Why {x['name']} failed"):
                    st.code(x["output"])
        st.subheader("Review comments")
        st.write(r["ai"]["summary"])
        for c in r["ai"]["comments"]:
            st.markdown(f"- {c}")
    with right:
        st.subheader(f"Memory recalled ({'on' if r['memory_on'] else 'off'})")
        if r["memories"]:
            for m in r["memories"]:
                st.markdown(f"- {m}")
        else:
            st.info("Memory is off, so this review had no team history.")

with protected_box:
    st.subheader("Protected features")
    for f in feats.load():
        st.write("🛡️ " + f["name"])