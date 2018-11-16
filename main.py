import paho.mqtt.client as mqtt
import configparser
import mysql.connector

# read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# connect to the database with MySQL
db = mysql.connector.connect(
  host=config['MySQL']['Host'],
  user=config['MySQL']['Username'],
  passwd=config['MySQL']['Password'],
  database=config['MySQL']['Database'])

def updateBike(id, longtitude, altitude, battery):
    db.cursor().execute("""
    UPDATE bikes_bike
    SET longtitude = (?), altitude = (?), battery = (?)
    WHERE {} = id;
    """, (longtitude, altitude, battery))

def updateBikeSecret(id, secret):
    db.cursor().execute("""
    UPDATE bikes_bike
    SET secret = (?)
    WHERE {} = id;
    """, (secret,))

def endContract(id, startD):
    db.cursor().execute("""
    UPDATE bikes_contract
    SET startD = (?)
    WHERE EXISTS (
    SELECT bikes_bike.id
    FROM bikes_bike, bikes_contract
    WHERE bikes_bike.id = bikes_contract.bike_id
    AND bikes_contract.time_end = NULL
    );
    """, (startD,))

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("test")
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    db.cursor().execute("")

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
