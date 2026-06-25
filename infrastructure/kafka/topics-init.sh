#!/bin/bash

kafka-topics --create \
  --topic order.created \
  --bootstrap-server kafka:9092

kafka-topics --create \
  --topic payment.completed \
  --bootstrap-server kafka:9092
