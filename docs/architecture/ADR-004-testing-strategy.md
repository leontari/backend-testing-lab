# ADR-004

## Runtime responsibilities

### Responsibilities

`TraceManager`:

- install trace
- restore trace
- expose current trace

`TraceContextStore`:

- ContextVar access

`TraceContext`:

- immutable value object

`TracePropagator`:

- W3C serialization

`Adapters`:

- HTTP
- Kafka
- gRPC conversion
