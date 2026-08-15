# Messaging

Universal message abstraction for Runtime Kernel.

The messaging package provides a common communication model used by:

- HTTP services
- Kafka messaging
- gRPC communication
- CommandBus
- EventBus
- Workflow Engine
- Saga Engine

The goal is to have a single message representation that can be transported
between application components and distributed services.

---

# Design principles

## One message model

The system does not have separate transport-specific messages.

The same `Message` object is used for:

- commands;
- events;
- requests;
- responses;
- notifications.

Example:

```
HTTP Request
|
v
Message
|
+--> CommandBus
|
+--> Workflow
|
+--> Kafka
|
+--> gRPC
```

---

# Message structure

The central object is:

```
Message

|
+-- Identity
|
+-- Headers
|
+-- Metadata
|
+-- Payload
```


---

# Message

File:

```
message.py
```

Contains:

- message semantic kind;
- payload;
- identity;
- distributed headers;
- runtime metadata.

Example:

```
message = Message(
    kind=MessageKind.COMMAND,
    payload=payload,
)
```

---

# MessageKind

Message kind describes message intention.

Available kinds:

```
COMMAND
EVENT
REQUEST
RESPONSE
NOTIFICATION
```

Important:
- Kind is semantic.
- It does not describe transport.

Bad:

```
KafkaMessage
HttpMessage
GrpcMessage
```

Good:

```
PaymentRequested
OrderCreated
UserNotification
```

---

# Identity

File:

```
identity.py
```

Message identity describes:

- uniqueness;
- causality;
- operation correlation.

Structure:

```text
MessageIdentity

 |
 +-- message_id
 |
 +-- correlation_id
 |
 +-- causation_id
 |
 +-- created_at
```

## message_id

Unique identifier of a single message.

Example:
```text
PaymentRequested

message_id=A
```

## correlation_id

Identifies a logical operation.

Example:

```text
CreateOrder

      |
      + Payment
      |
      + Inventory
      |
      + Notification
```

All messages:

```text
correlation_id=ORDER-123
```

## causation_id

Identifies the parent message.

Example:

```text
OrderCreated
    message_id=A

PaymentRequested
    message_id=B
    causation_id=A
```

This allows building a message graph:

```text
OrderCreated
       |
       v
PaymentRequested
       |
       v
PaymentCompleted
```

---

# Headers

File:
```text
headers.py
```

Headers contain distributed context.

They are transferred between services.

Used by:
- tracing;
- logging;
- metrics;
- routing;
- protocol metadata.

---

# Standard headers

Runtime Kernel owns:

```text
traceparent
tracestate
baggage
tenant
locale
content-type
schema
reply-to
correlation-id
```

---

# Business headers

Business headers are allowed.

Example:

```text
headers.set(
    "customer-id",
    "123"
)
```

But they are not part of Kernel.

The Kernel must not know:
```text
customer-id
payment-id
warehouse-id
campaign-id
```

---

# Tracing headers

Tracing uses W3C Trace Context.

Supported:
```text
traceparent
tracestate
baggage
```

Example:

```text
traceparent:
00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

The messaging layer only transports these values.

Parsing and lifecycle management belong to:

```text
shared/tracing
```

---

# Metadata

File:

```text
metadata.py
```

Metadata is runtime state.

Unlike headers, metadata is not propagated between services.

Used for:
- processing state;
- retries;
- lifecycle management.

Example:

```text
MessageMetadata
 |
 +-- status
 |
 +-- retry_count
 |
 +-- received_at
 |
 +-- processed_at
```

---

# Metadata lifecycle

The state machine:

```text
RECEIVED
    |
    v
PROCESSING
    |
    +--------------+
    |              |
    v              v
COMPLETED       FAILED



PROCESSING
    |
    v
RETRYING
    |
    v
PROCESSING
```

Terminal states:

```text
COMPLETED
FAILED
CANCELLED
```

---

# Payload

File:

```text
payload.py
```

Payload contains business data.

Structure:

```text
Payload
 |
 +-- schema
 |
 +-- version
 |
 +-- data
```

Example:

```text
Payload(
    schema="payment.created",
    version=1,
    data={
        "payment_id": "123",
        "amount": 100,
    }
)
```

---

# Schema versioning

Schemas are versioned explicitly.

Example:

- Version 1

```text
{
 "schema": "payment.created",
 "version": 1,
 "data": {
    "amount":100
 }
}
```

- Version 2

```text
{
 "schema": "payment.created",
 "version": 2,
 "data": {
    "amount":100,
    "currency":"EUR"
 }
}
```

Both versions may exist simultaneously.

---

# Serializer

File:

```text
serializer.py
```

Serializer converts messages between:

```text
Message
    |
    v
dict
    |
    v
JSON
    |
    v
bytes
```

Used by:
- HTTP;
- Kafka;
- gRPC.

Example:

```text
serializer = MessageSerializer()
data = serializer.dumps(message)
```

Result:

```text
{
 "identity": {},
 "kind": "event",
 "headers": {},
 "payload": {}
}
```

---

# Serialization rules

Serialized:

```text
Identity
Headers
Payload
Kind
```

Not serialized:

```text
Metadata
```

Reason:
- Metadata belongs to local runtime.

Example:

Producer:

```text
status=COMPLETED
```

Consumer:

```
status=RECEIVED
```

---

# Integration with other Kernel modules

## Logger

Uses:

```text
headers.traceparent
identity.correlation_id
```

for log correlation.

## Metrics

Uses:

```text
headers.tenant
message.kind
payload.schema
```

for dimensions.

## Tracing

Uses:

```text
headers.traceparent
headers.tracestate
headers.baggage
```

## CommandBus

Consumes:

```text
MessageKind.COMMAND
```

Example:

```text
CreatePayment
```

## EventBus

Consumes:

```text
MessageKind.EVENT
```

Example:

```text
PaymentCompleted
```

## Saga / Workflow

Uses:

```text
identity.correlation_id
identity.causation_id
```

to build execution graphs.

---

# Transport independence

Messaging does not know:

```
HTTP
Kafka
gRPC
RabbitMQ
NATS
```

Transport adapters are responsible for mapping:

```
Transport message
        |
        v
Kernel Message
```

Example:

```
Kafka Headers
        |
        v
MessageHeaders
```

---

# Package responsibility

```text
messaging
    Message: communication envelope
    Identity: message relations
    Headers: distributed context
    Metadata: runtime state
    Payload: business data
    Serializer: representation conversion
```

---

# Non-goals

Messaging does NOT provide:
- business rules;
- validation of DTO fields;
- workflow execution;
- retries;
- tracing implementation;
- transport clients.

Those belong to:

```text
dto
workflow
tracing
transport
```

---

# Final model

The complete message flow:

```text
              Application
                  |
                  v
              DTO
                  |
                  v
              Payload
                  |
                  v
              Message
        +---------+---------+
        |         |         |
     Headers   Identity  Metadata
                  |
                  v
          Transport Adapter
                  |
        +---------+---------+
       HTTP     Kafka     gRPC
```

Messaging is the stable communication contract of Runtime Kernel.
