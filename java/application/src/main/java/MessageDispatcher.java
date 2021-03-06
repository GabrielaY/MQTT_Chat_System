import chat_topics.TopicsOuterClass;
import chat_message.MessagePrototype;
import system_messages.SystemMessagesOuterClass;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import com.google.protobuf.util.JsonFormat;
import com.google.protobuf.InvalidProtocolBufferException;

public class MessageDispatcher {

    // Get topics and system messages
    private static final TopicsOuterClass.Topics topics =  TopicsOuterClass.Topics.getDefaultInstance();
    private static final SystemMessagesOuterClass.SystemMessages systemMessages = SystemMessagesOuterClass.SystemMessages.getDefaultInstance();

    // Send message
    public static void sendMessage(MqttClient client, String topic, MqttMessage message) {
        try {
            client.publish(topic, message);
        } catch (MqttException e) {
            System.out.println("Cause -> " + e.getCause());
            System.out.println("Message -> " + e.getMessage());
            System.out.println("Reason Code -> " + e.getReasonCode());
            e.printStackTrace();
        }
    }

    // Receive message
    public static void receiveMessage(String topic, String payload, MqttClient client, Object syncObject) throws MqttException, InvalidProtocolBufferException {
        // Get message from payload
        MessagePrototype.ChatMessage.Builder builder = MessagePrototype.ChatMessage.newBuilder();
        JsonFormat.parser().merge(payload, builder);
        MessagePrototype.ChatMessage message = builder.build();
        
        if (topic.equals(topics.getSystemResponseTopic() + client.getClientId())) {

            if (message.getContent().equals(systemMessages.getApproveJoinText())){
                System.out.println(systemMessages.getJoinedText());
                MQTTChatLogger.makeInfoLog(client.getClientId() + " -> " + systemMessages.getJoinedText());
                client.subscribe(topics.getChatTopic(), (tpc, msg) -> MessageDispatcher.receiveMessage(tpc, msg.toString(), client, syncObject));
                synchronized(syncObject) {
                    syncObject.notify();
                }
            }

            else {
                System.out.println(systemMessages.getAccessDeniedText());
                MQTTChatLogger.makeErrorLog(client.getClientId() + " -> " + systemMessages.getAccessDeniedText());
                MessagePrototype.ChatMessage disconnectMessage = MessagePrototype.ChatMessage.newBuilder()
                        .setContent(systemMessages.getDisconnectedText())
                        .setSender(client.getClientId())
                        .setTimestamp(MessageInitializer.generateTimeStamp())
                        .build();
                MessageDispatcher.sendMessage(client, topics.getSystemTopic(), MessageInitializer.generateMqttMessage(disconnectMessage));
                client.disconnect();
                MQTTChatLogger.makeErrorLog(client.getClientId() + " -> " + systemMessages.getDisconnectedText());
                System.exit(-1);
            }
        }
        else {
            System.out.println(message.getSender() + ": " + message.getContent() + " " + message.getTimestamp());
        }
    }

}
