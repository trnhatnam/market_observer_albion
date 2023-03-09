import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import requests

st.header("Informations sur un item 📖")
st.write("""On ne cherche pas à regarder le prix de l'item ici. On regarde seulement les
informations lié à l'item.""")
df= pd.read_csv("items.csv") # liste des items

itemName = st.selectbox("Tapez le nom de l'item : ", df['nom'].values)
infoLang = st.selectbox("Langue : ", ['FR-FR', 'EN-US'])
confirm = st.button('Valider')



if confirm:
    itemId = df[df['nom']==itemName]['identifiant'].values[0]
    infoLink = "https://gameinfo.albiononline.com/api/gameinfo/items/{item}/data".format(item=itemId)
    iconLink = "https://render.albiononline.com/v1/item/{identifier}.png".format(identifier=itemName)

    iconReq = requests.get(iconLink)
    icon = Image.open(BytesIO(iconReq.content))

    infoReq = requests.get(infoLink)
    info = infoReq.json()

    cols = st.columns(2)
    # Nom de l'item
    cols[0].write('Nom :')
    cols[1].write(info['localizedNames'][infoLang])

    cols = st.columns(2)
    # Description de l'item
    cols[0].write('Description :')
    cols[1].write(info['localizedDescriptions'][infoLang])

    cols = st.columns(2)
    # Affichage de l'icone
    cols[0].write('Icone :')
    cols[1].image(icon.resize((64,64)))

    cols = st.columns(2)
    # Type de l'item
    cols[0].write('Item type :')
    cols[1].write(info['itemType'])

    cols = st.columns(2)
    # Disponible sur le marché ?
    cols[0].write('Disponible sur le marché :')
    cols[1].write(info['showinmarketplace'])

    # Crafting list
    enchInfo = info['enchantments']
    st.write('Crafting list :')
    if enchInfo != None:
        with st.expander("Expand"):
            st.write('Crafting list :')
            craftingInfo = enchInfo['enchantments']
            for level in craftingInfo:
                st.subheader('Enchantement level : ' + str(level['enchantmentLevel']))
                st.write('Item power: ' + str(level['itemPower']))
                st.write(level['craftingRequirements'])
        


