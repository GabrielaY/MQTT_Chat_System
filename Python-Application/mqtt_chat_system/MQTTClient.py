import json
import paho.mqtt.client as mqtt
from datetime import datetime
import mqtt_chat_system.ProtoBuffer.ChatPrototypes_pb2 as ChatPrototypes
from google.protobuf.json_format import MessageToJson

topics = ChatPrototypes.Topics()
system_messages = ChatPrototypes.SystemMessages()


# Helper function for creating message
def create_message(content, sender_name):
    chat_message = ChatPrototypes.ChatMessage()
    chat_message.content = content
    chat_message.sender = sender_name
    chat_message.timestamp = datetime.now().strftime("%T")
    return MessageToJson(chat_message)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected")
    system_message = create_message(system_messages.connected_text, client_name)
    client.publish(topics.system_topic, system_message)


# The callback for when a PUBLISH message is received from the server.
def on_message(self, userdata, msg):
    received_message = json.loads(str(msg.payload.decode("utf-8")))

    if msg.topic == "/chat/" + client_name + "/response":  # /chat/response/ + client_name
        if received_message["content"] == system_messages.approve_join_text:
            print(system_messages.joined_text)
            python_client.subscribe(topics.chat_topic)
            global group_response
            group_response = 1
        else:
            print(system_messages.access_denied_text)
            disconnect_message = create_message(system_messages.disconnected_text, client_name)
            python_client.publish(topics.system_topic, disconnect_message)
            group_response = -1

    else:
        print(received_message["sender"] + ": " + received_message["content"] + " " + received_message["timestamp"])


client_name = input("Enter username: ")
python_client = mqtt.Client(client_name, True, None, mqtt.MQTTv31)
python_client.on_connect = on_connect
python_client.on_message = on_message
python_client.connect("mqtt.eclipse.org", 1883, 60)
python_client.loop_start()

python_client.subscribe("/chat/" + client_name + "/response")

# Request group access
group_response = 0
message = create_message(system_messages.request_join_text, client_name)
python_client.publish(topics.system_request_topic, message)

while not group_response:
    pass

if group_response == -1:
    exit()

while True:
    text = input()
    if text == "QUIT":
        message = create_message(system_messages.disconnected_text, client_name)
        python_client.publish(topics.system_topic, message)
        break

    message = create_message(text, client_name)
    python_client.publish(topics.chat_topic, message)

python_client.disconnect()
python_client.loop_stop()
