# =====================================================
# 🌸 ANALIZADOR DE TEXTO BAE
# =====================================================
import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from deep_translator import GoogleTranslator
from PIL import Image

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================
st.set_page_config(page_title="BAE | Analizador de Texto", page_icon="🍼", layout="wide")

# Paleta de colores BAE
COLOR_PRIMARIO = "#DD8E6B"
COLOR_FONDO = "#FFF8EA"
COLOR_ACENTO = "#FFF2C3"
COLOR_SUAVE = "#C6E2E3"
COLOR_TEXTO = "#3C3C3C"

# =====================================================
# ESTILO VISUAL PERSONALIZADO
# =====================================================
st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLOR_FONDO};
        color: {COLOR_TEXTO};
        font-family: 'Poppins', sans-serif;
    }}
    h1, h2, h3 {{
        color: {COLOR_PRIMARIO};
        font-weight: 700;
    }}
    .stButton > button {{
        background-color: {COLOR_SUAVE};
        color: {COLOR_TEXTO};
        border-radius: 10px;
        border: none;
        font-weight: 600;
        padding: 0.5em 1em;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_PRIMARIO};
        color: white;
        transform: scale(1.02);
    }}
    section[data-testid="stSidebar"] {{
        background-color: {COLOR_ACENTO};
        border-right: 2px solid #DD8E6B20;
    }}
    [data-testid="stExpander"] {{
        border-radius: 12px;
        background-color: #FFFFFFCC;
    }}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CABECERA
# =====================================================
col_logo, col_titulo = st.columns([1, 4])
with col_logo:
    try:
        st.image("logo_bae.png", width=120)
    except:
        st.write("🍼")
with col_titulo:
    st.title("Analizador de Texto BAE")
    st.write("Descubre el **sentimiento y la intención** detrás de cada palabra con nuestra IA emocional 🌸")

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.image("logo_bae.png", width=100)
    st.markdown("### 💡 ¿Qué hace esta app?")
    st.write("""
    Esta herramienta analiza el tono emocional y la claridad de los textos, detectando si son positivos,
    negativos o neutrales. Además, traduce automáticamente para mejorar la precisión.
    """)
    st.markdown("### ⚙️ Opciones de entrada")
    modo = st.selectbox(
        "Selecciona el modo de entrada:",
        ["Texto directo", "Archivo de texto"]
    )

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================
def traducir_texto(texto):
    """Traduce texto al inglés para mejorar el análisis de sentimiento."""
    try:
        return GoogleTranslator(source='auto', target='en').translate(texto)
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto

def contar_palabras(texto):
    """Cuenta palabras ignorando conectores comunes."""
    palabras = re.findall(r'\b\w+\b', texto.lower())
    stop_words = set(["de", "la", "que", "el", "en", "y", "a", "los", "se", "del", "las", 
                      "por", "un", "para", "con", "no", "una", "su", "al", "lo", "como",
                      "más", "pero", "sus", "le", "ya", "o", "fue", "este", "ha", "sí",
                      "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "también"])
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    conteo = {}
    for p in palabras_filtradas:
        conteo[p] = conteo.get(p, 0) + 1
    return dict(sorted(conteo.items(), key=lambda x: x[1], reverse=True))

def procesar_texto(texto):
    """Analiza sentimiento, subjetividad y palabras clave."""
    texto_traducido = traducir_texto(texto)
    blob = TextBlob(texto_traducido)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    palabras = contar_palabras(texto)
    return sentimiento, subjetividad, palabras, texto_traducido

# =====================================================
# INTERFAZ PRINCIPAL
# =====================================================
if modo == "Texto directo":
    st.subheader("✏️ Escribe tu texto para analizar")
    texto = st.text_area("", height=180, placeholder="Ejemplo: Me encanta ver cómo mi bebé aprende cosas nuevas 💕")

    if st.button("Analizar texto"):
        if texto.strip():
            with st.spinner("Analizando con amor y precisión... 💭"):
                sentimiento, subjetividad, palabras, traduccion = procesar_texto(texto)
                
                st.markdown("### 🔍 Resultados del análisis")
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Sentimiento:**")
                    st.progress((sentimiento + 1) / 2)
                    if sentimiento > 0.2:
                        st.success(f"💖 Positivo ({sentimiento:.2f})")
                    elif sentimiento < -0.2:
                        st.error(f"💔 Negativo ({sentimiento:.2f})")
                    else:
                        st.info(f"😐 Neutral ({sentimiento:.2f})")

                with col2:
                    st.write("**Subjetividad:**")
                    st.progress(subjetividad)
                    if subjetividad > 0.5:
                        st.warning(f"💭 Alta subjetividad ({subjetividad:.2f})")
                    else:
                        st.info(f"📋 Baja subjetividad ({subjetividad:.2f})")

                st.markdown("### 🔡 Palabras más frecuentes")
                top_palabras = dict(list(palabras.items())[:10])
                st.bar_chart(top_palabras)

                st.markdown("### 🌍 Texto traducido")
                st.text(traduccion)
        else:
            st.warning("Por favor, escribe algo para analizar 🍼")

else:
    st.subheader("📂 Carga un archivo de texto (.txt, .csv o .md)")
    archivo = st.file_uploader("", type=["txt", "csv", "md"])
    if archivo is not None:
        contenido = archivo.getvalue().decode("utf-8")
        with st.expander("👀 Ver contenido del archivo"):
            st.text(contenido[:1000])
        if st.button("Analizar archivo"):
            with st.spinner("Procesando archivo..."):
                sentimiento, subjetividad, palabras, traduccion = procesar_texto(contenido)
                st.success("✅ Análisis completado")
                st.bar_chart(dict(list(palabras.items())[:10]))

# =====================================================
# PIE DE PÁGINA
# =====================================================
st.markdown("---")
st.markdown(
    f"<p style='text-align:center; color:{COLOR_PRIMARIO}; font-size:0.9em;'>"
    "Desarrollado con 💕 por el equipo BAE — Inteligencia afectiva al servicio del cuidado</p>",
    unsafe_allow_html=True
)

