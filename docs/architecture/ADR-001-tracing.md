# ADR-001

## Use W3C Trace Context instead of custom trace headers

### Context

- Microservices communicate through `HTTP`, `gRPC`, `Kafka`.
- The tracing solution must support all transports without transport-specific logic.

### Decision

- Use `traceparent` and `tracestate` defined by W3C Trace Context.
- Internal runtime model may contain additional metadata (`created_at`, `parent_span_id`) 
which is not transmitted across the network.

### Consequences

Advantages

- OpenTelemetry compatible
- Jaeger compatible
- Tempo compatible
- Zipkin compatible
- vendor neutral

Disadvantages

- Slightly more complicated implementation than proprietary headers.
