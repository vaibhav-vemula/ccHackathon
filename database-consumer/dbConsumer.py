# To connect with the pymongo library:
import pymongo
import json
import pika
import time

sleepTime = 20
time.sleep(sleepTime)

#channel for database
channel = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
queueRideSharing = channel.queue_declare('rideSharingQueue')
nameRideSharingQueue = queueRideSharing.method.queue

channel.queue_bind(
    exchange='ride',
    queue=nameRideSharingQueue,
    routing_key='ride_database'
)

#mongoDB connection
mongoClient = pymongo.MongoClient('mongodb://mongo:27017/')
myDB = mongoClient["rideSharingDB"]
myCollection = myDB["consumer"]
cursor = myCollection.find()


print ("[*] Waiting for payload. To exit press CTRL+C")

def dbCallback(ch, method, properties, body):
    payload = json.loads(body)
    print("[x] Processign Request")
    # time.sleep(payload.get('time'))
    myCollection.insert_one(payload)
    #print name of the consumer from the database
    for document in cursor:
        print(document)
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_message_callback=dbCallback, queue='rideSharingQueue')
channel.start_consuming()