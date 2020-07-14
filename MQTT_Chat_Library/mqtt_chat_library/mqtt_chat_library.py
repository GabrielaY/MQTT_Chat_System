import json
import paho.mqtt.client as mqtt
from datetime import datetime
import mqtt_chat_library.ChatPrototypes_pb2 as ChatPrototypes
from google.protobuf.json_format import MessageToJson

response_for_join_request = 0
topics = ChatPrototypes.Topics()
system_messages = ChatPrototypes.SystemMessages()


def wait_for_response_for_join_request():
    while not response_for_join_request:
        pass
    return response_for_join_request


def create_message(content, sender_name):
    chat_message = ChatPrototypes.ChatMessage()
    chat_message.content = content
    chat_message.sender = sender_name
    chat_message.timestamp = datetime.now().strftime("%T")
    return MessageToJson(chat_message)


# The callback for when the client receives a CONNACK response from the server.
def client_on_connect(client, userdata, flags, rc):
    print("Connected")
    system_message = create_message(system_messages.connected_text, client._client_id.decode("utf-8"))
    client.publish(topics.system_topic, system_message)


# The callback for when a PUBLISH message is received from the server.
def client_on_message(client, userdata, msg):
    received_message = json.loads(str(msg.payload.decode("utf-8")))
    client_id = client._client_id.decode("utf-8")

    if msg.topic == topics.system_response_topic + client_id:
        
        global response_for_join_request
        if received_message["content"] == system_messages.approve_join_text:
            print(system_messages.joined_text)
            client.subscribe(topics.chat_topic)
            response_for_join_request = 1
        else:
            print(system_messages.access_denied_text)
            disconnect_message = create_message(system_messages.disconnected_text, client_id)
            client.publish(topics.system_topic, disconnect_message)
            response_for_join_request = -1

    else:
        print(received_message["sender"] + ": " + received_message["content"] + " " + received_message["timestamp"])


# The callback for when the admin receives a CONNACK response from the server.
def admin_on_connect(self, userdata, flags, rc):
    print("Admin connected")


# The callback for when a PUBLISH message is received from the server.
def admin_on_message(client, userdata, msg):
    received_message = json.loads(str(msg.payload.decode("utf-8")))
    client_id = client._client_id.decode("utf-8")

    if msg.topic == topics.system_request_topic:

        if received_message["sender"][:1] == "a":
            response = create_message(system_messages.approve_join_text, client_id)
        else:
            response = create_message(system_messages.deny_join_text, client_id)

        response_topic = topics.system_response_topic + received_message["sender"]
        client.publish(response_topic, response)

    else:
        print(received_message["sender"] + ": " + received_message["content"] + " " + received_message["timestamp"])
