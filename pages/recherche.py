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
    itemResp = requests.get("https://www.albion-online-data.com/api/v2/stats/Charts/{item}.json?locations={location}&time-scale=24".format(item=itemId, location=cityNames[0]))
    dataItem = itemResp.json()
    if dataItem == []:
        st.write("Pas de données pour cet item")
    else:
        prices = dataItem[0]['data']['prices_avg']
        stock = dataItem[0]['data']['item_count']
        quality = dataItem[0]['quality']
        location = dataItem[0]['location']
        dates = pd.to_datetime(dataItem[0]['data']['timestamps'])
        st.write('Stock sur 1 mois :')
        st.line_chart(pd.DataFrame({'date': dates, 'stock': stock}), x="date", y="stock")
        st.write('Prix (en pièces argent) sur 1 mois :')
        st.line_chart(pd.DataFrame({'date': dates, 'prix': prices}), x="date", y="prix")
        st.write("La qualité de l'item est : " + str(quality))
        st.write("Lieu recherché : " + location)