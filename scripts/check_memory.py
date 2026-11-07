import sys
from guardian.memory import recall_memories

query = " ".join(sys.argv[1:]) or "What has broken add task before?"
for m in recall_memories(query).results:
    print("-", m.text)
