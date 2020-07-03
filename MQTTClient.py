import json
import paho.mqtt.client as mqtt
from datetime import datetime


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    system_message = json.dumps(
        {"content": "connected",
         "sender": client.client_id.decode("utf-8"),
         "timestamp": datetime.now().strftime("%T")})
    client.publish("/chat/system", system_message)


# The callback for when a PUBLISH message is received from the server.
def on_message(self, userdata, received_message):
    received_message = json.loads(str(received_message.payload.decode("utf-8")))
    print(received_message["sender"] + ": " + received_message["content"] + " " + received_message["timestamp"])


client_name = input("Enter username: ")
python_client = mqtt.Client(client_name, True, None, mqtt.MQTTv31)
python_client.on_connect = on_connect
python_client.on_message = on_message
python_client.connect("mqtt.eclipse.org", 1883, 60)
python_client.loop_start()
python_client.subscribe("/chat/messages")

while True:
    text = input()
    if text == "QUIT":
        message = json.dumps(
            {"content": "disconnected",
             "sender": python_client.client_id.decode("utf-8"),
             "timestamp": datetime.now().strftime("%T")})
        python_client.publish("/chat/system", message)
        break
    message = json.dumps(
        {"content": text,
         "sender": python_client.client_id.decode("utf-8"),
         "timestamp": datetime.now().strftime("%T")})
    python_client.publish("/chat/messages", message)

python_client.disconnect()
python_client.loop_stop()
