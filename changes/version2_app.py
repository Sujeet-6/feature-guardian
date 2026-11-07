tasks = []

def add_task(text):
    tasks.append({"text": text, "done": False})
    return list(tasks)

def delete_task(index):
    tasks.pop(index)
    return list(tasks)

def mark_done(index):
    tasks[index]["done"] = True
    return list(tasks)
