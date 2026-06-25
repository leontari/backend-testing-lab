import time


def wait_for_event(consumer, condition_fn, timeout=30):

    start = time.time()

    while time.time() - start < timeout:

        for msg in consumer.messages:
            if condition_fn(msg):
                return msg

        time.sleep(1)

    raise TimeoutError("Event not found")
