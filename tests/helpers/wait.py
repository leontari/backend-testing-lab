import time


# retry logic
def wait_until(fn, timeout=30):
    start = time.time()

    while time.time() - start < timeout:
        try:
            if fn():
                return True
        except Exception:
            pass
        time.sleep(1)

    raise TimeoutError("Condition not met")
