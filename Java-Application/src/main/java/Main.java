import message.ChatPrototypes;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.util.Scanner;
import java.io.IOException;

public class Main {

    public static void main(String[] args) throws IOException {

        // Get topics and system messages
        ChatPrototypes.Topics topics = ChatPrototypes.Topics.getDefaultInstance();
        ChatPrototypes.SystemMessages systemMessages = ChatPrototypes.SystemMessages.getDefaultInstance();

        // Used so that the main can wait for the admin to respond to the join request
        Object syncObject = new Object();

        // Broker info
        String broker = "tcp://mqtt.eclipse.org:1883";
        MemoryPersistence memoryPersistence = new MemoryPersistence();

        // Input reader
        Scanner scanner = new Scanner(System.in);

        // Client info
        System.out.println("Enter username: ");
        String clientId = scanner.nextLine();
        final String responseTopic = "/chat/" + clientId + "/response";

        try {
            // Create client
            MqttClient client = new MqttClient(broker, clientId, memoryPersistence);

            // Create connection options
            MqttConnectOptions options = new MqttConnectOptions();
            options.setAutomaticReconnect(true);
            options.setCleanSession(true);
            options.setConnectionTimeout(10);

            // Connect to broker and publish to administrator
            client.connect(options);
            ChatPrototypes.ChatMessage connectedMessage = ChatPrototypes.ChatMessage.newBuilder()
                    .setContent(systemMessages.getConnectedText())
                    .setSender(clientId)
                    .setTimestamp(MessageInitializer.generateTimeStamp())
                    .build();
            MessageDispatcher.sendMessage(client, topics.getSystemTopic(), MessageInitializer.generateMqttMessage(connectedMessage));

            // Subscribe to response topic
            client.subscribe(responseTopic, (topic, message) -> MessageDispatcher.receiveMessage(topic, message.toString(), client, syncObject));

            // Try to join group topic
            ChatPrototypes.ChatMessage requestMessage = ChatPrototypes.ChatMessage.newBuilder()
                    .setContent(systemMessages.getRequestJoinText())
                    .setSender(clientId)
                    .setTimestamp(MessageInitializer.generateTimeStamp())
                    .build();
            MessageDispatcher.sendMessage(client, topics.getSystemRequestTopic(), MessageInitializer.generateMqttMessage(requestMessage));

            // Wait for response
            synchronized (syncObject) {
                try {
                    syncObject.wait();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            while (scanner.hasNextLine()) {
                // Read message from System.in
                String messageToBeSent = scanner.nextLine();

                // Check if user has finished chatting
                if (messageToBeSent.equals("QUIT")) {
                    // Disconnect and publish to administrator
                    ChatPrototypes.ChatMessage disconnectMessage = ChatPrototypes.ChatMessage.newBuilder()
                            .setContent(systemMessages.getDisconnectedText())
                            .setSender(clientId)
                            .setTimestamp(MessageInitializer.generateTimeStamp())
                            .build();
                    MessageDispatcher.sendMessage(client, topics.getSystemTopic(), MessageInitializer.generateMqttMessage(disconnectMessage));
                    client.disconnect();
                    System.exit(0);
                }

                // Create and publish message
                ChatPrototypes.ChatMessage message = ChatPrototypes.ChatMessage.newBuilder()
                        .setContent(messageToBeSent)
                        .setSender(clientId)
                        .setTimestamp(MessageInitializer.generateTimeStamp())
                        .build();
                MessageDispatcher.sendMessage(client, topics.getChatTopic(), MessageInitializer.generateMqttMessage(message));

            }
        } catch (MqttException e) {
            System.out.println("Cause -> " + e.getCause());
            System.out.println("Message -> " + e.getMessage());
            e.printStackTrace();
        }
    }
}