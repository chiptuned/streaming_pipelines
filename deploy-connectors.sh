#!/bin/bash

# Debezium Connect API URL
connect_url="http://localhost:8083/connectors/"

# Path to the connector configuration file
config_file="./debezium-connector.json"

# Wait for Debezium Connect to be ready
echo "Waiting for Debezium Connect to start..."
while ! curl -s "${connect_url}" > /dev/null; do
    sleep 5
done
echo "Debezium Connect is up and running."

# Function to check if Kafka is ready
kafka_ready() {
    kafka-topics.sh --list --bootstrap-server kafka:9092 > /dev/null 2>&1
}

# Wait for Kafka to be ready
until kafka_ready; do
    echo "Waiting for Kafka to be ready..."
    sleep 5
done

# Create Kafka topic (if not already exists)
kafka-topics.sh --create --if-not-exists --bootstrap-server kafka:9092 \
                --replication-factor 1 \
                --partitions 3 \
                --topic your_topic

# Deploy Debezium connector
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
    "${connect_url}" -d @"${config_file}"

echo "Connector deployed"