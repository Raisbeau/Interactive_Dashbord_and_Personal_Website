import paho.mqtt.client as mqtt #pip install paho-mqtt

# MQTT broker settings
mqtt_broker = "mqtt.rais-beaurel.com"
mqtt_port = 1883  # MQTT default port 1883
mqtt_topic = "airquality"
# Callback function for MQTT client connection
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, message):
    f = open("sensors_readings.txt","a")
    f.write(str(message.payload.decode("utf-8"))+"\n")
    f.close()
    #print(str(message.payload.decode("utf-8"))+"\n")
# Create MQTT client instance
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect(mqtt_broker, mqtt_port)
client.loop_forever()

