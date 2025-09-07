import paho.mqtt.client as mqtt, time, json, random, os

BROKER = os.getenv("BROKER", "test.mosquitto.org")
TOPIC = "smarthealth/water"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

def publish_once(sensor_id):
    payload = {
        "sensor_id": sensor_id,
        "village": "VillageA",
        "pH": round(6.0 + random.random()*2,2),
        "turbidity": round(random.random()*10,2),
        "bacterial_index": round(random.random(),2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    client.publish(TOPIC, json.dumps(payload))
    print("Published", payload)

if __name__ == "__main__":
    for i in range(5):
        publish_once(f"S{i}")
        time.sleep(2)