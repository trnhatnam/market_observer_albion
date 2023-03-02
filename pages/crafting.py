import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import requests

st.header("Infos lié à un item")
st.write("""On ne cherche pas à regarder le prix de l'item ici. On regarde seulement les
informations lié à l'item.""")
df= pd.read_csv("items.csv") # liste des items

itemName = st.selectbox("Tapez le nom de l'item : ", df['nom'].values)
confirm = st.button('Valider')

if confirm:
    infoLink = "https://gameinfo.albiononline.com/api/gameinfo/items/{item}/data".format(item=itemName)
    iconLink = "https://render.albiononline.com/v1/item/{identifier}.png".format(identifier=itemName)

    iconReq = requests.get(iconLink)
    icon = Image.open(BytesIO(iconReq.content))

    st.image(icon.resize((64,64)))
