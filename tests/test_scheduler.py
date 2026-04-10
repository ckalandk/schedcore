import time
import threading
import pytest
from scheduler import Scheduler, Task


@pytest.fixture
def scheduler():
    """
    This fixture creates a fresh scheduler for every test, starts it,
    and most importantly, guarantees request_stop() is called after the test
    finishes (even if an assertion fails) so we don't leak threads.
    """
    s = Scheduler(workers=2)
    s.start()
    yield s
    s.request_stop()


def test_single_delayed_task(scheduler):
    """
    Test 1: Basic Delay.
    Ensures a task executes after the correct delay without blocking the main thread.
    """
    event = threading.Event()

    # Schedule a task for 50 milliseconds from now
    scheduler.schedule(Task(timeout=0.05, repeat=False, func=event.set))

    # wait() blocks the test until the worker thread calls event.set().
    # The 1.0s timeout ensures the test fails instantly instead of hanging forever if broken.
    success = event.wait(timeout=1.0)

    assert success is True, "The scheduled task never fired."


def test_task_priority_and_ordering(scheduler):
    """
    Test 2: Ordering.
    Ensures that a task with a shorter timeout fires FIRST, even if scheduled LAST.
    """
    results = []
    event = threading.Event()

    def append_and_check(name):
        results.append(name)
        if len(results) == 2:
            event.set()

    # Task A is scheduled first, but is due in 200ms
    scheduler.schedule(Task(timeout=0.2, repeat=False, func=append_and_check, name="A"))

    # Task B is scheduled second, but is due in 50ms
    scheduler.schedule(
        Task(timeout=0.05, repeat=False, func=append_and_check, name="B")
    )

    event.wait(timeout=1.0)

    # B should absolutely finish before A
    assert results == ["B", "A"]


def test_repeating_task(scheduler):
    """
    Test 3: Repetition.
    Ensures that a repeating task successfully reschedules itself.
    """
    results = []

    def counter_func():
        results.append(time.monotonic())

    # Schedule a task to repeat every 50ms
    scheduler.schedule(Task(timeout=0.05, repeat=True, func=counter_func))

    start_time = time.monotonic()
    while len(results) < 3 and time.monotonic() - start_time < 1.0:
        time.sleep(0.01)

    assert len(results) >= 3, "The task did not repeat the expected number of times."


def test_graceful_shutdown():
    """
    Test 4: The Teardown.
    Ensures that calling request_stop() instantly wakes up the dispatcher
    and kills the OS threads, even if tasks are waiting in the queue.
    """
    s = Scheduler(workers=2)
    s.start()

    # Schedule a task 10 minutes in the future.
    # If our stop logic is broken, the dispatcher thread will sleep for 10 minutes.
    s.schedule(Task(timeout=600, repeat=False, func=lambda: None))

    # Request stop immediately
    s.request_stop()

    # Assert that the dispatcher thread successfully woke up and exited
    assert s.__getattribute__("_Scheduler__thread").is_alive() is False, (
        "Dispatcher thread failed to terminate."
    )
