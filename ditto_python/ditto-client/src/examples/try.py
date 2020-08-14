import paho.mqtt.client as mqtt
import json


def client_on_connect(self, userdata, flags, rc):
	print("Connected")


def client_on_message(self, userdata, msg):
	print(msg.payload)


client = mqtt.Client("test", None, None, mqtt.MQTTv311)
client.on_connect = client_on_connect
client.on_message = client_on_message

client.connect("172.22.150.156", 1883, 60)

# client.subscribe("org.example.intern.dmp/internship/things/twin/commands/retrieve")
# msg = json.dumps({
# 	"topic": "org.example.intern.dmp/internship/things/twin/commands/retrieve",
# 	"headers": {},
# 	"path": "/"
# })
# client.publish("org.example.intern.dmp/internship/things/twin/commands/retrieve", msg, qos=1)

msg = json.dumps({
	"topic": "org.example.intern.dmp/lamp/things/twin/commands/modify",
	"headers": {},
	"path": "/features",
	"value": {
		"lightbulb_2": {
			"properties": {
				"status": 1,
				"color": "red"
			}
		}
	}
})

client.publish("e/t372ac8725cb94bd3a1fba1585bb104dc_hub/org.example.intern.dmp:lamp", msg, qos=1)

# msg2 = json.dumps({
# 	"topic": "org.example.intern.dmp/internship/things/twin/commands/modify",
# 	"headers": {},
# 	"path": "/features",
# 	"value": {
# 		"test_11_56": {
# 			"properties": {
# 				"name": "new name"
# 			}
# 		}
# 	}
# })
#
# client.publish("e/t372ac8725cb94bd3a1fba1585bb104dc_hub/org.example.intern.dmp:internship", msg2, qos=1)

# client.subscribe("edge/thing/response")
# client.publish("edge/thing/request", None)
client.loop_forever()
