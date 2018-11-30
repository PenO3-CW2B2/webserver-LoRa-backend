import paho.mqtt.client as mqtt
import configparser
import requests
import json
import base64

# read the config file
config = configparser.ConfigParser()
config.read('config.ini')


def updateBike(id, longitude, latitude, battery):
    r = requests.post('https://'+config['WebApp']['Host']+'/auth/bikes/'+str(id), data={'last_longitude': str(longitude), 'last_laltitude': str(latitude), 'battery': str(battery)}, headers={'Authorization': 'Token '+config['WebApp']['Token']})
    print(r.text)
    if r.status_code != 200:
        raise RuntimeError


def updateBikeSecret(id, secret):
    r = requests.post(config['WebApp']['Host']+'/auth/bikes/'+id, data={'secret': secret})
    if r.status_code != 200:
        raise RuntimeError


def endContract(id, endD):
    r = requests.post(config['WebApp']['Host']+'/auth/contracts/'+id+'/end', data={'end_time': endD})
    if r.status_code != 200:
        raise RuntimeError


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("test")
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config['LoRa']['App']+"/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
    data = json.loads(msg.payload.decode('utf-8'))
    location = data["metadata"]['gateways'][2]
    payload_data = base64.b64decode(data['payload_raw'])
    print('payload data= '+payload_data.decode())
    updateBike(2, location['longitude'], location['latitude'], 32767)


# Create the mqtt client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# start the connection
client.username_pw_set(config['LoRa']['Username'], config['LoRa']['Password'])
client.connect(config['LoRa']['host'], int(config['LoRa']['Port']))

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
