from machine import Pin, ADC, DAC, PWM
from time import sleep
import network
from umqttsimple import MQTTClient
import ujson

SSID = "Wi-Fi Unimagdalena"
PASSWORD = ""
client = MQTTClient("prueba", "18.228.232.219")
#ENTRADAS
#CONTINUIDAD(PIN 5), VOLTÍMETRO(PIN 34, 35 ADC)

#SALIDAS
#FUENTE(PIN 25, 26 DAC)

#EQUILIBRAR ADC
def equilibrio(valor_ADC):
    if valor_ADC > 3600:
        return valor_ADC*1.11
    elif valor_ADC > 3400:
        return valor_ADC*1.13
    elif valor_ADC > 3100:
        return valor_ADC*1.16
    elif valor_ADC > 3000:
        return valor_ADC*1.17
    elif valor_ADC > 2700:
        return valor_ADC*1.18
    elif valor_ADC > 2600:
        return valor_ADC*1.19
    elif valor_ADC > 2300:
        return valor_ADC*1.2
    elif valor_ADC > 2000:
        return valor_ADC*1.21
    elif valor_ADC > 1900:
        return valor_ADC*1.22
    elif valor_ADC > 1700:
        return valor_ADC*1.23
    elif valor_ADC > 1500:
        return valor_ADC*1.24
    elif valor_ADC > 1400:
        return valor_ADC*1.26
    elif valor_ADC > 1200:
        return valor_ADC*1.28
    elif valor_ADC > 1000:
        return valor_ADC*1.3
    elif valor_ADC > 900:
        return valor_ADC*1.34
    elif valor_ADC > 800:
        return valor_ADC*1.36
    elif valor_ADC > 700:
        return valor_ADC*1.4
    elif valor_ADC > 600:
        return valor_ADC*1.45
    elif valor_ADC > 500:
        return valor_ADC * 1.5
    elif valor_ADC > 400:
        return valor_ADC*1.59
    elif valor_ADC > 300:
        return valor_ADC*1.72
    elif valor_ADC > 200:
        return valor_ADC*2
    elif valor_ADC > 100:
        return valor_ADC*2.4
    else:
        return valor_ADC*5

def multimetro(tipoMult, enable):
    entrada = Pin(5, Pin.IN, Pin.PULL_UP)
    led = Pin(22,Pin.OUT, value = 0)
    adc = ADC(Pin(34, mode=Pin.IN))
    adc2 = ADC(Pin(35, mode=Pin.IN))
    if enable == True:
        print("ESTAS EN MULTIMETRO")
        if tipoMult == "continuidadMult":

            #CONTINUIDAD
            print("estas en continuidad")
            print(entrada.value())
            sleep(0.01)
            if entrada.value():
                led.on()
            else:
                led.off()
    
        elif tipoMult == "voltMult":
            #VOLTÍMETROS
            print("estás en voltímetro")
            adc.atten(ADC.ATTN_11DB)
            adc.width(ADC.WIDTH_12BIT)
        
            valor_ADC = adc.read()
            valor_ADC = equilibrio(valor_ADC)
            valor_ADC = valor_ADC*(3/(4095*0.1))
                
            adc2.atten(ADC.ATTN_11DB)
            adc2.width(ADC.WIDTH_12BIT)

            valor_ADC2 = adc2.read()
            valor_ADC2 = equilibrio(valor_ADC2)
            valor_ADC2 = valor_ADC2*(3/(4095*0.1))
            
            
            voltajePagina = round(valor_ADC, 2) - round(valor_ADC2, 2)
            msg = {
                    "voltajePagina": voltajePagina
                }
            print(msg)
            client.publish("salida/voltaje", ujson.dumps(msg))
            sleep(1)
    elif enable == False:
        led.off()
        
#FUENTE DE VOLTAJE

def fuente(voltPuerto1, voltPuerto2, enable = True):
    #PUERTO 1
    salidaDAC = DAC(Pin(25))
    voltajeDeseado = float(voltPuerto1)
    amplificador = (voltajeDeseado)/3.136
    print(amplificador)
    sleep(1)
    valorDAC = 255*amplificador/3.187
    print(round(valorDAC))
    sleep(1)
    salidaDAC.write(round(valorDAC))
    
    #PUERTO2
    salidaDAC2 = DAC(Pin(26))
    voltajeDeseado = float(voltPuerto2)
    amplificador = (voltajeDeseado)/3.136
    print(amplificador)
    sleep(1)
    valorDAC = 255*amplificador/3.187
    print(round(valorDAC))
    sleep(1)
    salidaDAC2.write(round(valorDAC))
    
    #desabilitación
    if enable == "False":
        salidaDAC1.deinit()
        salidaDAC2.deinit()
    
#GENERADOR DE SEÑALES
def generador(frecuencia, duty, enable):
    frecuencia = int(frecuencia)
    dutyDeseado = int(duty)
    dutyDeseado = 1023 * dutyDeseado/100
    pwmSignal = PWM(Pin(15), frecuencia)
    pwmSignal.duty(round(dutyDeseado))
    if enable == "False":
        pwmSignal.deinit()
        
#OSCILOSCOPIO
def osciloscopio(enable):
    adc = ADC(Pin(34, mode=Pin.IN))
    adc2 = ADC(Pin(35, mode=Pin.IN))
    if enable == "True":
        #PUERTO 1
        adc.atten(ADC.ATTN_11DB)
        adc.width(ADC.WIDTH_12BIT)
        
        valor_ADC = adc.read()
        valor_ADC = equilibrio(valor_ADC)
        valor_ADC = valor_ADC*(3/(4095*0.1))
        print(valor_ADC)
        
        #PUERTO 2
        adc2.atten(ADC.ATTN_11DB)
        adc2.width(ADC.WIDTH_12BIT)

        valor_ADC2 = adc2.read()
        valor_ADC2 = equilibrio(valor_ADC2)
        valor_ADC2 = valor_ADC2*(3/(4095*0.1))
        print(valor_ADC2)    

loop_entrada = b'algo'
def main_callback(topic,msg):
    global loop_entrada
    loop_entrada = topic
    
    global loop_msg
    loop_msg = msg
    
    if topic == b'principal/generador':
        print(msg.decode())
        data = ujson.loads(msg.decode())
        generador(**data)
    elif topic == b'principal/fuente':
        print(msg.decode())
        print("estas en fuente")
        data = ujson.loads(msg.decode())
        print(data)
        fuente(**data)
    elif topic == b'principal/multimetro':
        print("estas en multimetro")
        data = ujson.loads(msg.decode())
        multimetro(**data)
    elif topic == b'principal/osciloscopio':
        print(msg.decode())
        print("estas en osciloscopio")
        data = ujson.loads(msg.decode())
        print(data)
        osciloscopio(**data)

def do_connect(SSID, PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(SSID, PASSWORD)

        while not wlan.isconnected():
            pass
    print("network config:", wlan.ifconfig())
    
do_connect(SSID,PASSWORD)
client.set_callback(main_callback)
client.connect()
client.subscribe("principal/#")


while True:
    client.check_msg()
    
    if loop_entrada == b'principal/multimetro':
        #print(loop_msg.decode())
        #print("estas en multimetro")
        loop_data = ujson.loads(loop_msg.decode())
        print(loop_data)
        multimetro(**loop_data)
        sleep(1)
   
        