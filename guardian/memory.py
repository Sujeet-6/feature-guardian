from .config import get_client, BANK

def remember(text):
    return get_client().retain(bank_id=BANK, content=text)

def recall_memories(query):
    return get_client().recall(bank_id=BANK, query=query)
