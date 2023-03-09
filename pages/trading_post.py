import streamlit as st
import pandas as pd
import requests
import datetime
import plotly.graph_objs as go  

st.header("Trading Post 💰")
st.write("""Si vous trouvez qu'il y a des données étranges, c'est peut-être parce que
l'API n'est pas complètement à jour.

⚠️ Guide:
- Bien remplir les informations
- Il est possible d'intéragir avec le graphe : on peut cliquer sur les légendes pour afficher ou non les courbes
- Beaucoup d'objets n'ont pas d'informations, c'est normal. Les objets qui ont plus de chance d'avoir des informations sur les armes (dagger, sword...) """)
df= pd.read_csv("items.csv") # liste des items

# Les options
itemName = st.selectbox("Nom de l'item : ", df['nom'].values)
dateDeDeb = st.text_input("Date de début (format : AAAA-MM-JJ), mettez la date 1 mois avant aujourd'hui si vous ne savez pas quoi mettre : ")

# types de comparaison
typeComp = st.selectbox("Type de comparaison:", ["Par ville", "Par qualité"])
confirm = st.button("Rechercher")

if confirm:
    # construction de la database
    itemId = df[df['nom']==itemName]['identifiant'].values[0]

    # on récupère les données
    link = "https://www.albion-online-data.com/api/v2/stats/Charts/{item}.json?date={date}&end-date={datefin}&time-scale=24".format(item=itemId, date=dateDeDeb, datefin=datetime.datetime.today().date())
    linkReq = requests.get(link)
    dataItem = linkReq.json()

    if dataItem == []:
        st.write("Pas de données sur cet item")
    else:
        st.caption("Requête : " + link)
        database = pd.DataFrame.from_dict(dataItem)
        database['data'] = database['data'].apply(pd.DataFrame.from_dict)
        
        # traçage des figures avec plotly
        if typeComp == "Par ville":
            st.write("Cf le guide pour pouvoir intéragir avec les graphes : les courbes peuvent être affichées et cachées en cliquant sur les légendes.")
            qualityGrpBy = database.groupby('quality')
            for quality in qualityGrpBy.groups.keys():
                # info sur le prix
                fig = go.Figure() # prix moyen
                fig2 = go.Figure() # stock
                for row in qualityGrpBy.get_group(quality).itertuples():
                    fig.add_trace(go.Scatter(x=pd.to_datetime(row.data['timestamps']), y=row.data['prices_avg'], name=row.location, visible="legendonly"))
                    fig2.add_trace(go.Scatter(x=pd.to_datetime(row.data['timestamps']), y=row.data['item_count'], name=row.location, visible="legendonly"))
                fig.update_layout(title="Prix moyen de l'item " + itemName + " (qualité=%s) "%(quality) + "en fonction du temps sur 1 mois", xaxis_title="Temps", yaxis_title="Prix moyen")
                fig2.update_layout(title="Stock de l'item " + itemName + " (qualité=%s) "%(quality) + "en fonction du temps sur 1 mois", xaxis_title="Temps", yaxis_title="Stock")
                st.plotly_chart(fig)
                st.plotly_chart(fig2)
        else:
            locGrpBy = database.groupby('location')
            st.write("Cf le guide pour pouvoir intéragir avec les graphes : les courbes peuvent être affichées et cachées en cliquant sur les légendes.")
            for loc in locGrpBy.groups.keys():
                # info sur le prix
                fig = go.Figure() # prix moyen
                fig2 = go.Figure() # stock
                for row in locGrpBy.get_group(loc).itertuples():
                    fig.add_trace(go.Scatter(x=pd.to_datetime(row.data['timestamps']), y=row.data['prices_avg'], name=row.quality, visible="legendonly"))
                    fig2.add_trace(go.Scatter(x=pd.to_datetime(row.data['timestamps']), y=row.data['item_count'], name=row.quality, visible="legendonly"))
                fig.update_layout(title="Prix moyen de l'item " + itemName + " (location=%s) "%(loc) + "en fonction du temps sur 1 mois", xaxis_title="Temps", yaxis_title="Prix moyen")
                fig2.update_layout(title="Stock de l'item " + itemName + " (location=%s) "%(loc) + "en fonction du temps sur 1 mois", xaxis_title="Temps", yaxis_title="Stock")
                st.plotly_chart(fig)
                st.plotly_chart(fig2)            
        

                
        

        