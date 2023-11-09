import threading
import time
import random
import pandas as pd

def generate_random_df(username):
    headers = ['A', 'B', 'C', 'D']
    data = {'A': random.randint(1, 10),
            'B': random.randint(1, 10),
            'C': random.randint(1, 10),
            'D': random.randint(1, 10)}

    df = pd.DataFrame([data], columns=headers)
    print("{} generated DataFrame:\n{}".format(username, df))
    return df

# Create a list to store thread instances
threads = []

# Create and start 5 threads, passing a unique username to each thread
dfs = []
for i in range(5):
    username = "User{}".format(i + 1)
    thread = threading.Thread(target=lambda: dfs.append(generate_random_df(username)))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Combine all DataFrames into one
result_df = pd.concat(dfs, ignore_index=True)
print("\nCombined DataFrame:\n", result_df)
