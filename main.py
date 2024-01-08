import logging
from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Configure
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

# Kafka Consumer Setup
logging.info("Setting up Kafka Consumer")
consumer = KafkaConsumer(
    'my_topic', 
    bootstrap_servers=['localhost:29092'],
    value_deserializer=lambda m: json.loads(m.decode('ascii'))
)

# MongoDB Setup
logging.info("Setting up MongoDB client")
client = MongoClient(f'mongodb://root:{MONGO_INITDB_ROOT_PASSWORD}@mongo:27017/') 
db = client.your_database
collection = db.your_collection

# Aggregation Logic
def aggregate_data():
    logging.info("Starting data aggregation")
    start_time = time.time()
    count = 0
    while time.time() - start_time < 10:  # 10-second window
        for message in consumer:
            data = message.value
            if data['operation'] == 'create':  # Replace with actual logic to identify new insertions
                count += 1
                logging.info(f"Aggregating new data: {data}")
            if time.time() - start_time >= 10:
                break

    logging.info(f"Aggregated data count: {count}")
    collection.insert_one({'date': datetime.now(), 'count': count})
    logging.info("Data aggregation completed and stored in MongoDB")

# Main loop
while True:
    aggregate_data()
    logging.info("Completed a round of data aggregation")
