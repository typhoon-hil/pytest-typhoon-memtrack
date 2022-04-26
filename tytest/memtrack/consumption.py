import psutil


def get_memory_consumption(pid):
    current_process = psutil.Process(pid)
    memory_percent = current_process.memory_percent()
    memory_total = float(current_process.memory_info().rss) / 1048576
    for child_process in current_process.children(recursive=True):
        memory_percent += child_process.memory_percent()
        memory_total += float(child_process.memory_info().rss) / 1048576
    return memory_total, memory_percent


def get_cpu_percent(pid):
    current_process = psutil.Process(pid)
    cpu_percent = current_process.cpu_percent(interval=1)
    for child_process in current_process.children(recursive=True):
        cpu_percent += child_process.cpu_percent(interval=1)
    return cpu_percent
