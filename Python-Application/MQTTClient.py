import paho.mqtt.client as mqtt
import mqtt_chat_library.mqtt_chat_library as MqttChatLibrary

topics = MqttChatLibrary.topics
system_messages = MqttChatLibrary.system_messages

# Create client
client_name = input("Enter username: ")
python_client = mqtt.Client(client_name, True, None, mqtt.MQTTv31)
python_client.on_connect = MqttChatLibrary.client_on_connect
python_client.on_message = MqttChatLibrary.client_on_message

# Connect client
python_client.connect("mqtt.eclipse.org", 1883, 60)
python_client.subscribe("/chat/" + client_name + "/response")
python_client.loop_start()

# Request group access
message = MqttChatLibrary.create_message(system_messages.request_join_text, client_name)
python_client.publish(topics.system_request_topic, message)

# Wait for response
response = MqttChatLibrary.wait_for_response_for_join_request()
if response == -1:
    exit()

# Activate chat for client
while True:
    text = input()

    # Option for client to quit
    if text == "QUIT":
        message = MqttChatLibrary.create_message(system_messages.disconnected_text, client_name)
        python_client.publish(topics.system_topic, message)
        break

    message = MqttChatLibrary.create_message(text, client_name)
    python_client.publish(topics.chat_topic, message)

# Disconnect client
python_client.disconnect()
python_client.loop_stop()
