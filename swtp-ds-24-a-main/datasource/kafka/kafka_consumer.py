from kafka import KafkaConsumer
import json
decode = lambda x: json.loads(x.decode('utf-8'))
consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092",group_id= 'groupe_A', auto_offset_reset = "latest") #value_deserializer=decode)
consumer.subscribe(topics = ["quicktest"])

def read_message(consumer):
    for message in consumer:
        print('hallotesettese', message.value)

read_message(consumer)
for message in consumer.poll(max_records=3):
    print('HI', message.value)
