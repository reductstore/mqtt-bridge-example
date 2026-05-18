import json
import random
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "mosquitto"
BROKER_PORT = 1883
TOPIC = "sensor/data"
RETRY_DELAY_SECONDS = 2
PUBLISH_INTERVAL_SECONDS = 1


def connect_with_retry(client: mqtt.Client) -> None:
    while True:
        try:
            client.connect(BROKER_HOST, BROKER_PORT, 60)
            print(f"Connected to MQTT broker at {BROKER_HOST}:{BROKER_PORT}")
            return
        except Exception as err:  # pylint: disable=broad-except
            print(f"MQTT connection failed: {err}. Retrying in {RETRY_DELAY_SECONDS}s...")
            time.sleep(RETRY_DELAY_SECONDS)


def main() -> None:
    client = mqtt.Client()
    connect_with_retry(client)
    client.loop_start()

    try:
        while True:
            data = {
                "temperature": round(random.uniform(20.0, 60.0), 2),
                "pressure": round(random.uniform(900.0, 1100.0), 2),
            }
            payload = json.dumps(data)
            result = client.publish(TOPIC, payload, qos=1)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"Published to {TOPIC}: {data}")
            else:
                print(f"Publish failed with code {result.rc}: {data}")
            time.sleep(PUBLISH_INTERVAL_SECONDS)
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
