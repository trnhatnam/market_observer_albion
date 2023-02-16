import streamlit as st
import pandas as pd
import requests

df= pd.read_csv("items.csv") # liste des items
itemName = st.selectbox("Tapez le nom de l'item : ", df['nom'].values)
cityNames = ["Thetford", "Fort_Sterling", "Carleon", "Lymhurst", "Martlock", "Bridgewatch", "Black Market"]
st.write('Choisis une ville : ')
for city in cityNames:
    st.checkbox(city, key=city)

confirm = st.button("Valider")

if confirm:
    itemId = df[df['nom'].str.contains(itemName)]['identifiant'].values[0]
    