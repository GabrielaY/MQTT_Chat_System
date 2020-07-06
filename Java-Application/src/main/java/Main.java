import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        // Constants
        final String messageTopic = "/chat/messages";
        final String systemTopic = "/chat/system";
        final String connectionMessage = "connected";
        final String disconnectionMessage = "disconnected";
        final int defaultQualityOfService = 0;


        // Broker info
        String broker = "tcp://mqtt.eclipse.org:1883";
        MemoryPersistence memoryPersistence = new MemoryPersistence();

        // Input reader
        Scanner scanner = new Scanner(System.in);

        // Client info
        System.out.println("Enter username: ");
        String clientId = scanner.nextLine();

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
            Message connectedMessage = new Message(systemTopic, connectionMessage, defaultQualityOfService, clientId);
            MessageDispatcher.sendMessage(client, connectedMessage);

            // Subscribe to topic
            client.subscribe(messageTopic, (topic, message) -> MessageDispatcher.receiveMessage(message.toString()));

            while(scanner.hasNextLine()) {
                // Read message from System.in
                String messageToBeSent = scanner.nextLine();

                // Check if user has finished chatting
                if(messageToBeSent.equals("QUIT")) {
                    // Disconnect and publish to administrator
                    Message disconnectMessage = new Message(systemTopic, disconnectionMessage, defaultQualityOfService, clientId);
                    MessageDispatcher.sendMessage(client, disconnectMessage);
                    client.disconnect();
                    System.exit(0);
                }

                // Create and publish message
                Message message = new Message(messageTopic, messageToBeSent, defaultQualityOfService, clientId);
                MessageDispatcher.sendMessage(client, message);

            }

        } catch (MqttException e) {
            System.out.println("Cause -> " + e.getCause());
            System.out.println("Reason Code -> " + e.getReasonCode());
            System.out.println("Message -> " + e.getMessage());
            e.printStackTrace();
        }

    }
}