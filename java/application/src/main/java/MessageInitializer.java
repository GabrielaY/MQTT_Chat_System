import chat_message.MessagePrototype;

import org.eclipse.paho.client.mqttv3.MqttMessage;

import com.google.protobuf.util.JsonFormat;
import com.google.protobuf.InvalidProtocolBufferException;

import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;

public class MessageInitializer {

    // Generate timestamp from current time
    public static String generateTimeStamp() {
        DateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");
        Date date = new Date();
        return dateFormat.format(date);
    }

    // Create content for the message to be sent
    public static MqttMessage generateMqttMessage(MessagePrototype.ChatMessage chatMessage) throws InvalidProtocolBufferException {
        byte [] payload = JsonFormat.printer().print(chatMessage).getBytes();
        return new MqttMessage(payload);
    }

}
