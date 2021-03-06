import paho.mqtt.client as mqtt
import mqtt_chat_system.mqtt_chat_library as MqttChatLibrary
from log_config import info_log, error_log

topics = MqttChatLibrary.topics

# Create admin
admin = mqtt.Client("Admin", True, None, mqtt.MQTTv31)
info_log.info("Admin has been initialized")
admin.on_connect = MqttChatLibrary.admin_on_connect
admin.on_message = MqttChatLibrary.admin_on_message

# Connect admin
admin.connect("mqtt.eclipse.org", 1883, 60)
info_log.info("Admin connected to broker")
admin.subscribe(topics.system_topic)
admin.subscribe(topics.system_request_topic)
admin.loop_start()

# Option for admin to terminate (on text input)
text = input()
admin.disconnect()
info_log.info("Admin disconnected from broker")
admin.loop_stop()
