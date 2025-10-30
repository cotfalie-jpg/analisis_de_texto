import streamlit as st
import pandas as pd
from textblob import TextBlob
import re

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="BAE Análisis de Texto 💛",
    page_icon="💛",
    layout="wide"
)

# --- ESTILOS PERSONALIZADOS (BAE) ---
st.markdown("""
    <style>
    body {
        background-color: #fff8e7;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #fff8e7;
    }
    [data-testid="stSidebar"] {
        background-color: #fdf3c2;
    }
    h1, h2, h3 {
        color: #d1a300;
    }
    .stButton>button {
        background-color: #f9e79f;
        color: #5a4300;
        border-radius: 10px;
        border: 1px solid #f0d77b;
    }
    .stButton>button:hover {
        background-color: #ffecb3;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGO Y TÍTULO ---
st.image("logo_bae.png", width=150)
st.title("💛 Analizador de Texto BAE")
st.write("Descubre el **sentimiento, subjetividad y palabras clave** de cualquier texto.")

# --- OPCIÓN DE ENTRADA ---
st.sidebar.header("Opciones")
modo = st.sidebar.selectbox("Selecciona el modo:", ["Texto directo", "Archivo de texto"])

# --- FUNCIÓN PARA CONTAR PALABRAS ---
def contar_palabras(texto):
    stop_words = set([
        "a","al","algo","como","con","de","del","en","el","ella","ellos","eso","esta",
        "ha","han","he","la","las","le","lo","los","me","mi","muy","no","nos","o","por",
        "que","se","si","sin","son","su","sus","te","tu","un","una","uno","y","ya","yo"
    ])
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for p in palabras_filtradas:
        contador[p] = contador.get(p, 0) + 1
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    return contador_ordenado

# --- FUNCIÓN PRINCIPAL DE ANÁLISIS ---
def procesar_texto(texto):
    blob = TextBlob(texto)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    contador_palabras = contar_palabras(texto)
    frases = [f.strip() for f in re.split(r'[.!?]+', texto) if f.strip()]
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "contador_palabras": contador_palabras,
        "frases": frases
    }

# --- VISUALIZACIÓN ---
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌈 Sentimiento general")
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.progress(sentimiento_norm)
        if resultados["sentimiento"] > 0.05:
            st.success(f"Positivo 😊 ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"Negativo 😟 ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"Neutral 😐 ({resultados['sentimiento']:.2f})")

        st.subheader("💭 Subjetividad")
        st.progress(resultados["subjetividad"])
        if resultados["subjetividad"] > 0.5:
            st.warning(f"Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"Baja subjetividad ({resultados['subjetividad']:.2f})")

    with col2:
        st.subheader("🔤 Palabras más usadas")
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            st.bar_chart(palabras_top)

    st.subheader("📚 Frases analizadas")
    for i, frase in enumerate(resultados["frases"][:10], 1):
        blob_frase = TextBlob(frase)
        sent = blob_frase.sentiment.polarity
        emoji = "😊" if sent > 0.05 else ("😟" if sent < -0.05 else "😐")
        st.write(f"{i}. {emoji} *{frase}* ({sent:.2f})")

# --- MODO DE ENTRADA ---
if modo == "Texto directo":
    st.subheader("✍️ Escribe tu texto")
    texto = st.text_area("", height=200, placeholder="Escribe o pega aquí tu texto...")
    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando con amor... 💛"):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("Por favor ingresa algún texto.")

elif modo == "Archivo de texto":
    st.subheader("📂 Sube un archivo (.txt, .md o .csv)")
    archivo = st.file_uploader("", type=["txt", "md", "csv"])
    if archivo is not None:
        contenido = archivo.getvalue().decode("utf-8")
        with st.expander("Ver contenido del archivo"):
            st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
        if st.button("Analizar archivo"):
            with st.spinner("Analizando con amor... 💛"):
                resultados = procesar_texto(contenido)
                crear_visualizaciones(resultados)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown("✨ Desarrollado con 💛 por BAE — Analiza, comprende y siente tus palabras.")

