import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

import java.lang.reflect.Type;
import java.util.Map;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

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
            Message connectedMessage = new Message("/chat/system", "connected", 0, clientId);
            connectedMessage.sendMessage(client);

            // Subscribe to topic
            client.subscribe("/chat/messages", (topic, message) -> receiveMessage(message.toString()));

            while(scanner.hasNextLine()) {
                // Read message from System.in
                String messageToBeSent = scanner.nextLine();

                // Check if user has finished chatting
                if(messageToBeSent.equals("QUIT")) {
                    // Disconnect and publish to administrator
                    Message disconnectMessage = new Message("/chat/system", "disconnected", 0, clientId);
                    disconnectMessage.sendMessage(client);
                    client.disconnect();
                    System.exit(0);
                }

                // Create and publish message
                Message message = new Message("/chat/messages", messageToBeSent, 0, clientId);
                message.sendMessage(client);

            }

        } catch (MqttException e) {
            System.out.println("Cause -> " + e.getCause());
            System.out.println("Reason Code -> " + e.getReasonCode());
            System.out.println("Message -> " + e.getMessage());
            e.printStackTrace();
        }

    }

    // Receive message callback function
    private static void receiveMessage(String message) {
        Type typeOfHashMap = new TypeToken<Map<String, String>>(){}.getType();
        Map<String, String> messageInfo = new Gson().fromJson(message, typeOfHashMap);

        System.out.println(messageInfo.get("sender") + ": " + messageInfo.get("content") + " " + messageInfo.get("timestamp"));
    }

}