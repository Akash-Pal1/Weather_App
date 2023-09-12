import folium
import streamlit as st
from streamlit_folium import st_folium
import requests, json

api_key = st.secrets['api_key']

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

st.title("Weather App")


city_name = st.text_input('Enter the city name','Delhi, IN')

base_url = "http://api.openweathermap.org/data/2.5/weather?"
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
response = requests.get(complete_url)
x = response.json()

if x['cod'] == '404':
    st.warning("No such city found")
else:
    longitude = x['coord']['lon']
    latitude = x['coord']['lat']
    weather_main = x['weather'][0]['main']
    weather_desc = x['weather'][0]['description']
    weather_icon = x['weather'][0]['icon']
    base_icon_image_url = 'https://openweathermap.org/img/wn/'+weather_icon+'@2x.png'
    curr_temp = round(x['main']['temp']-273.15,1)
    temp_min = round(x['main']['temp_min']-273.15,1)
    temp_max = round(x['main']['temp_max']-273.15,1)
    pressure = x['main']['pressure']
    humidity = x['main']['humidity']
    visibility = x['visibility']
    wind_speed = x['wind']['speed']
    wind_degree = x['wind']['deg']
    country = x['sys']['country']
    city = x['name']
    
    location_city = [latitude,longitude]
    
    # Menu Section starting 
    
    desc_show, map_show = st.columns(2)
    
    with desc_show:
        icon_show ,desc_show_main = st.columns([1,1])
        with icon_show:
            st.image(base_icon_image_url,caption=weather_main)
    
        with desc_show_main:
            st.title(weather_main.capitalize())
    
        st.markdown(f"<h4 class='desc_of_weather' style='text-align: center; color: black;'> {weather_desc.capitalize()} </h4>", unsafe_allow_html=True)
    
    
    with map_show:
        m = folium.Map(location=location_city)
        folium.Marker(
            location_city, popup=city, tooltip=city
        ).add_to(m)
        st_data = st_folium(m,height=190,width=355)
    
    temp_c_show, temp_max_show, temp_min_show = st.columns(3)
    
    with temp_c_show:
        st.metric("Current Temperature",f"{curr_temp} °C")
        st.metric("Humidity",f"{humidity} %")
    with temp_max_show:
        st.metric("Maximum Temperature",f"{temp_max} °C")
        st.metric("Pressure",f"{pressure} hPa")
    with temp_min_show:
        st.metric("Minimum Temperature",f"{temp_min} °C")
        st.metric("Wind Speed",f"{wind_speed} m/s")

    
    

# Icon Display
# st.image(base_icon_image_url,caption=weather_main,width = 10)

# Map 
# m = folium.Map(location=location_city)
# folium.Marker(
#     location_city, popup=city, tooltip=city
# ).add_to(m)
# st_data = st_folium(m, width=100,height=100)

