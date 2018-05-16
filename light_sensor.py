#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
import requests
from requests import Session
from requests.exceptions import HTTPError


__author__ = 'Gus (Adapted from Adafruit)'
__license__ = "GPL"
__maintainer__ = "pimylifeup.com"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(9,GPIO.OUT)

#define the pin that goes to the circuit
pin_to_circuit = 7
pin_to_light = 11
limiar = 36
tolerancia = 10
counter = 0
proximo = 100


def salva_firebase(velocidade):
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://projetoxamarin.firebaseio.com/', None)
    result = firebase.post('/rasp', velocidade)
    print result
def rc_time (pin_to_circuit):
    count = 0
    
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
    #time.sleep(0.001)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1
        #print(count)

    return count

#Catch when script is interupted, cleanup correctly
try:
     
    # Main loop
    inicial = time.time()
    GPIO.output(pin_to_light,1)
    passou = 0
    anterior = 0
    while time.time() - inicial <= 10:
    #while(True):
        proximo = rc_time(pin_to_circuit)
        print(proximo)
        if(limiar > proximo and passou < 2):
            print("talvez esteja dentro")
            passou = 1+passou
            anterior = proximo
        elif (passou == 2 and anterior + tolerancia > proximo):
            print("Volta completa")
            counter=counter+1
            lido = rc_time(pin_to_circuit)
            while (limiar+tolerancia > lido):
                print("==============================" + str(lido))
                lido = rc_time(pin_to_circuit)
            passou = 0
        elif (passou == 1 and anterior + tolerancia < proximo):
            passou = 0
       
            
    GPIO.output(pin_to_light,0)
    print("demos: "+str(counter) + " voltas")
    distancia = 2*3.14*6*counter/100
    print("Distancia percorrida: " + str(distancia) +"m")
    tempo = time.time() - inicial
    print("Tempo total: " + str(tempo))
    velocidade = distancia/tempo
    velocidade = velocidade*3.6
    print("Velocidade: " + str(velocidade) + "km/h")
    salva_firebase(velocidade)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
