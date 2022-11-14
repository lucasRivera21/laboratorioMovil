import paho.mqtt.client as mqtt
import json
def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
def send_option(option: str, frec=None, duty=None, enable=True):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("52.67.100.141",1883)
    if option == "generador":
        msg = {
            "frecuencia": frec,
            "duty": duty,
            "enable": enable
        }
        print(msg)
        client.publish("principal/generador",json.dumps(msg))
    elif option == "fuente":
        msg = {
            "voltPuerto1": frec,
            "voltPuerto2": duty,
            "enable": enable
        }
        print(msg)
        client.publish("principal/fuente",json.dumps(msg))
    elif option == "multimetro":
        
        msg = {
            "tipoMult": frec,
            "enable": enable
        }
        print(msg)
        client.publish("principal/multimetro",json.dumps(msg))