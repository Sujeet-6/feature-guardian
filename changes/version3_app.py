tasks = []

def add_task(text):
    tasks.append({"text": text, "done": False})
    # refactor: the return value was dropped by mistake

def delete_task(index):
    tasks.pop(index)
    return list(tasks)

def mark_done(index):
    tasks[index]["done"] = True
    return list(tasks)
