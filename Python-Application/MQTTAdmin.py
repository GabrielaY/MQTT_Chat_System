from datetime import datetime
import json
import paho.mqtt.client as mqtt
import ProtoBuffer.ChatPrototypes_pb2 as ChatPrototypes
from google.protobuf.json_format import MessageToDict, MessageToJson

# from MQTTClient import topics, system_messages, create_message

topics = ChatPrototypes.Topics()
system_messages = ChatPrototypes.SystemMessages()


# Helper function for creating message
def create_message(content, sender_name):
    chat_message = ChatPrototypes.ChatMessage()
    chat_message.content = content
    chat_message.timestamp = datetime.now().strftime("%T")
    return MessageToJson(chat_message)


# The callback for when the admin receives a CONNACK response from the server.
def on_connect(self, userdata, flags, rc):
    print("connected")


# The callback for when a PUBLISH message is received from the server.
def on_message(self, userdata, msg):

    received_message = json.loads(str(msg.payload.decode("utf-8")))

    if msg.topic == topics.system_request_topic:

        if received_message["sender"][:1] == "a":
            response = create_message(system_messages.approve_join_text, None)

        else:
            response = create_message(system_messages.deny_join_text, None)

        response_topic = "/chat/" + received_message["sender"] + "/response"
        admin.publish(response_topic, response)

    else:
        print(received_message["sender"] + ": " + received_message["content"] + " " + received_message["timestamp"])


admin = mqtt.Client("Admin", True, None, mqtt.MQTTv31)
admin.on_connect = on_connect
admin.on_message = on_message

admin.connect("mqtt.eclipse.org", 1883, 60)
admin.subscribe(topics.system_topic)
admin.subscribe(topics.system_request_topic)
admin.loop_start()

# Option for admin to terminate (on text input)
text = input()
admin.disconnect()
admin.loop_stop()
