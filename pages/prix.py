import streamlit as st
import pandas as pd
import requests
import datetime

st.header("Info sur un item dans le marché")
st.write("""Il se peut que l\'item cherché ne soit pas vendu dans certaines villes, que 
la requête ne trouve pas l'item attendu ou bien qu'elle fonctionne mal.""")
df= pd.read_csv("items.csv") # liste des items

# Les options
itemName = st.selectbox("Tapez le nom de l'item : ", df['nom'].values)

cityNames = ["Thetford", "Fort Sterling", "Carleon", "Lymhurst", "Martlock", "Bridgewatch", "Black Market"]
st.write('Choisis une ville : ')
for city in cityNames:
    st.checkbox(city, key=city)

qualityIn = st.text_input("Entrez la qualité de l'item (min 0, max 4, normal 1) : ")
dateDeDeb = st.text_input("Entrez la date de début (format : AAAA-MM-JJ) : ")


confirm = st.button("Valider")

if confirm:
    itemId = df[df['nom']==itemName]['identifiant'].values[0]

    # On va mettre tous les villes cochés dans le lien
    cityNamesTicked = ",".join([city for city in cityNames if st.session_state[city]])

    link = "https://www.albion-online-data.com/api/v2/stats/Charts/{item}.json?locations={loc}&date={date}&end-date={datefin}&qualities={qua}&time-scale=24".format(item=itemId, qua=qualityIn, loc=cityNamesTicked, date=dateDeDeb, datefin=datetime.datetime.today().date())
    itemResp = requests.get(link)
    dataItem = itemResp.json()

    st.caption("Requête : " + link)
    if dataItem == []:
        st.write("Pas de données pour cet item")
    
    else: # on a des données sur l'item
        #pprint.pprint(dataItem)

        for elem in dataItem:
            # on prend les données
            prices = elem['data']['prices_avg']
            stock =elem['data']['item_count']
            quality = elem['quality']
            location = elem['location']
            dates = pd.to_datetime(elem['data']['timestamps'])

            st.subheader("Prix/stock de " + itemName + " de qualité " + str(quality) + " à " + location)

            # on les affiche bien
            st.write('Prix (en pièces argent) :')
            st.line_chart(pd.DataFrame({'date': dates, 'prix': prices}), x="date", y="prix")
            st.write('Stock :')
            st.line_chart(pd.DataFrame({'date': dates, 'stock': stock}), x="date", y="stock")