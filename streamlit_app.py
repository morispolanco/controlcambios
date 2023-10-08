import streamlit as st
import requests
import sounddevice as sd
import soundfile as sf
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
st.title("Transcripción de Audio en Tiempo Real")

# Inicializar variables
recording = False
audio_frames = []

# Botón para iniciar/detener la grabación
if st.button("Iniciar/Detener Grabación"):
    if not recording:
        recording = True
        st.write("Grabando...")
        audio_frames = []
        # Configurar la grabación de audio desde el micrófono
        samplerate = 44100
        duration = 10  # Duración de la grabación en segundos
        audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
        sd.wait()
        # Guardar la grabación en un archivo WAV
        wav_audio = io.BytesIO()
        sf.write(wav_audio, audio, samplerate)
        wav_audio.seek(0)
        # Realizar la transcripción del audio
        texto_transcrito = transcribir_audio(wav_audio)
        if texto_transcrito is not None:
            # Mostrar el texto transcrito
            st.text("Texto transcrito:")
            st.write(texto_transcrito)
        else:
            st.error("Error al realizar la transcripción del audio.")
    else:
        recording = False
        st.write("Grabación detenida.")
