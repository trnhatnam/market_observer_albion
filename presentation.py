import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(layout='wide')
st.title('Albion Online Trading Post')
st.write('''Un site web pour regarde ce qu\'il y a dans le marché de Albion Online.
\n Voici quelques photos du jeu :''')

for link in ["https://i.ytimg.com/vi/YM3c90leQFU/maxresdefault.jpg", "https://doc.ubuntu-fr.org/lib/exe/fetch.php?tok=13bc7c&media=https%3A%2F%2Fi.imgur.com%2FetB6qdZ.jpg"]:
    imgResponse = requests.get(link)
    imgPresentation = Image.open(BytesIO(imgResponse.content))

    st.image(imgPresentation.resize((640,480)))
