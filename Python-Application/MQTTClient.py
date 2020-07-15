import paho.mqtt.client as mqtt
import mqtt_chat_library.mqtt_chat_library as MqttChatLibrary
from log_config import info_log, error_log

topics = MqttChatLibrary.topics
system_messages = MqttChatLibrary.system_messages

# Create client
client_name = input("Enter username: ")
python_client = mqtt.Client(client_name, True, None, mqtt.MQTTv31)
python_client.on_connect = MqttChatLibrary.client_on_connect
python_client.on_message = MqttChatLibrary.client_on_message

# Connect client
python_client.connect("mqtt.eclipse.org", 1883, 60)
info_log.info("%s connected to broker" % client_name)
python_client.subscribe(topics.system_response_topic + client_name)
info_log.info("%s subscribed to topic: %s" % (client_name, topics.system_request_topic + client_name))
python_client.loop_start()

# Request group access
message = MqttChatLibrary.create_message(system_messages.request_join_text, client_name)
python_client.publish(topics.system_request_topic, message)
info_log.info("%s published a message to topic: %s" % (client_name, topics.system_request_topic))

# Wait for response
response = MqttChatLibrary.wait_for_response_for_join_request()
if response == -1:
    error_log.error("Access denied!")
    exit()

# Activate chat for client
while True:
    text = input()

    # Option for client to quit
    if text == "QUIT":
        message = MqttChatLibrary.create_message(system_messages.disconnected_text, client_name)
        python_client.publish(topics.system_topic, message)
        info_log.info("%s disconnected from broker" % client_name)
        break

    message = MqttChatLibrary.create_message(text, client_name)
    python_client.publish(topics.chat_topic, message)
    info_log.info("%s published a message to topic: %s" % (client_name, topics.chat_topic))

# Disconnect client
python_client.disconnect()
python_client.loop_stop()
