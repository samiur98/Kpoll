# Import Statements
from kafka import KafkaProducer

# Creates a Producer
def create_producer():
    producer = KafkaProducer(bootstrap_servers = ['localhost:9092'], 
                                api_version = (0, 10, 1))
    return producer

