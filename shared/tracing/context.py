import contextvars
import uuid

trace_id_var = contextvars.ContextVar("trace_id", default=None)


def get_trace_id():
    trace_id = trace_id_var.get()

    if trace_id is None:
        trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)

    return trace_id


def set_trace_id(trace_id: str):
    trace_id_var.set(trace_id)
