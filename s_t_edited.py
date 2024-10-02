import os
import streamlit as st
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from gtts import gTTS
from googletrans import Translator
from PIL import Image
import time
import glob

# Título de la aplicación
st.title("🌐 **Traductor de Voz**")
st.subheader("¡Hable y traduzca fácilmente!")

# Cargar y mostrar la imagen
image = Image.open('OIG7.jpg')
st.image(image, width=300)

# Instrucciones en la barra lateral
with st.sidebar:
    st.subheader("Instrucciones:")
    st.write("1. **Presiona el botón** para iniciar el reconocimiento de voz.")
    st.write("2. **Habla** lo que deseas traducir.")
    st.write("3. **Selecciona** las configuraciones de idioma y acento.")
    st.write("4. **Presiona 'Convertir'** para obtener el audio traducido.")

# Botón para iniciar el reconocimiento de voz
st.write("🔊 **Toca el botón y habla para traducir:**")
stt_button = Button(label="Escuchar 🎤", width=300, height=50)

# Código JavaScript para el reconocimiento de voz
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

# Procesar el resultado del reconocimiento de voz
result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# Si hay resultado, procesar la traducción
if result and "GET_TEXT" in result:
    spoken_text = result.get("GET_TEXT")
    st.success(f"🎉 Texto reconocido: **{spoken_text}**")

    # Crear carpeta temporal si no existe
    os.makedirs("temp", exist_ok=True)

    st.title("🔊 **Texto a Audio*
