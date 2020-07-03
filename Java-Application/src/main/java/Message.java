import com.google.gson.Gson;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class Message {

    private String topic;

    private MqttMessage message = new MqttMessage();

    public Message(String topic, String content, int qos, String clientId) {
        this.topic = topic;
        message.setQos(qos);
        message.setPayload(generateMessagePayload(content, clientId, generateTimeStamp()));
    }

    // Generate timestamp from current time
    private String generateTimeStamp() {
        DateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");
        Date date = new Date();
        return dateFormat.format(date);
    }

    // Create content for the message to be sent
    private byte[] generateMessagePayload(String content, String sender, String timestamp) {

        Map<String, String> messageInfo = new HashMap<>();

        messageInfo.put("content", content);
        messageInfo.put("sender", sender);
        messageInfo.put("timestamp", timestamp);

        Gson gson = new Gson();

        return gson.toJson(messageInfo).getBytes();
    }

    // Send message
    public void sendMessage(MqttClient client) {
        try {
            client.publish(topic, message);
        } catch (MqttException e) {
            System.out.println("Cause -> " + e.getCause());
            System.out.println("Message -> " + e.getMessage());
            System.out.println("Reason Code -> " + e.getReasonCode());
            e.printStackTrace();
        }
    }

}
