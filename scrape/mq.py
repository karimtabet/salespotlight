import threading, time
import yaml
import json

from kafka import KafkaProducer


class Producer(threading.Thread):
    '''
    Threaded Kafka Producer with additional parameter 
    for message to produce
    '''
    def __init__(self, message, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.message = message

    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.send('products', self.message)

def produce(message):
    '''
    Creates a producer object initiated with a message
    '''
    producer = Producer(str.encode(str(message)))
    producer.start()
    time.sleep(1)
