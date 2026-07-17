# Shared Logger

Production-grade structured logging layer.

The logger provides a unified application logging interface
for all runtime components.

The module is designed for:

- Kubernetes environments;
- distributed systems;
- async applications;
- microservices;
- tracing correlation;
- structured log aggregation.

---

# Design Goals

The logger layer provides:

- single logging API;
- structured JSON output;
- async-safe runtime context;
- trace correlation;
- service metadata;
- exception serialization;
- DI integration.

Application code must not use:

```python
import logging
```
directly.

Instead:
```python
from shared.logger import Logger
```

## Architecture

```
Application
     |
     v
  Logger
     |
     +----------------+
     |                |
 LogContext       Formatter
     |
     v
 ContextVar
     |
     v
 stdout
     |
     +----------------+
                      |
              Loki / ELK / OpenSearch
```

## Package Structure

```
shared/logger/

├── __init__.py
├── config.py
├── context.py
├── formatter.py
├── logger.py
└── protocols.py
```

## Components

### LoggerConfig

Runtime configuration.

Example:
```
from shared.logger import LoggerConfig


config = LoggerConfig(
    service="order-service",
    environment="production",
    version="1.4.0",
)
```

Fields:

| Field       | 	Description         |
|-------------|----------------------|
| service     | 	service name        |
| environment | 	runtime environment |
| version     | 	application version |
| level       | 	logging level       |
| json        | 	enable JSON output  |

## Logger

Main application facade.

The object should be registered as a singleton
in the dependency container.

Example:

```
logger.info(
    "order.created",
    order_id=100,
)
```

Output:

```
{
    "timestamp":"2026-07-16T10:20:00Z",
    "level":"INFO",
    "service":"order-service",
    "environment":"production",
    "version":"1.4.0",
    "message":"order.created",
    "order_id":100
}
```

## Dependency Injection

Logger is a runtime singleton.

Example:

```
container.register(
    contract=Logger,
    provider=logger,
    scope=DependencyScope.SINGLETON,
)
```

Application services receive:

```
class OrderService:

    def __init__(
        self,
        logger: Logger,
    ):
        self.logger = logger
```

## Logging API

### info

```
logger.info(
    "order.created",
    order_id=123,
)
```

### error

```
logger.error(
    "payment.failed",
    payment_id=10,
)
```

### exception

Automatically serializes exception metadata.

Example:

```
try:
    process_payment()
except Exception:
    logger.exception("payment.error")
```

Output:

```
{
    "level":"ERROR",
    "message":"payment.error",
    "error.type":"ValueError",
    "error.message":"invalid payment"
}
```

## Runtime Context

The logger supports async-safe contextual metadata.

Implementation:
 - `ContextVar` is used internally.

Example:

```
set_context(
    LogContext(
        {
            "request_id":"abc",
            "trace_id":"123"
        }
    )
)
```

All following logs automatically contain:

```
{
    "request_id":"abc",
    "trace_id":"123"
}
```

## Tracing Integration

Logger does not depend on tracing implementation.

Dependency direction:

```
Tracing
    |
    v
LogContext
    |
    v
Logger
```

The logger only consumes context.

Example:

Incoming request:

```
trace_id=abc
span_id=123
```

Application log:

```
logger.info("request.completed")
```

Output:

```
{
    "message":"request.completed",
    "trace_id":"abc",
    "span_id":"123"
}
```

## Kubernetes Usage

The logger writes JSON to stdout.

Example:

```
{
    "service":"payment-service",
    "level":"INFO",
    "message":"payment.completed",
    "payment_id":100
}
```

Kubernetes logging pipeline:

```
Application
     |
     v
stdout
     |
     v
Fluent Bit / Vector
     |
     v
Loki / Elasticsearch
     |
     v
Grafana
```

## Log Search Examples

Find all logs for request:
```
trace_id="abc123"
```

Find all errors:
```
level="ERROR"
```

Find service:
```
service="payment-service"
```

## Async Safety

The logger uses `ContextVar`.

Each async task receives its own context.

Example:

```
async def handler():
    set_context(
        LogContext(
            {
                "request_id":"123"
            }
        )
    )

    logger.info("request.started")
```

Concurrent requests do not share metadata.

## Logging Rules

### Correct

```
logger.info(
    "order.created",
    order_id=100,
)
```

### Incorrect

```
print("order created")
```

Incorrect

```
import logging

logging.info("message")
```

## Production Recommendations

Recommended:

- JSON output enabled;
- stdout logging;
- log aggregation outside application;
- trace correlation enabled;
- INFO level in production;
- DEBUG only temporarily.

## Responsibilities

Logger owns:

- formatting;
- structured fields;
- context propagation;
- exception serialization.

Logger does not own:

- log storage;
- log rotation;
- file management;
- monitoring;
- alerting.

These responsibilities belong to infrastructure.

## Integration With Shared Modules

Current dependency graph:

```
              Application

                  |
                  |

        +---------+---------+
        |         |         |

     Logger   Metrics   Tracing


                  |

             Infrastructure
```

Logger is a foundational runtime component.

## Testing

Tests:

```
tests/logger/

├── test_config.py
├── test_context.py
├── test_formatter.py
└── test_logger.py
```

Run:

```
pytest shared/tests/logger -v
```
