from collections.abc import Callable
from functools import partial
from typing import Any
from datetime import timedelta


class Task:
    """
    Represents a task to be executed by the Scheduler.

    The Task class encapsulates a callable and its arguments, along with
    timeout and repeat.

    Attributes:
        interval (timedelta | float): The delay before the task should execute,
            Pass a float for seconds, or a timedelta for explicit units.
        repeat (bool): If True, the task will be rescheduled after execution
            using the same interval.
        func (Callable): The function or executable to be run.
        args (tuple): Positional arguments to pass to the function.
        kwargs (dict): Keyword arguments to pass to the function.
    """

    def __init__(
        self,
        interval: timedelta | float,
        repeat: bool,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ):
        self.__interval = (
            interval.total_seconds() if isinstance(interval, timedelta) else interval
        )
        self.__repeat = repeat
        self.__func: partial[Any] = partial(func, *args, **kwargs)

    @property
    def interval(self):
        return self.__interval

    @property
    def repeat(self):
        return self.__repeat

    def __call__(self):
        return self.__func()

    def __repr__(self):
        func_name = (
            self.__func.func.__name__
            if hasattr(self.__func, "func")
            else str(self.__func)
        )
        return f"Task(timeout={self.__interval}, repeat={self.__repeat}, func='{func_name}')"
