# Distributed Tracing Module

Lightweight async-friendly distributed tracing subsystem.

The module provides:

* W3C Trace Context propagation;
* async-safe trace context storage using `ContextVar`;
* universal transport extraction/injection;
* FastAPI/gRPC/Kafka integration;
* DI-friendly runtime API;
* single public facade object.

The application works only with the `Tracing` object. Internal components (`Manager`, `Factory`, `Store`, `Propagator`) are hidden behind the public API.

---

# Architecture

```
Tracing
 |
 +-- TraceManager
 |      |
 |      +-- TraceFactory
 |      |
 |      +-- TraceContextStore
 |
 +-- TracePropagator
 |
 +-- TransportRegistry
```

Responsibilities:

| Component           | Responsibility                       |
| ------------------- | ------------------------------------ |
| `Tracing`           | Public application API               |
| `TraceManager`      | Runtime lifecycle management         |
| `TraceFactory`      | Creating root and child spans        |
| `TraceContextStore` | Async execution context storage      |
| `TracePropagator`   | W3C traceparent/tracestate parsing   |
| `TransportRegistry` | Transport-specific header conversion |

---

# Basic Usage

Create tracing subsystem:

```python
from tracing import Tracing


tracing = Tracing()
```

The object is fully initialized and ready to use.

---

# Current Trace

Get active trace context:

```python
context = tracing.current()

if context:
    print(context.trace_id)
    print(context.span_id)
```

If no trace exists:

```python
None
```

is returned.

---

# Creating Spans

Use `span()` as an async context manager:

```python
async with tracing.span() as context:
    await process_payment()
```

The context lifecycle is handled automatically:

```
enter

create span
activate ContextVar

execute code

exit

restore previous context
```

The application does not need to manually manage tokens or reset context.

---

# Nested Spans

Example:

```python
async with tracing.span() as request_span:

    async with tracing.span() as database_span:

        await query_database()
```

Result:

```
Trace ID: A


request_span
    span_id: 1


        |
        |
        v


database_span
    span_id: 2
    parent_span_id: 1
```

---

# HTTP Integration

## Incoming Request

Extract trace context:

```python
source = tracing.extract(
    request.headers
)
```

Create request span:

```python
async with tracing.span(source):

    response = await handler()
```

---

## Outgoing Request

Inject current trace:

```python
headers = {}

tracing.inject(
    tracing.current(),
    headers,
)
```

Result:

```http
traceparent: 00-<trace_id>-<span_id>-01
tracestate: ...
```

---

# FastAPI Middleware

Example:

```python
from tracing.fastapi import TraceMiddleware


tracing = Tracing()


app.add_middleware(
    TraceMiddleware,
    tracing=tracing,
)
```

Middleware automatically:

1. extracts incoming trace;
2. creates request span;
3. binds context to current async task;
4. restores previous context;
5. injects response headers.

---

# Kafka Usage

Incoming message:

```python
context = tracing.extract(
    message.headers
)


async with tracing.span(context):

    await process_message()
```

Outgoing message:

```python
tracing.inject(
    tracing.current(),
    message.headers,
)
```

---

# gRPC Usage

Incoming metadata:

```python
context = tracing.extract(
    metadata
)


async with tracing.span(context):

    await grpc_handler()
```

Outgoing metadata:

```python
tracing.inject(
    tracing.current(),
    metadata,
)
```

---

# Custom Transport

The module does not depend on HTTP, Kafka or gRPC.

New transports can be registered:

```python
tracing.register_transport(
    RabbitHeaders,

    extract=lambda carrier: {
        "traceparent": carrier.traceparent
    },

    inject=lambda carrier, headers:
        carrier.update(headers),
)
```

After registration:

```python
context = tracing.extract(
    rabbit_headers
)
```

works automatically.

---

# Dependency Injection

Register tracing as application singleton:

```python
container.register_singleton(
    Tracing,
    Tracing(),
)
```

Services depend only on the public API:

```python
class PaymentService:

    def __init__(
        self,
        tracing: Tracing,
    ):
        self.tracing = tracing
```

---

# Design Principles

## Single Public API

Application imports only:

```python
from tracing import Tracing
```

No direct usage of:

* `TraceManager`
* `TraceFactory`
* `ContextVar`
* transport adapters

---

## Transport Independence

Tracing works with any carrier:

```
HTTP headers
      |
gRPC metadata
      |
Kafka headers
      |
RabbitMQ properties
      |
custom transport
```

All are converted into a common internal representation.

---

## Async Safe

The module uses Python `ContextVar`.

Each async task receives its own trace context:

```
Request A

ContextVar
   |
 Trace A


Request B

ContextVar
   |
 Trace B
```

No global state is shared.

---

# Testing

Tracing components can be replaced:

```python
tracing = Tracing(
    manager=fake_manager,
    propagator=fake_propagator,
    transport=fake_transport,
)
```

This allows isolated unit testing without real transports.

---

# Future Extensions

Possible integrations:

* Prometheus metrics;
* Grafana dashboards;
* OpenTelemetry exporter;
* span processors;
* structured logging correlation;
* distributed workflow tracing.

The public API remains unchanged:

```python
tracing.current()

async with tracing.span()

tracing.extract()

tracing.inject()
```
