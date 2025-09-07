import paho.mqtt.client as mqtt, json, requests, os
API = os.getenv("API_URL","http://api:8000/report/water")
BROKER = os.getenv("BROKER","test.mosquitto.org")
TOPIC = "smarthealth/water"

def on_message(client, userdata, msg):
    payload=json.loads(msg.payload.decode())
    print("Received", payload)
    try:
        requests.post(API, json=payload, timeout=5)
    except Exception as e:
        print("Failed to post to API:", e)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)
client.loop_forever()