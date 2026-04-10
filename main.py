import time
from scheduler import Scheduler, Task


# 1. Define your tasks
def greet(name: str):
    print(f"[{time.strftime('%X')}] Hello, {name}!")


def recurring_ping():
    print(f"[{time.strftime('%X')}] Ping...")


# 2. Initialize the Scheduler (automatically sizes the ThreadPool based on CPU cores)
scheduler = Scheduler(workers=4)
scheduler.start()

print(f"[{time.strftime('%X')}] Scheduler started.")

# 3. Schedule tasks
# Runs once, 2 seconds from now
task_one = Task(timeout=2, repeat=False, func=greet, name="Alice")
scheduler.schedule(task_one)

# Runs repeatedly, every 1.5 seconds
task_two = Task(timeout=1.5, repeat=True, func=recurring_ping)
scheduler.schedule(task_two)

# 4. Keep the main thread alive to watch the background threads work
try:
    time.sleep(6)
except KeyboardInterrupt:
    pass
finally:
    # 5. Cleanly shut down all background threads
    print("Shutting down gracefully...")
    scheduler.request_stop()
