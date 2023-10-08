import streamlit as st
import requests
from PIL import Image

# Configuración de las credenciales
subscription_key = "bd43ff7a-c218-4228-8379-78333b20e73e"
endpoint = "https://cara-recon.cognitiveservices.azure.com/face/v1.0/detect"

# Función para realizar la solicitud de reconocimiento facial
def reconocer_cara(image_file):
    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(endpoint, headers=headers, data=image_file)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Configuración de la aplicación Streamlit
st.title("Reconocimiento Facial")

# Cargar imagen
image_file = st.file_uploader("Cargar imagen", type=["jpg", "jpeg", "png"])

if image_file is not None:
    # Mostrar la imagen
    image = Image.open(image_file)
    st.image(image, caption="Imagen cargada", use_column_width=True)

    # Realizar el reconocimiento facial
    resultado = reconocer_cara(image_file)

    if resultado is not None:
        # Mostrar los resultados del reconocimiento facial
        st.subheader("Resultados del reconocimiento facial:")
        for cara in resultado:
            st.write("Cara detectada:")
            st.write(" - Edad: ", cara["faceAttributes"]["age"])
            st.write(" - Género: ", cara["faceAttributes"]["gender"])
            st.write(" - Emoción: ", cara["faceAttributes"]["emotion"])
            st.write(" - Sonrisa: ", cara["faceAttributes"]["smile"])
            st.write(" - Gafas: ", cara["faceAttributes"]["glasses"])
            st.write(" - Barba: ", cara["faceAttributes"]["facialHair"]["beard"])
            st.write(" - Bigote: ", cara["faceAttributes"]["facialHair"]["moustache"])
    else:
        st.error("Error al realizar el reconocimiento facial.")
