# imports
import pika 
import uuid
import json
from flask import Flask, request
from flask_cors import CORS
import time

time.sleep(10)
# Initialisations
app = Flask(__name__)
CORS(app)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(
    exchange='ride',
    exchange_type='direct'
)
consumerData = []


# DataStructures
# queueRideSharing = channel.queue_declare(queue='rideSharingQueue') #durable=True
# channel.queue_declare(queue='rideSharingQueue')
# nameRideSharingQueue = queueRideSharing.method.queue
print("[x] Ready to send messages")
@app.route('/')
def home():
    return "Welcome to the Ride Sharing Service"

@app.route('/new_ride', methods=['POST'])
def new_ride():
    data = request.get_json(force=True)['data']
    #checking if consumer exists or not
    check = 0
    # print("consumerdATA ", type(consumerData[0]))
    # return type(data["consumerId"])
    if(len(consumerData) == 0):
        return "No Consumer In"
    for _, i in enumerate(consumerData):
        i_values = list(i.values())
        # return type(data["consumerId"])
        if str(data["consumerId"]) in i_values[0][0]:
            check = 1
    if(check==0):
        return str(consumerData)
    taskId = str(uuid.uuid4())
    data['taskId'] = taskId
    channel.basic_publish(exchange="ride",
                        routing_key = "ride_queue",
                        body = json.dumps(data))
    print (" [x] Sent data")
    # another exchange to send data to database
    channel.basic_publish(exchange="ride",
                        routing_key = "ride_database",
                        body = json.dumps(data))
    print (" [x] Sent data to database")
    return json.dumps({'taskId': taskId}), 200, {'ContentType':'application/json'}
    # connection.close()

@app.route('/new_ride_matching_consumer', methods=['POST'])
def new_ride_matching_consumer():
    data = request.get_json(force=True)['data']
    value = (data['consumerId'], data['serverIp'])
    key = (data['name'], data['consumerIp'])
    dic = {}
    dic[key] = value
    consumerData.append(dic)
    print(consumerData)
    return str(consumerData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
