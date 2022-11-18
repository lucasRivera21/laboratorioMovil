import paho.mqtt.client as mqtt
import json
import pymysql

conn = pymysql.connect(
    host="localhost", 
    port=3306,
    user="root",
    password="l44bvmg2001",
    db="salidas"
)

cur = conn.cursor()

topics = [("salida/voltaje",0),("salida/osciloscopio",0)]

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    if msg.topic == "salida/voltaje":
        data = json.loads(msg.payload)
        output = data["voltajePagina"]
        print(data["voltajePagina"])
        query = 'INSERT INTO voltMult (voltaje) VALUES (%s)'
        cur.execute(query,(data["voltajePagina"]))
        conn.commit()
    elif msg.topic == "salida/osciloscopio":
        data = json.loads(msg.payload)
        output = data["voltajePagina"]
        print(output)
        # query = f'INSERT INTO voltOsc (voltaje) VALUES ({output})' 
        # cur.execute(query)
        # cur.commit()
    elif msg.topic == "salida/corriente":
        data = json.loads(msg.payload)
        output = data["corrientePagina"]
        print(output)
        # query = f'INSERT INTO corrienteMult (corriente) VALUES ({output})'
        # cur.execute(query)
        # cur.commit()
        # cur.close()

def listen():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("52.67.58.169",1883)
    client.subscribe(topics)
    client.loop_forever()

if __name__ == "__main__":
    listen()