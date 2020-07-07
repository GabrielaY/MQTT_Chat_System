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
    public static void receiveMessage(String msg_topic, String payload_message, MqttClient client, Object syncObject) throws MqttException {
        Type typeOfHashMap = new TypeToken<Map<String, String>>(){}.getType();
        Map<String, String> messageInfo = new Gson().fromJson(payload_message, typeOfHashMap);
        if(msg_topic.equals("/chat/" + client.getClientId() + "/response")){
            if(messageInfo.get("content").equals("yes")){
                System.out.println("Joined group chat");
                client.subscribe("/chat/messages", (topic, message) -> MessageDispatcher.receiveMessage(topic, message.toString(),client, syncObject));
                synchronized(syncObject) {
                    syncObject.notify();
                }
            }
            else {
                System.out.println("Access denied!");
                Message disconnectMessage = new Message("/chat/system", "disconnected", 0, client.getClientId());
                MessageDispatcher.sendMessage(client, disconnectMessage);
                client.disconnect();
                System.exit(-1);
            }
        }
        else{
            System.out.println(messageInfo.get("sender") + ": " + messageInfo.get("content") + " " + messageInfo.get("timestamp"));
        }
    }

}
