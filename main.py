import time
from schedcore import Scheduler, Task


# 1. Define your tasks
def greet(name: str):
    print(f"[{time.strftime('%X')}] Hello, {name}!")


def recurring_ping():
    print(f"[{time.strftime('%X')}] Ping...")


def raise_error():
    raise ValueError("Task raised and exception")


def error_handler(exception, task):
    print(f"Task: {task} didn't execute du to an exception: {exception}")


# 2. Initialize the Scheduler (automatically sizes the ThreadPool based on CPU cores)
scheduler = Scheduler(workers=4)
scheduler.set_error_handler(error_handler)

scheduler.start()

print(f"[{time.strftime('%X')}] Scheduler started.")

# 3. Schedule tasks
# Runs once, 2 seconds from now
task_one = Task(timeout=2, repeat=False, func=greet, name="Alice")
scheduler.schedule(task_one)

# Runs repeatedly, every 1.5 seconds
task_two = Task(timeout=1.5, repeat=True, func=recurring_ping)
scheduler.schedule(task_two)
scheduler.schedule(Task(timeout=3, repeat=False, func=raise_error))

# 4. Keep the main thread alive to watch the background threads work
try:
    time.sleep(6)
except KeyboardInterrupt:
    pass
finally:
    # 5. Cleanly shut down all background threads
    print("Shutting down gracefully...")
    scheduler.request_stop()
