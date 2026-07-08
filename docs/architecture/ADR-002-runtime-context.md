# ADR-002

## Runtime Context

### Context

- Every asynchronous request must have its own `TraceContext`.
- Python threads are not suitable for `asyncio`, `FastAPI`, `aiokafka` shared threads.

### Decision

- Store `TraceContext` inside `ContextVar`.
- Encapsulate `TraceContext` by `TraceContextStore`.
- Only `TraceContextStore` may directly access `ContextVar`.

### Consequences

Advantages

- async safe
- request isolation
- task isolation
- no global state
