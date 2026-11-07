import time
from guardian.memory import remember

with open("data/seed_notes.txt") as f:
    notes = [l.strip() for l in f if l.strip() and not l.startswith("#")]

for i, note in enumerate(notes, 1):
    remember(note)
    print(f"{i}/{len(notes)} saved")
    time.sleep(1)
print("done - wait a minute or two for processing before recalling")
