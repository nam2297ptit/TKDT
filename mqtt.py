import paho.mqtt.client as mqtt
import os
import config
def on_connect(client, userdata, flags, rc):
    client.subscribe("#")


def on_message(client, userdata, msg):
	print(msg.topic,msg.payload.decode("utf-8") )
	if msg.topic == "home/detect":
		if msg.payload.decode("utf-8") == "detect":
			os.system("python3 detector.py")
		elif msg.payload.decode("utf-8") == "emotion":
			os.system("python3 emotion.py")
	if msg.topic == "home/result":
		if msg.payload.decode("utf-8") == "unknown":
			os.system("python3 gad.py")



client = mqtt.Client()
client.username_pw_set(username = config.username , password=config.password)
client.on_connect = on_connect
client.on_message = on_message

client.connect(config.server, config.port, 60)

try:
	client.loop_forever()
	
except KeyboardInterrupt:
	client.loop_stop()
	print ("Close Progarm")

