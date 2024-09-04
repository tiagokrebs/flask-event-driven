from kafka import KafkaProducer

def publish_message(producer_instance, topic_name, key, value):
    try:
        producer_instance.send(topic_name, key=key, value=value)
        producer_instance.flush()
        print('Message published successfully.')
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
        
