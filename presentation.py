import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(layout='wide')
st.title('Albion Online Trading Post ⚖️')
st.write('''Un site web (encore en développement) concernant l'économie de Albion Online.
Vous trouverez trois pages :
- trading_post : permet de voir les prix et les stocks des items dans le trading post
- item_info : permet de voir les informations lié à un item
- les sources''')

for link in ["https://i.ytimg.com/vi/YM3c90leQFU/maxresdefault.jpg"]:
    imgResponse = requests.get(link)
    imgPresentation = Image.open(BytesIO(imgResponse.content))

    st.image(imgPresentation.resize((640,480)))
