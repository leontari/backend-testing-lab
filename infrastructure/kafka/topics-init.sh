#!/bin/bash

kafka-topics --create \
  --if-not-exists \
  --topic payment.created \
  --bootstrap-server kafka:9092

kafka-topics --create \
  --if-not-exists \
  --topic payment.completed \
  --bootstrap-server kafka:9092

kafka-topics --list \
  --bootstrap-server kafka:9092
