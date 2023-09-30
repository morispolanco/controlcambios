import streamlit as st
import requests
from docx import Document

# Cambiar el título en la pestaña del navegador
st.set_page_config(page_title="AITranslate", layout="centered")

# URL base de la API de AI Translate
BASE_URL = "https://ai-translate.pro/api"

# Función para traducir texto
def translate_text(text, lang_from, lang_to, secret_key):
    url = f"{BASE_URL}/{secret_key}/{lang_from}-{lang_to}"
    headers = {'Content-Type': 'application/json'}
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()["result"]
        available_chars = response.json()["available_chars"]
        return result, available_chars
    else:
        return None, None

# Título de la aplicación
st.title("AITranslate")

# Agregar título y texto en la parte superior
st.markdown("## La mejor traducción automática del mundo")
st.markdown("Las redes neuronales de AITranslate son capaces de captar hasta los más mínimos matices y reproducirlos en la traducción a diferencia de cualquier otro servicio. Para evaluar la calidad de nuestros modelos de traducción automática, realizamos regularmente pruebas a ciegas. En las pruebas a ciegas, los traductores profesionales seleccionan la traducción más precisa sin saber qué empresa la produjo. AITranslate supera a la competencia por un factor de 3:1.")

# Campo de entrada para la clave API
secret_key = st.text_input("Ingrese su clave API de AITranslate", type="password")

# Explicación sobre cómo obtener la clave API
st.markdown("Para obtener la clave API de AI Translate, por favor envíe un correo electrónico a info@editorialarje.com.")

# Cargar archivo DOCX en español
uploaded_file = st.file_uploader("Cargar archivo DOCX en español", type=["docx"])

# Botón para traducir
if st.button("Traducir"):
    if secret_key and uploaded_file is not None:
        # Leer el contenido del archivo DOCX en español
        docx_es = Document(uploaded_file)
        text_es = "\n".join([paragraph.text for paragraph in docx_es.paragraphs])

        # Traducir el texto al inglés
        translation_en, _ = translate_text(text_es, "es", "en", secret_key)

        if translation_en:
            # Crear un nuevo documento DOCX con la traducción al inglés
            docx_en = Document()
            docx_en.add_paragraph(translation_en)

            # Traducir el documento en inglés de nuevo al español
            translation_es, _ = translate_text(translation_en, "en", "es", secret_key)

            if translation_es:
                # Crear un nuevo documento DOCX con la traducción al español
                docx_es_translated = Document()
                docx_es_translated.add_paragraph(translation_es)

                # Guardar el documento traducido al español en un objeto BytesIO
                docx_buffer = BytesIO()
                docx_es_translated.save(docx_buffer)
                docx_buffer.seek(0)

                # Descargar el archivo DOCX traducido al español
                st.download_button("Descargar documento traducido al español", data=docx_buffer, file_name="documento_traducido.docx")

                st.success("El documento traducido al español se ha guardado en el archivo 'documento_traducido.docx'")
            else:
                st.error("Error al traducir el documento del inglés al español. Verifique su clave API o intente nuevamente.")
        else:
            st.error("Error al traducir el documento del español al inglés. Verifique su clave API o intente nuevamente.")
    else:
        st.error("Por favor, ingrese su clave API de AI Translate y cargue un archivo DOCX en español.")
