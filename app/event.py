from kafka import KafkaProducer
import json

def publish_message(producer_instance, topic_name, value=None):
    try:
        value_bytes = json.dumps(value).encode('utf-8')
        producer_instance.send(topic=topic_name, value=value_bytes)
        producer_instance.flush()
    except Exception as ex:
        print('Error publishing message.')
        print(str(ex))

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
    except Exception as ex:
        print('Error while connecting Kafka producer.')
        print(str(ex))
    return _producer
        
