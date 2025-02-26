import time

print("Controller script is running...", flush=True)
print("Performing initialization...", flush=True)
print("Controller operations have completed.", flush=True)
i = 0
while True:
    print(str(i) + " iteration", flush=True)
    i += 1
    time.sleep(1)