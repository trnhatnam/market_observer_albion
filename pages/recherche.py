import streamlit as st
import pandas as pd
import requests

df= pd.read_csv("items.csv")
df= df.set_index('nom')
# try :
# 	print(df.loc[['Carrot Seeds']]["identifiant"][0])
# except KeyError:
# 	print('Non trouvé')
st.set_page_config(layout='wide')
text = st.text_input("Item")
confirm = st.button('Confirm')
items = df[df.index.str.contains(text, case=False)]
st.table(df[df.index.str.contains(text, case=False)])

if confirm:
    item_id = items["identifiant"][0]
    response = requests.get("https://www.albion-online-data.com/api/v2/stats/prices/" + item_id + ".json?locations=Caerleon,Bridgewatch")
    df_item = pd.json_normalize(response.json())
    st.write('Current buying price is '  + str(df_item[df_item['city'] == "Bridgewatch"]['buy_price_min'].values[0]) + " silvers")