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
lang = st.selectbox("Langue : ", ['FR-FR', 'EN-US'])
confirm = st.button('Valider')

if confirm:
    itemId = df[df['nom']==itemName]['identifiant'].values[0]
    infoLink = "https://gameinfo.albiononline.com/api/gameinfo/items/{item}/data".format(item=itemId)
    iconLink = "https://render.albiononline.com/v1/item/{identifier}.png".format(identifier=itemName)

    infoReq = requests.get(infoLink)

    infoReq.raise_for_status()

    iconReq = requests.get(iconLink)
    icon = Image.open(BytesIO(iconReq.content))

    info = infoReq.json()

    cols = st.columns(2)
    # Nom de l'item
    cols[0].write('Nom :')
    cols[1].write(info['localizedNames'][lang])

    cols = st.columns(2)
    # Description de l'item
    cols[0].write('Description :')
    cols[1].write(info['localizedDescriptions'][lang])

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
    cols = st.columns(2)
    cols[0].write('Crafting list :')
    if enchInfo != None:

        # création d'un expandeur
        with st.expander("Expand"):
            craftingInfo = enchInfo['enchantments']
            for section in craftingInfo:
                st.subheader('Niveau d\'enchantement : ' + str(section['enchantmentLevel']))
                craftReq = section['craftingRequirements']
                st.write('Crafting Focus : ' + str(craftReq['craftingFocus']))
                for ingredient in craftReq['craftResourceList']:
                    cols = st.columns(4)
                    subItemId = ingredient['uniqueName']
                    cols[0].write(df[df['identifiant'] == subItemId]['nom'].values[0])

                    # icone du sous-item
                    ingLink = "https://render.albiononline.com/v1/item/{identifier}.png".format(identifier=subItemId)
                    ingReq = requests.get(ingLink)
                    ingIcon = Image.open(BytesIO(ingReq.content))
                    cols[1].image(ingIcon.resize((64,64)))

                    cols[2].write('x' + str(ingredient['count']))

    else:
        cols[1].write('Non craftable')