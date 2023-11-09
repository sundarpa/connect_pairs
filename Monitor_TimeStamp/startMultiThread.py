import threading
import time
import random

def random_hello(username):
    wait_time = random.uniform(1, 5)
    print("Waiting for {} seconds before saying hello to {}...".format(wait_time, username))
    time.sleep(wait_time)
    print("Hello, {}!".format(username))

# Create a list to store thread instances
threads = []

# Create and start 5 threads, passing a unique username to each thread
for i in range(5):
    username = "User{}".format(i + 1)
    thread = threading.Thread(target=random_hello, args=(username,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("All threads have finished.")
