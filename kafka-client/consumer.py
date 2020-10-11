# Import Statements
from kafka import KafkaConsumer

# Creates a consumer
def create_consumer(consumer_topic):
    consumer = KafkaConsumer(consumer_topic, bootstrap_servers = ['localhost:9092'], 
                                api_version = (0, 10))
    return consumer

