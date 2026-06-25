from dataclasses import dataclass


@dataclass
class PaymentCompletedEvent:
    payment_id: str
    order_id: str
    trace_id: str
