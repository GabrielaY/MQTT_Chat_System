from datetime import datetime
import json
import paho.mqtt.client as mqtt


# The callback for when the admin receives a CONNACK response from the server.
def on_connect(self, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(self, userdata, msg):
    received_message = json.loads(str(msg.payload.decode("utf-8")))

    if msg.topic == "/chat/system/request":
        if received_message["sender"][:1] == "a":
            response = json.dumps({
                "content": "yes",
                "timestamp": datetime.now().strftime("%T")
            })
        else:
            response = json.dumps({
                "content": "no",
                "timestamp": datetime.now().strftime("%T")
            })

        response_topic = "/chat/" + received_message["sender"] + "/response"
        admin.publish(response_topic, response)

    else:
        print(received_message["sender"] + ": " + received_message["content"] + " " + received_message["timestamp"])


admin = mqtt.Client("Admin", True, None, mqtt.MQTTv31)
admin.on_connect = on_connect
admin.on_message = on_message

admin.connect("mqtt.eclipse.org", 1883, 60)
admin.subscribe("/chat/system")
admin.subscribe("/chat/system/request")
admin.loop_start()

# Option for admin to terminate (on text input)
text = input()
admin.disconnect()
admin.loop_stop()
