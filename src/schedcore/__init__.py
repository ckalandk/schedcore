from .scheduler import Scheduler
from .task import Task
from .threadPool import ThreadPool

from importlib import metadata

try:
    __version__ = metadata.version("schedcore")
except metadata.PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["Scheduler", "Task", "ThreadPool"]
