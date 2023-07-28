import numpy as np
from datetime import datetime
import streamlit as st
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots
import plotly.express as px
import matplotlib.pylab as plt
from matplotlib.widgets import Slider
import time
from PIL import Image
# Set page title and header
st.set_page_config(page_title="Qualité de l'air temps réel", page_icon="♻",layout="wide")
st.write("### Qualité de l'air - données temps réel du capteur ZPHS01B")
st.sidebar.header("Configuration du graphe")
default_selection = ["PM1", "PM2.5","PM10"]  # Set the default selection
selected_graphs = st.sidebar.multiselect("Particules", ["PM1", "PM2.5","PM10"], default=default_selection)

# Define SessionState class to persist selected dates and times
class SessionState:
    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time

def update_plot(start_time, end_time):
    data = np.loadtxt("sensors_readings.txt", delimiter=";", dtype="str")
    if len(data) > 0:
        d_time = data[:, 0]
        temp = data[:, 2]
        hum = data[:, 5]
        pm1 = data[:,8]
        pm2_5 = data[:,11]
        pm10 = data[:,14]
        co2 = data[:,17]
        co = data[:,20]
        ch2o = data[:,23]
        o3 = data[:,26]
        no2 = data[:,20]
        temp = temp.astype(float)
        hum = hum.astype(float)
        pm1,pm2_5,pm10,co2,co,ch2o,o3,no2 = pm1.astype(float),pm2_5.astype(float),pm10.astype(float),co2.astype(float),co.astype(float),ch2o.astype(float),o3.astype(float),no2.astype(float)
        d_time = d_time.astype(str)
        log_time = []
        pm1_plot = []
        pm2_5_plot = []
        pm10_plot = []
        temperature_prev, humidity_prev = round(np.mean(temp[-120:-60]),1),round(np.mean(hum[-120:-60]),1)
        co2_prev,co_prev,ch2o_prev,o3_prev,no2_prev = round(np.mean(co2[-120:-60]),1),round(np.mean(co[-120:-60]),2),round(np.mean(ch2o[-120:-60]),2),round(np.mean(o3[-120:-60]),2),round(np.mean(no2[-120:-60]),2)
        temperature, humidity = round(np.mean(temp[-60:]),1),round(np.mean(hum[-60:]),1)
        co2,co,ch2o,o3,no2 = round(np.mean(co2[-60:]),1),round(np.mean(co[-60:]),2),round(np.mean(ch2o[-60:]),2),round(np.mean(o3[-60:]),2),round(np.mean(no2[-60:]),2)
        delta_val = [round(temperature-temperature_prev,2),round(humidity-humidity_prev,2),round(co2-co2_prev,2),round(co-co_prev,2),round(o3-o3_prev,2),round(no2-no2_prev,2),round(ch2o-ch2o_prev,2)]
        # delta, to get the differecne between the previous values and the current last 60 values (1 period = 1h)
        
        for i in range(len(d_time)):
            timestamp = datetime.strptime(d_time[i], "%d/%m/%Y %H:%M:%S")
            if start_time <= timestamp <= end_time:
                pm1_plot.append(pm1[i])
                pm2_5_plot.append(pm2_5[i])
                pm10_plot.append(pm10[i])
                log_time.append(timestamp)
        # Create a figure with temperature and humidity lines
    return log_time,pm1_plot,pm2_5_plot,pm10_plot,temperature,humidity,co2,co,ch2o,o3,no2,delta_val

# Load data from file
data = np.loadtxt("sensors_readings.txt", delimiter=";", dtype="str")
# Check if data is not empty
if len(data) >= 100:
    # Extract the last 100 values from the loaded file
    last_100_data = data[-100:, 0]
    default_start_time = datetime.strptime(last_100_data[0], "%d/%m/%Y %H:%M:%S")
    default_end_time = datetime.strptime(last_100_data[-1], "%d/%m/%Y %H:%M:%S")
    start_timestamp = datetime.strptime(data[0, 0], "%d/%m/%Y %H:%M:%S")
    end_timestamp = datetime.strptime(data[-1, 0], "%d/%m/%Y %H:%M:%S")
    # extract availlable date from the data
    available_dates = [datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S").date() for timestamp in data[:, 0]]
elif len(data)<100:
    default_start_time = datetime.strptime(data[0, 0], "%d/%m/%Y %H:%M:%S")
    default_end_time = datetime.strptime(data[-1, 0], "%d/%m/%Y %H:%M:%S")
    start_timestamp = datetime.strptime(data[0, 0], "%d/%m/%Y %H:%M:%S")
    end_timestamp = datetime.strptime(data[-1, 0], "%d/%m/%Y %H:%M:%S")
    available_dates = [datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S").date() for timestamp in data[:, 0]]
else:
    # Set default start and end times to current time if data is empty
    default_start_time = datetime.now()
    default_end_time = datetime.now()
    start_timestamp = datetime.now()
    end_timestamp = datetime.now()
    available_dates = [datetime.now().date()]
# Initialize SessionState object with default start and end times
session_state = SessionState(start_time=default_start_time, end_time=default_end_time)# Input fields for start date
start_date = st.sidebar.date_input("Date de début", value=session_state.start_time.date(), min_value=start_timestamp.date(), max_value=end_timestamp.date())

# Automatically select the earliest time for the selected date
if start_date in available_dates:
    start_times = [datetime.strptime(data[i, 0], "%d/%m/%Y %H:%M:%S").strftime("%H:%M") for i in range(len(data)) if datetime.strptime(data[i, 0], "%d/%m/%Y %H:%M:%S").date() == start_date]
    start_time = st.sidebar.selectbox("Heure de début", options=start_times, index=0)
    #start_time = st.sidebar.selectbox("Select the start time", options=start_times, index=start_times.index(session_state.start_time.strftime("%H:%M")))
else:
    start_time = st.sidebar.time_input("Heure de début", value=session_state.start_time.time())

start_datetime = datetime.combine(start_date, datetime.strptime(start_time, "%H:%M").time())

# Input fields for end date
end_date = st.sidebar.date_input("Date de fin", value=session_state.end_time.date(), min_value=start_date, max_value=end_timestamp.date())

# Automatically select the latest time for the selected date
if end_date in available_dates:
    end_times = [datetime.strptime(data[i, 0], "%d/%m/%Y %H:%M:%S").strftime("%H:%M") for i in range(len(data)) if datetime.strptime(data[i, 0], "%d/%m/%Y %H:%M:%S").date() == end_date]
    end_time = st.sidebar.selectbox("Heure de fin", options=end_times, index=len(end_times) - 1)
else:
    end_time = st.sidebar.time_input("Heure de fin", value=session_state.end_time.time())

end_datetime = datetime.combine(end_date, datetime.strptime(end_time, "%H:%M").time())
# Call the update_plot function with selected timestamps
log_time,pm1_plot,pm2_5_plot,pm10_plot,temperature,humidity,co2,co,ch2o,o3,no2,delta_val=update_plot(start_datetime, end_datetime)

fig = make_subplots(rows=1, cols=1,specs=[[{"secondary_y": False}]])
fig.update_layout(title=default_selection[0], showlegend=True,plot_bgcolor='#dbdbdb')
fig.update_layout(height=500,width=1000)
# fig.add_trace(go.Scatter(x=log_time,y=temperature,name="Temperature °C",yaxis="y1",line_color='purple'))
# fig.add_trace(go.Scatter(x=log_time,y=humidity,name="Humidity %",yaxis="y2",line_color='green'))
# fig.update_yaxes(title_text="Temperature °C", secondary_y=False)
# fig.update_yaxes(title_text="Humidity %", secondary_y=True)
#fig.update_xaxes(rangeslider_visible=True, rangeslider_thickness=0.05, rangeslider_bgcolor='white')

# Perform actions based on the selected menu items
graph_title = ""
for graph_type in selected_graphs:
    graph_title+=graph_type+" "
    if graph_type == "PM1":
        # Plot the temperature graph
        fig.add_trace(go.Scatter(x=log_time, y=pm1_plot, name="PM1 µg/m3", yaxis="y1", line_color='purple'))
        fig.update_yaxes(title_text="PM1 µg/m3", secondary_y=False)
        fig.update_layout(title=graph_title, showlegend=True,plot_bgcolor='#dbdbdb')
        fig.update_layout(title_x=0.35)  # Center align the graph title
    elif graph_type == "PM2.5":
        # Plot the humidity graph
        fig.add_trace(go.Scatter(x=log_time, y=pm2_5_plot, name="PM2.5 µg/m3", yaxis="y1", line_color='green'))
        fig.update_yaxes(title_text="PM2.5 µg/m3", secondary_y=False)
        fig.update_layout(title=graph_title, showlegend=True,plot_bgcolor='#dbdbdb')
        fig.update_layout(title_x=0.35)  # Center align the graph title
    elif graph_type == "PM10":
        # Plot the humidity graph
        fig.add_trace(go.Scatter(x=log_time, y=pm10_plot, name="PM10 µg/m3", yaxis="y1", line_color='blue'))
        fig.update_yaxes(title_text="PM10 µg/m3", secondary_y=False)
        fig.update_layout(title=graph_title, showlegend=True,plot_bgcolor='#dbdbdb')
        fig.update_layout(title_x=0.35)  # Center align the graph title

temperature,humidity,co2,co= str(temperature)+" °C", str(humidity)+" %", str(co2)+" ppm", str(co)+ " ppm"
ch2o,o3,no2  = str(ch2o)+" mg/m3",str(o3)+" ppm", str(no2)+" ppm"
placeholder1 = st.empty()# empty element to display the graph
with placeholder1:
    col1, col2, col3, col4, col5, col6=st.columns(6)
    ct1, ct2, ct3, ct4, ct5, ct6 = col1.empty(), col2.empty(), col3.empty(), col4.empty(), col5.empty(), col6.empty()
    ct1.metric("Température", temperature,delta=delta_val[0])
    ct2.metric("Humidité",humidity,delta=delta_val[1])
    ct3.metric("CO2",co2,delta=delta_val[2])
    ct4.metric("CO",co,delta=delta_val[3])
    ct5.metric("O3",o3,delta=delta_val[4])
    ct6.metric("NO2",no2,delta=delta_val[5])
#col7.metric("CH2O",ch2o)
# Display the plot
st.plotly_chart(fig)
f = open("main.css")
st.markdown(f"""<style>{f.read()}</style>""",unsafe_allow_html=True)
f.close()

st.markdown("""
<p>Les données ci-dessus sont mesuré en temps réel avec le capteur ZPHS01B développé sur ESP32. 
Le capteur transmet les données vers un serveur MQTT, ces données sont récupérées sur un serveur distant sur lequel est hébergé notre page. 
    </p>
<p>ZPHS01B est un module de qualité de l'air multi-en-un, intégrant un capteur de poussière laser, un capteur de dioxyde de carbone infrarouge, 
un capteur de formaldéhyde électrochimique, un capteur d'ozone électrochimique, un capteur de monoxyde de carbone électrochimique, un capteur 
de COV, un capteur de NO2 et un capteur de température et d'humidité. Il peut mesurer avec précision la concentration de divers gaz dans l'air, avec une interface de communication UART (niveau TTL). Le module intègre aussi un capteur de température et d’humilité. 
</p>
""",unsafe_allow_html=True)
image = Image.open('capteur.jpg')
st.image(image, caption="Capteur de surveillance de la qualité de l'air")

delta_val_old = delta_val
while True:
    time.sleep(60)
    log_time,pm1_plot,pm2_5_plot,pm10_plot,temperature,humidity,co2,co,ch2o,o3,no2,delta_val=update_plot(start_datetime, end_datetime)
    temperature,humidity,co2,co= str(temperature)+" °C", str(humidity)+" %", str(co2)+" ppm", str(co)+ " ppm"
    ch2o,o3,no2  = str(ch2o)+" mg/m3",str(o3)+" ppm", str(no2)+" ppm"
    with placeholder1:
        if(delta_val[0] != delta_val_old[0]):
            # print(((datetime.now()-start).total_seconds()))
            # print(delta_val[0])
            ct1.empty()
            ct1.metric("Température", temperature,delta=delta_val[0])
            delta_val_old = delta_val
        if(delta_val[1] != delta_val_old[1]):
            # print(((datetime.now()-start).total_seconds()))
            # print(delta_val[1])
            ct2.empty()                
            ct2.metric("Humidité",humidity,delta=delta_val[1])
            delta_val_old = delta_val    
        if(delta_val[2] != delta_val_old[2]):
            # print(((datetime.now()-start).total_seconds()))
            # print(delta_val[2])
            ct3.empty()                
            ct3.metric("CO2",co2,delta=delta_val[2])
            delta_val_old = delta_val                    
        if(delta_val[3] != delta_val_old[3]):
            # print(((datetime.now()-start).total_seconds()))
            # print(delta_val[3])
            ct4.empty()                     
            ct4.metric("CO",co,delta=delta_val[3])
            delta_val_old = delta_val    
        if(delta_val[4] != delta_val_old[4]):
            # print(((datetime.now()-start).total_seconds()))
            # print(delta_val[4])
            ct5.empty()                   
            ct5.metric("O3",o3,delta=delta_val[4])
            delta_val_old = delta_val
        if(delta_val[5] != delta_val_old[5]):
            # print(((datetime.now()-start).total_seconds()))
            # print(delta_val[5])
            ct6.empty()                   
            ct6.metric("NO2",no2,delta=delta_val[5])          
            delta_val_old = delta_val
# st.markdown(
#     """
#     <style>
#     .footer {
#         font-size: 14px;
#         color: gray;
#         text-align: center;
#         padding: 20px;
#     }
#     </style>
#     """
#     "<div class='footer'>© Rais Beaurel 2023</div>",
#     unsafe_allow_html=True,
# )

# Start the MQTT client loop
