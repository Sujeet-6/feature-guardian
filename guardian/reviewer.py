# sends code + recalled memories to Gemini, returns accept/reject + comments
import json, re, time
from google import genai
from .config import GEMINI_API_KEY, GEMINI_MODEL

_client = None

def _get():
    global _client
    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client

def review(code, claimed_features, memories, check_summary):
    mem_block = "\n".join(f"- {m}" for m in memories) if memories else "(none - no team history available)"
    prompt = f"""You are a code review agent for a small team.

Team history recalled from memory:
{mem_block}

Automated test results for this change:
{check_summary}

Features the author says this change adds: {', '.join(claimed_features) or 'none stated'}
Each claimed feature has its own automated test, and its result is in the test results above, so never say tests are missing.
Submitted code:
{code}

Write 2 to 4 short, specific review comments. When a comment draws on the team history, end it with "(from team history)".
Reply ONLY with JSON: {{"summary": "one sentence", "comments": ["...", "..."]}}"""
    last_err = None
    models = [GEMINI_MODEL] + [m for m in ("gemini-3.5-flash-lite", "gemini-3.8-flash") if m != GEMINI_MODEL]
    for model in models:
        for _ in range(2):
            try:
                resp = _get().models.generate_content(
                    model=model, contents=prompt,
                    config={"response_mime_type": "application/json"})
                text = re.sub(r"^```(?:json)?|```$", "", resp.text.strip(), flags=re.M).strip()
                data = json.loads(text)
                return {"summary": str(data.get("summary", "")),
                        "comments": [str(c) for c in data.get("comments", [])]}
            except Exception as e:
                last_err = e
                time.sleep(2)
    return {"summary": f"(AI review unavailable: {last_err})", "comments": []}