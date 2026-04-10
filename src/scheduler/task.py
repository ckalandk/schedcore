from collections.abc import Callable
from functools import partial
from typing import Any


class Task:
    """
    Represents a task to be executed by the Scheduler.

    The Task class encapsulates a callable and its arguments, along with
    timeout and repeat.

    Attributes:
        timeout (float): The delay in seconds before the task should execute.
        repeat (bool): If True, the task will be rescheduled after execution
            using the same timeout interval.
        func (Callable): The function or executable to be run.
        args (tuple): Positional arguments to pass to the function.
        kwargs (dict): Keyword arguments to pass to the function.
    """

    def __init__(
        self,
        timeout: float,
        repeat: bool,
        func: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ):
        self.__timeout = timeout
        self.__repeat = repeat
        self.__func: partial[Any] = partial(func, *args, **kwargs)

    @property
    def timeout(self):
        return self.__timeout

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
        return f"Task(timeout={self.__timeout}, repeat={self.__repeat}, func='{func_name}')"
