import paho.mqtt.client as mqtt
import configparser
import requests

# read the config file
config = configparser.ConfigParser()
config.read('config.ini')


def updateBike(id, longtitude, altitude, battery):
    r = requests.post(config['WebApp']['Host']+'/bikes/'+id, data={'last_longtitude': longtitude, 'last_laltitude': altitude, 'battery': battery})
    if r.status_code != 200:
        raise RuntimeError


def updateBikeSecret(id, secret):
    r = requests.post(config['WebApp']['Host']+'/bikes/'+id, data={'secret': secret})
    if r.status_code != 200:
        raise RuntimeError


def endContract(id, endD):
    r = requests.post(config['WebApp']['Host']+'/contracts/'+id+'/end', data={'end_time': endD})
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
    print(msg.topic+" "+str(msg.payload))


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
