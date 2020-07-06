import json
import paho.mqtt.client as mqtt


# The callback for when the admin receives a CONNACK response from the server.
def on_connect(self, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(self, userdata, message):
    message = json.loads(str(message.payload.decode("utf-8")))
    print(message["sender"] + ": " + message["content"] + " " + message["timestamp"])


admin = mqtt.Client("Admin", True, None, mqtt.MQTTv31)
admin.on_connect = on_connect
admin.on_message = on_message

admin.connect("mqtt.eclipse.org", 1883, 60)
admin.subscribe("/chat/system")
admin.loop_forever()