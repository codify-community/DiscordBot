import os
import psutil
def get_current_memory_usage_by_python() -> str:
    """
    Returns the current memory usage of the process in MB.
    """
    process = psutil.Process(os.getpid())
    return "{:.2f}".format(process.memory_info().rss / 1024 / 1024)