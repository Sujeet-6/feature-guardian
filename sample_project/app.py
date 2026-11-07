tasks = []

def add_task(text):
    tasks.append({"text": text, "done": False})
    return list(tasks)
