from pydantic import BaseModel


class OrderDTO(BaseModel):
    order_id: str
    payload: dict
    trace_id: str
