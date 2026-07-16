# Metrics subsystem

## Overview

The metrics subsystem provides application-level metrics collection
through a unified runtime API.

The module is designed as part of the Runtime Kernel infrastructure
and provides:

- counters;
- gauges;
- histograms;
- execution timers;
- Prometheus integration.

The application does not depend directly on `prometheus_client`.

All metrics operations go through the single public facade:

```python
from metrics import Metrics
```

---

# Architecture

The internal structure:

```
Application
     |
     v
 Metrics
     |
     v
 MetricManager
     |
     v
 PrometheusBackend
     |
     v
 prometheus_client
```

Responsibilities:

## Metrics

Public application API.

Responsible for:

- incrementing counters;
- updating gauges;
- observing values;
- measuring execution time.

Does not know about:

- Prometheus;
- exporters;
- storage.

---

## MetricManager

Runtime lifecycle manager.

Responsible for:

- lazy metric creation;
- caching metric instances;
- preventing duplicate registration;
- maintaining metric type consistency.

---

## PrometheusBackend

Backend adapter.

Responsible for:

- creating Prometheus metric objects.

The rest of the application never imports this layer directly.

---

# Installation

The module requires:

```
prometheus_client
```

Install:

```bash
pip install prometheus-client
```

---

# Dependency Injection

Metrics is designed to be used as a singleton runtime service.

Example:

```python
metrics = Metrics()

container.register(
    contract=Metrics,
    instance=metrics,
)
```

Services receive it through constructor injection:

```python
class OrderService:

    def __init__(
        self,
        metrics: Metrics,
    ):
        self._metrics = metrics
```

---

# Public API

## Counter

Counters represent values that only increase.

Examples:

- created objects;
- processed messages;
- failed operations.

Usage:

```python
metrics.increment(
    "orders.created.total"
)
```

Increment by custom value:

```python
metrics.increment(
    "messages.processed.total",
    value=10,
)
```

With labels:

```python
metrics.increment(
    "requests.total",
    labels={
        "status": "success",
    },
)
```

Prometheus result:

```
requests_total{status="success"} 1
```

---

# Gauge

Gauges represent current values.

Examples:

- active connections;
- queue size;
- memory usage.

Usage:

```python
metrics.gauge(
    "connections.active",
    25,
)
```

With labels:

```python
metrics.gauge(
    "workers.active",
    4,
    labels={
        "service": "payment",
    },
)
```

---

# Histogram

Histograms measure distributions.

Typical use cases:

- latency;
- request duration;
- database execution time.

Usage:

```python
metrics.observe(
    "request.duration.seconds",
    0.145,
)
```

---

# Timer

Timer is a helper for measuring execution duration.

## Synchronous code

```python
with metrics.timer(
    "database.query.seconds"
):

    repository.find()
```

## Asynchronous code

```python
async with metrics.timer(
    "grpc.request.seconds"
):

    await client.call()
```

The timer automatically records elapsed time into a histogram.

---

# FastAPI integration

The metrics subsystem does not expose HTTP endpoints.

The application decides how metrics are published.

Example:

```python
from prometheus_client import make_asgi_app


app.mount(
    "/metrics",
    make_asgi_app(),
)
```

Prometheus can then scrape:

```
GET /metrics
```

---

# Naming conventions

Metric names should describe:

- what is measured;
- the unit;
- the aggregation type.

Recommended format:

```
<object>_<action>_<unit>
```

Examples:

Good:

```
orders_created_total

http_request_duration_seconds

database_query_duration_seconds

active_connections
```

Bad:

```
orders

time

counter1
```

---

# Units

Durations:

Use seconds:

```
_seconds
```

Example:

```
http_request_duration_seconds
```

Sizes:

Use bytes:

```
_bytes
```

Example:

```
cache_size_bytes
```

Totals:

Use:

```
_total
```

Example:

```
messages_processed_total
```

---

# Labels

Labels should represent dimensions.

Good:

```python
metrics.increment(
    "requests.total",
    labels={
        "method": "GET",
        "status": "200",
    },
)
```

Bad:

```python
metrics.increment(
    "requests.total",
    labels={
        "user_id": "123456",
    },
)
```

Do not use high-cardinality values:

- user IDs;
- request IDs;
- trace IDs;
- timestamps.

---

# Relationship with tracing

Metrics and tracing solve different problems.

Tracing answers:

```
Why was this request slow?
```

Metrics answer:

```
How often does this happen?
```

They work together:

```
              Request

                 |
        +--------+--------+
        |                 |
     Tracing           Metrics

     trace_id          counters
     span_id           latency
     workflow          errors
```

Example:

```python
trace = tracing.current()

metrics.increment(
    "payment.failed.total"
)
```

The trace context should not be stored inside metrics.

---

# Thread safety

Metrics is safe to use from:

- asyncio applications;
- background workers;
- multiple threads.

The underlying synchronization is handled by
`prometheus_client`.

---

# Production recommendations

## Do

- keep metric names stable;
- avoid high-cardinality labels;
- measure business-critical operations;
- prefer histograms for latency.

## Do not

- create metrics dynamically from user input;
- include IDs in labels;
- create thousands of unique metric names.

---

# Testing

The module should be tested at three levels:

## Unit tests

Test:

- MetricManager;
- Metrics facade;
- timer behaviour.

## Integration tests

Test:

- FastAPI `/metrics`;
- Prometheus exposition format.

## Runtime tests

Test:

- metrics availability during service lifecycle.

---

# Future extensions

Possible future additions:

- OpenTelemetry metrics exporter;
- custom exporters;
- runtime metric namespaces;
- automatic HTTP/gRPC instrumentation.

These extensions should not change the public API.
