import streamlit as st
import requests
from docx import Document
from io import BytesIO
from docx_diff import compare

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

# Cargar archivo DOCX
uploaded_file = st.file_uploader("Cargar archivo DOCX", type=["docx"])

# Obtener la clave API desde los secretos
secret_key = st.secrets["aitranslate"]["api_key"]

# Botón para traducir
if st.button("Traducir"):
    if secret_key and uploaded_file is not None:
        # Leer el contenido del archivo DOCX
        docx = Document(uploaded_file)
        text = "\n".join([paragraph.text for paragraph in docx.paragraphs])

        # Traducción del español al inglés
        lang_from = "es"
        lang_to = "en"
        translation_english, _ = translate_text(text, lang_from, lang_to, secret_key)

        # Traducción del inglés al español
        lang_from = "en"
        lang_to = "es"
        translation_spanish, available_chars = translate_text(translation_english, lang_from, lang_to, secret_key)

        # Crear documentos DOCX con el texto original y traducido
        original_docx = Document()
        original_docx.add_paragraph(text)

        translated_docx = Document()
        translated_docx.add_paragraph(translation_spanish)

        # Comparar los documentos y obtener el resultado
        comparison_result = compare(original_docx, translated_docx)

        # Guardar el resultado en un nuevo archivo DOCX
        comparison_docx = Document()
        comparison_docx.add_paragraph(comparison_result)

        # Guardar el documento de comparación en un objeto BytesIO
        comparison_buffer = BytesIO()
        comparison_docx.save(comparison_buffer)
        comparison_buffer.seek(0)

        # Descargar el archivo de comparación
        st.download_button("Descargar comparación", data=comparison_buffer, file_name="comparacion.docx")

        st.success("La comparación se ha guardado en el archivo 'comparacion.docx'")
        st.info(f"Caracteres disponibles: {available_chars}")
    else:
        st.error("Por favor, cargue un archivo DOCX.")
