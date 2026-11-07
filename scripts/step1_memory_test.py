import time
from guardian.config import get_client, BANK
from guardian.memory import remember, recall_memories

client = get_client()
try:
    client.create_bank(bank_id=BANK, name=BANK)
    print("bank created")
except Exception as e:
    print("create_bank skipped:", e)   # fine if it already exists

remember("Feature 1 of the sample project lets users add a task and must always keep working.")
time.sleep(10)  # memory processing can lag behind

result = recall_memories("Which features must keep working?")
for m in result.results:
    print("-", m.text)