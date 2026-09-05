# Smart Home IoT Automation System - Team 11

## Team Members
* Karim Khaled Ismail
* Amaal Abdo
* Mohamed Samir

## Project Overview
A cloud-controlled Smart Home automation system based on MQTT architecture using HiveMQ Cloud, featuring a local publisher (Voice/Text) and a Raspberry Pi 4 Model B subscriber.

## Hardware & Pin Configuration
* Raspberry Pi 4 Model B
* LED 1: GPIO 17 | LED 2: GPIO 27 | LED 3: GPIO 22
* Servo Motor: GPIO 18 (requires `pigpio`)

## Dependencies
* Python 3.9+
* `paho-mqtt`, `gpiozero`, `pigpio`, `sounddevice`, `wavio`, `speech_recognition`

## Quick Execution Steps
1. **On Raspberry Pi (Subscriber):**
   ```bash
   sudo apt update && sudo apt install pigpio python3-pigpio -y
   pip3 install paho-mqtt gpiozero pigpio
   sudo systemctl enable pigpiod && sudo systemctl start pigpiod
   python3 subscriber.py
   ```
2. **On Local PC (Publisher):**
   ```bash
   python publisher.py
   ```
3. **Commands:** Choose text ('t') or voice ('v') for states like "entering home", "lights on", "area 1/2/3", or "getting out".
