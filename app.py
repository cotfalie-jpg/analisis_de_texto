import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator
from PIL import Image

# ======================================================
# CONFIGURACIÓN GENERAL Y ESTILO VISUAL "BAE"
# ======================================================

st.set_page_config(
    page_title="BAE | Analizador Emocional de Texto",
    page_icon="👶",
    layout="wide"
)

# COLORES DE IDENTIDAD
COLOR_PRIMARIO = "#DD8E6B"  # melocotón cálido
COLOR_SECUNDARIO = "#FFF8EA"  # crema suave
COLOR_ACENTO = "#FFF2C3"  # amarillo pastel
COLOR_AGUA = "#C6E2E3"  # celeste bebé

# CSS personalizado
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {COLOR_SECUNDARIO};
            color: #3C3C3C;
            font-family: 'Poppins', sans-serif;
        }}
        h1, h2, h3, h4 {{
            color: {COLOR_PRIMARIO};
            font-weight: 700;
        }}
        .stButton > button {{
            background-color: {COLOR_AGUA};
            color: #3C3C3C;
            border: none;
            border-radius: 12px;
            padding: 0.6em 1.2em;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            background-color: {COLOR_PRIMARIO};
            color: white;
            transform: scale(1.03);
        }}
        section[data-testid="stSidebar"] {{
            background-color: {COLOR_ACENTO};
            border-right: 2px solid #DD8E6B20;
        }}
        .stProgress > div > div {{
            background-color: {COLOR_PRIMARIO} !important;
        }}
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 2rem;
        }}
    </style>
""", unsafe_allow_html=True)

# ======================================================
# ENCABEZADO
# ======================================================

try:
    logo = Image.open("logo_bae.png")
    st.image(logo, width=130)
except:
    st.write("👶 **BAE - Baby App Especializada**")

st.title("💬 Analizador Emocional de Texto | BAE")
st.write("""
Esta aplicación analiza el **tono emocional y subjetivo** del texto que escribes.  
BAE ayuda a entender cómo te sientes a través de tus palabras.
""")

# ======================================================
# BARRA LATERAL
# ======================================================
st.sidebar.image("logo_bae.png", width=100)
st.sidebar.markdown("## 🌸 Opciones de análisis")
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)
st.sidebar.markdown("---")
st.sidebar.write("""
BAE combina inteligencia emocional y análisis de texto para ayudar a los padres 
a comprender mejor su estado emocional mientras cuidan a sus bebés.
""")

# ========================================

