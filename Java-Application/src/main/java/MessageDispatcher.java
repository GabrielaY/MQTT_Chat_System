import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;

import java.lang.reflect.Type;
import java.util.Map;

public class MessageDispatcher {

    // Send message
    public static void sendMessage(MqttClient client, Message message) {
        try {
            client.publish(message.getTopic(), message.getMessage());
        } catch (MqttException e) {
            System.out.println("Cause -> " + e.getCause());
            System.out.println("Message -> " + e.getMessage());
            System.out.println("Reason Code -> " + e.getReasonCode());
            e.printStackTrace();
        }
    }

    // Receive message
    public static void receiveMessage(String message) {
        Type typeOfHashMap = new TypeToken<Map<String, String>>(){}.getType();
        Map<String, String> messageInfo = new Gson().fromJson(message, typeOfHashMap);

        System.out.println(messageInfo.get("sender") + ": " + messageInfo.get("content") + " " + messageInfo.get("timestamp"));
    }

}
