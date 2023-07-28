import streamlit as st
#import paho.mqtt.client as mqtt

st.set_page_config(page_title="Broker MQTT", page_icon="➗", layout="wide")
# MQTT_BROKER = "mqtt.rais-beaurel.com"
# MQTT_PORT = 1883

# # Create an MQTT client instance
# mqtt_client = mqtt.Client()

# # Callback function when connected to the MQTT broker
# def on_connect(client, userdata, flags, rc):
#     print(mqtt_client.is_connected())
# # Callback function when a message is published to a subscribed topic
# def on_message(client, userdata, msg):
#     #st.write(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")
#     f = open("message_rec.txt","w")
#     f.write(str(msg.payload.decode("utf-8"))+"\n")
#     f.close()
#     print(str(message.payload)+"\n")
    
# # Connect to the MQTT broker
# mqtt_client.on_connect = on_connect
# mqtt_client.connect(MQTT_BROKER, MQTT_PORT)


st.markdown("""
# Serveur et Client MQTT
##### Cette page fourni les information pour se connecter au serveur MQTT mqtt.rais-beaurel.com
##### Pour des exemples de code pour Arduino, ESP32 et Python, veuillez consuler ma page [GitHub](https://github.com/Raisbeau).
""")
st.markdown("""
    <div style="border: 2px solid black; border-radius: 10px; padding: 10px;">
        <h2>Informations de connection au serveur MQTT</h2>
        <ul>
            <li>Adresse du serveur : <b>mqtt.rais-beaurel.com</b></li>
            <li>Port de connection (TCP): <b>1883</b></li>
        </ul>
    </div>
""", unsafe_allow_html=True)
st.write("\n")
st.markdown("""Un serveur MQTT (Message Queuing Telemetry Transport) joue un rôle essentiel dans l'IoT en 
            facilitant une communication M2M (Machine-to-Machine) efficace, à faible bande passante 
            et latence. Grâce à son modèle Publish/Subscribe (Pub/Sub), il permet une distribution 
            d'informations à plusieurs destinataires sans connaissance préalable de leur présence, 
            assurant ainsi une architecture flexible et évolutive. Il s'agit d'une solution idéale pour ceux qui veulent transferer 
            les données de capteurs d'une région distante vers un point.""")

# col1, col2 = st.columns(2)

# with col2 :
#     st.write("#### Souscrire à un sujet")
#     topic = st.text_input("topic", "sujet",label_visibility="hidden")
#     if st.button("Souscrire"):
#         mqtt_client.subscribe(topic)
#         st.success(f"Vous avez souscrit au sujet : {topic}")
#     f = open("message_rec.txt")
#     message = st.chat_message("user",avatar="🧑‍💻")
#     message.write("Vos messages apparaissent ici")
#     message.write(f.read())
#     f.close()
# with col1:
#     st.write("#### Publier dans un sujet")
#     topic = st.text_input("Entrez le sujet",value="Sujet",label_visibility="hidden")
#     message = st.text_area("message",value="Saisissez votre message ici",label_visibility="hidden")
#     if st.button("Publier"):
#         mqtt_client.publish(topic, message)
#         st.success(f"Message publié dans : {topic}")

# mqtt_client.on_message = on_message
# mqtt_client.loop_start()



f = open("main.css")
st.markdown(f"""<style>{f.read()}</style>""",unsafe_allow_html=True)
f.close()