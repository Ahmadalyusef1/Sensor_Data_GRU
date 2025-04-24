import datetime, time, json
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic, KafkaAdminClient
import time
# dict to json
encode = lambda x: json.dumps(x).encode("utf-8")
#decode = lambda x: json.loads(x.decode('utf-8'))
# connect to Kafka

conf = {#'bootstrap.servers': 'localhost:9092',
             #'queue.buffering.max.messages': 1000000,
             'queue.buffering.max.ms' : 500
        }
producer = KafkaProducer(bootstrap_servers="slo.swe.th-luebeck.de:9092", value_serializer=encode, acks=0, retries=3, linger_ms = 2, batch_size = 0)


data = {
    "n": 92830,
    "accelerometer": {"x": -0.015625, "y": -0.169678, "z": 1.044434},
    "gyroscope": {"x": -2.251908, "y": -0.916031, "z": -0.389313},
    "timestamp": 111
   
}
#  # Zeitstempel hinzufügen
producer.send('quicktest', data)

#producer.send('quicktest', {"P":"test"})


