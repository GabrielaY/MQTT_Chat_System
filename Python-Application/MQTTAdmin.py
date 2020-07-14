import paho.mqtt.client as mqtt
import mqtt_chat_library.mqtt_chat_library as MqttChatLibrary

topics = MqttChatLibrary.topics

# Create admin
admin = mqtt.Client("Admin", True, None, mqtt.MQTTv31)
admin.on_connect = MqttChatLibrary.admin_on_connect
admin.on_message = MqttChatLibrary.admin_on_message

# Connect admin
admin.connect("mqtt.eclipse.org", 1883, 60)
admin.subscribe(topics.system_topic)
admin.subscribe(topics.system_request_topic)
admin.loop_start()

# Option for admin to terminate (on text input)
text = input()
admin.disconnect()
admin.loop_stop()
