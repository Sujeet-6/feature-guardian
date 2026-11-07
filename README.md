# Feature Guardian

**Team ABSTRACT..!**

A code review agent that remembers your team's history and protects the features that already work.

## The problem
When several people change the same codebase, one "small improvement" often silently breaks something that used to work. Reviewers forget past incidents, and AI tools review each change with no memory of the team.

## What it does
1. The agent keeps a **protected list** of features, each with its own test.
2. When someone submits a change, it first runs the test of **every protected feature**. If any fails, the change is **rejected** and the broken feature is named.
3. If all pass, it runs the tests for the features the change claims to add. Verified features are **added to the protected list**.
4. Gemini writes review comments, informed by what Hindsight remembers about the team.
5. The outcome is saved to memory, so the next review is smarter.

Accept or reject is decided by the tests. The AI comments are advice.

## How Hindsight memory is used
- **retain:** after every review, the agent saves a plain-sentence outcome (for example, a change rejected because it broke "add task"). The team's past history is also seeded into the memory bank.
- **recall:** before writing comments, the agent recalls memories relevant to the change and gives them to Gemini. Comments that use team history are tagged "(from team history)".
- **Visible before/after:** the UI has a memory on/off toggle. With memory off, the comments are generic. With memory on, they cite past rejections and team preferences.
- Memory is stored in a Hindsight Cloud bank named `abstract`.

## Data note
The team history (the "Acme" team, its past rejected changes, and its preferences) is **synthetic**, written for this demo. The sample project is a small to-do app.

## Tech
Python, Hindsight Cloud (memory), Gemini (review comments), pytest (feature checks), Streamlit (UI).

## Run it
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # fill in your Hindsight and Gemini keys
python -m scripts.seed_memory   # once, to load the sample history
streamlit run ui/app.py --server.address localhost
```
Command-line version: `python -m scripts.run_review changes/version3_app.py`

## Demo flow
1. Reset demo, load Version 2: accepted, and its new features join the protected list.
2. Load Version 3: rejected because it breaks "add task".
3. Switch memory off and review Version 2 again: generic comments. Switch it on: comments cite team history.

## How it would be used in a real team
1. **Setup:** connect the repository and mark the features that must never break, each tied to an existing test.
2. **On every pull request:** Guardian runs all protected tests on the new code. If any fails, it blocks the merge and names the broken feature. If all pass, it verifies the new features, adds them to the protected list, and posts review comments.
3. **Memory:** Hindsight stores every decision, so comments cite the team's real history and improve with each review.

**Status:** this hackathon build is a working prototype of steps 2 and 3 on a sample project, with synthetic history. Connecting it to GitHub pull requests (for example, with a GitHub Action) is the next step.
