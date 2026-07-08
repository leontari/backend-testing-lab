# ADR-003

## Why adapters do not know TraceManager

### Context

- HTTP, Kafka, gRPC should remain transport layers.
- Business logic should not leak into transport adapters.

### Decision

- Transport adapters only convert

```
Headers
↓
RawTraceCarrier
```

- TraceManager decides

```
Root
or
Child

trace
```

### Consequences

- Transport layer remains reusable.
- Testing becomes easier.
