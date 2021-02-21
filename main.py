#!/usr/bin/env python3

import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep

# Sensor Setup
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4 # GPIO Pinout.

# Relay Setup
GPIO.setmode(GPIO.BCM)  # Using BCM Pinout
GPIO.setwarnings(False)

R1: int = 22
R2: int = 23
R3: int = 24
R4: int = 25

RELAYS = [R1, R2, R3, R4]

GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)

# Humidity & Temperature Range
HUM_HIGH: int = 90
HUM_LOW: int = 75
TEMP_HIGH: int = 40
TEMP_LOW: int = 30

# Set the value to True/Flase depending on your relay module. 
# Use True for active low relay module.
# Use False for active high relay module.
INVERT = True

HIGH = GPIO.HIGH if not INVERT else GPIO.LOW
LOW = GPIO.LOW if not INVERT else GPIO.HIGH
ON = 1 if not INVERT else 0
OFF = 0 if not INVERT else 1

if INVERT:
    for pin in RELAYS:
        GPIO.output(pin, GPIO.HIGH)


try:
    
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:

            if humidity <= HUM_LOW and GPIO.input(R1) == OFF:
                GPIO.output(R1, HIGH)
                print("Relay turned ON")
            elif humidity >= HUM_HIGH and GPIO.input(R1) == ON:
                GPIO.output(R1, LOW)
                print("Relay turned OFF")

            print(f"Humidity is {humidity}, Temperature is {temperature}")
            sleep(0.5)
        else:
            print("Failed to load data.")
except KeyboardInterrupt:
    GPIO.cleanup()


