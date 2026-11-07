from concurrent.futures import ThreadPoolExecutor
from hindsight_client import Hindsight
from .config import BASE_URL, API_KEY, BANK

def _in_thread(fn):
    def work():
        client = Hindsight(base_url=BASE_URL, api_key=API_KEY)
        try:
            return fn(client)
        finally:
            try:
                client.close()
            except Exception:
                pass
    with ThreadPoolExecutor(max_workers=1) as ex:
        return ex.submit(work).result()

def remember(text):
    """Save one plain-sentence memory."""
    return _in_thread(lambda c: c.retain(bank_id=BANK, content=text))

def recall_memories(query):
    """Search memory for anything relevant to the query."""
    return _in_thread(lambda c: c.recall(bank_id=BANK, query=query))