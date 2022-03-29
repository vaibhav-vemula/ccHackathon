#This file consumes the data from the producer.py file
import pika
import time
import json
import uuid
import sys
import requests

# initial environment values
IP_PROD = sys.argv[1]
PORT_PROD = sys.argv[2]
IP_CONSUMER = sys.argv[3]
NAME_CONSUMER = sys.argv[4]
CONSUMER_ID = str(uuid.uuid4())

sleepTime = 20
time.sleep(sleepTime)


channel = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
queueRideSharing = channel.queue_declare('rideSharingQueue')
nameRideSharingQueue = queueRideSharing.method.queue

channel.queue_bind(
    exchange='ride',
    queue=nameRideSharingQueue,
    routing_key='ride_queue'
)

print ("[*] Waiting for messages. To exit press CTRL+C")

def callback(ch, method, properties, body):
    payload = json.loads(body)
    # print(payload)
    print("[x] Processing Request")
    time.sleep(payload.get('time'))
    print(f'[*] TaskID: {payload.get("taskId")}')
    ch.basic_ack(delivery_tag = method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
data_new_user = {
    "data": {
        "consumerId": CONSUMER_ID,
        "serverIp": IP_PROD,
        "consumerIp": IP_CONSUMER,
        "name": NAME_CONSUMER
    }
}

data_new_ride = {
    "data": {
        "consumerId": CONSUMER_ID,
        "pickup": "PES Univeristy",
        "destination": "NYC",
        "time": 5,
        "cost": 100,
        "seats": 4,
        "consumerId": 1
    }
}

API_URL = f'http://{IP_PROD}:{PORT_PROD}/new_ride_matching_consumer'
# print("API_URL:", API_URL)
response = requests.post(API_URL, json=data_new_user)
print("FIRST response:", response.text)
API_URL = f'http://{IP_PROD}:{PORT_PROD}/new_ride'
response = requests.post(API_URL, json=data_new_ride)
print("SECOND response:", response.text)
# print(response)
channel.basic_consume(on_message_callback=callback, queue='rideSharingQueue')
channel.start_consuming()