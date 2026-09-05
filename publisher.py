#team 11

import os
import sys
import paho.mqtt.client as mqtt
import ssl
import sounddevice as sd
import wavio
import speech_recognition as sr

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
client.username_pw_set("karimkhaled", "12345678")
client.connect("503f7ededacf4c179546929b67d5884f.s1.eu.hivemq.cloud", 8883, 60)
client.loop_start()

def record_voice(filename="voice_cmd.wav", duration=4):
    print("\nListening...")
    audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='int16')
    sd.wait()
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    wavio.write(filename, audio, 16000, sampwidth=2)
    return filename

recognizer = sr.Recognizer()
print("Publisher Ready!")

while True:
    try:
        mode = input("\nChoose Mode -> Type 'v' for Voice OR 't' for Text (Ctrl+C to quit): ").strip().lower()
        
        if mode == 'v':
            input("Press Enter to start recording...")
            audio_file = record_voice()
            print("Processing voice...")
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"You said: {text}")
            client.publish("karimkhaled", text)
            
        elif mode == 't':
            text = input("Enter command to send: ").strip()
            if text:
                print(f"Sending text: {text}")
                client.publish("karimkhaled", text)
                
        else:
            print("Invalid mode. Please type 'v' or 't'.")
            
    except sr.UnknownValueError:
        print("Could not understand audio, try again.")
    except sr.RequestError:
        print("API Unavailable.")
    except KeyboardInterrupt:
        print("\nExiting Publisher...")
        client.loop_stop()
        client.disconnect()
        sys.exit()
