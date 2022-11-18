import paho.mqtt.client as mqtt
import json
def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

def send_option(option: str, **kwargs):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("52.67.58.169",1883)
    if option == "generador":
        msg = {
            "frecuencia": kwargs["frecuencia"],
            "duty": kwargs["duty"],
            "enable": kwargs["enable"]
        }
        print(msg)
        client.publish("principal/generador",json.dumps(msg))
    elif option == "fuente":
        msg = {
            "voltPuerto1": kwargs["voltPuerto1"],
            "voltPuerto2": kwargs["voltPuerto2"],
            "enable": kwargs["enable"]
        }
        print(msg)
        client.publish("principal/fuente",json.dumps(msg))
    elif option == "multimetro":
        
        msg = {
            "tipoMult": kwargs["tipoMult"],
            "enable": kwargs["enable"]
        }
        print(msg)
        client.publish("principal/multimetro",json.dumps(msg))
    elif option == "osciloscopio":

        msg={
            "enable": kwargs["enable"]
        }
        print(msg)
        client.publish("principal/osciloscopio",json.dumps(msg))

