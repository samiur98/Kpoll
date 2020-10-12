# Import Statements
from kafka import KafkaConsumer

# Creates a consumer
def create_consumer(consumer_topic, time = 300000):
    consumer = KafkaConsumer(consumer_topic, bootstrap_servers = ['localhost:9092'], 
                                api_version = (0, 10), consumer_timeout_ms = time)
    return consumer

