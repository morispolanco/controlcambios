import streamlit as st
import requests
from pydub import AudioSegment
import io

# Configuración de las credenciales
subscription_id = "bd43ff7a-c218-4228-8379-78333b20e73e"
resource_group = "Texto"
account_name = "Voa-a-texto-mp"
endpoint = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken"

# Función para realizar la solicitud de transcripción
def transcribir_audio(audio_file):
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_id,
        "Content-Type": "audio/wav"
    }
    response = requests.post(endpoint, headers=headers, data=audio_file)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Configuración de la aplicación Streamlit
st.title("Transcripción de Audio")

# Cargar archivo de audio
audio_file = st.file_uploader("Cargar archivo de audio", type=["m4a"])

if audio_file is not None:
    # Convertir archivo M4A a WAV
    audio = AudioSegment.from_file(io.BytesIO(audio_file.read()), format="m4a")
    wav_audio = io.BytesIO()
    audio.export(wav_audio, format="wav")
    wav_audio.seek(0)

    # Realizar la transcripción del audio
    texto_transcrito = transcribir_audio(wav_audio)

    if texto_transcrito is not None:
        # Mostrar el texto transcrito
        st.text("Texto transcrito:")
        st.write(texto_transcrito)
    else:
        st.error("Error al realizar la transcripción del audio.")
