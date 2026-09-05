#team 11
import os
import sys
import paho.mqtt.client as mqtt
import time
import ssl
from gpiozero import LED, Servo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
led1 = LED(17)
led2 = LED(27)
led3 = LED(22)
servo = Servo(18, pin_factory=factory)

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Subscriber connected to HiveMQ successfully! Waiting for Smart Home commands...")
        client.subscribe("karimkhaled")
    else:
        print(f"Connection failed with code {reason_code}")

def on_message(client, userdata, msg):
    command_text = msg.payload.decode().lower().strip()
    print(f"Received Command: {command_text}")
    process_smart_home(command_text)

def process_smart_home(text):
    if "entering home" in text:
        print("Executing: Entering Home Scenario...")
        servo.max()
        led1.on()
        led2.on()
        led3.on()
    elif "getting out" in text:
        print("Executing: Getting Out Scenario...")
        servo.min()
        led1.off()
        led2.off()
        led3.off()
    elif "lights on" in text:
        print("Executing: All Lights On...")
        led1.on()
        led2.on()
        led3.on()
    elif "area 1" in text:
        print("Toggling Area 1 Light...")
        led1.toggle()
    elif "area 2" in text:
        print("Toggling Area 2 Light...")
        led2.toggle()
    elif "area 3" in text:
        print("Toggling Area 3 Light...")
        led3.toggle()
    elif "exit" in text or "stop" in text:
        print("Exiting Subscriber...")
        client.loop_stop()
        client.disconnect()
        sys.exit()

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("karimkhaled", "12345678")
client.connect("503f7ededacf4c179546929b67d5884f.s1.eu.hivemq.cloud", 8883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nDisconnecting Subscriber...")
    client.disconnect()
    sys.exit()