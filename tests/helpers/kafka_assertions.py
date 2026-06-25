def assert_event_exists(events, key, value):
    for e in events:
        if e.get(key) == value:
            return True

    raise AssertionError(f"Event not found: {key}={value}")


def assert_event_chain(order_event, payment_event):
    assert order_event["order_id"] == payment_event["order_id"]
