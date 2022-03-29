#This file consumes the data from the producer.py file

import pika
import time
import json

sleepTime = 1
time.sleep(sleepTime)


channel = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')).channel()
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
    print("[x] Processign Request")
    time.sleep(payload.get('time'))
    print(f'[*] destination: {payload.get("destination")} {payload.get("taskId")}')
    ch.basic_ack(delivery_tag = method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=callback, queue='rideSharingQueue')
channel.start_consuming()