import paho.mqtt.client as mqtt
import json

topics = [("salida/voltaje",0),("salida/osciloscopio",0)]
output = None

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    global output
    if msg.topic == "salida/voltaje":
        data = json.loads(msg.payload)
        output = data["voltajePagina"]
        print(output)
    elif msg.topic == "salida/osciloscopio":
        data = json.loads(msg.payload)
        output = data["voltajePagina"]

def listen():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("18.228.232.219",1883)
    client.subscribe(topics)
    client.loop_forever()

