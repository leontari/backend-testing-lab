from dataclasses import dataclass


@dataclass
class OrderCreatedEvent:
    order_id: str
    trace_id: str
