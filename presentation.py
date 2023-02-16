import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(layout='wide')
st.title('Albion Online Trading Post')
st.write('Un site web pour regarde ce qu\'il y a dans le marché de Albion Online')

imgResponse = requests.get("https://i.ytimg.com/vi/YM3c90leQFU/maxresdefault.jpg")
imgPresentation = Image.open(BytesIO(imgResponse.content))

st.image(imgPresentation, caption="Albion Online")

