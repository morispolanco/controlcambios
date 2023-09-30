import streamlit as st
import requests
from docx import Document
from io import BytesIO
import os

# Cambiar el título en la pestaña del navegador
st.set_page_config(page_title="AICorrect", layout="centered")

# Función para traducir texto utilizando la API de DeepL
def translate_text(text, lang_from, lang_to):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": "bf24d7da-c037-e26e-ea0a-becd1e742d97:fx",
        "text": text,
        "source_lang": lang_from,
        "target_lang": lang_to
    }
    response = requests.post(url, data=params)
    translation = response.json()["translations"][0]["text"]
    return translation

# Título de la aplicación
st.title("AI Correct")

# Agregar título y texto en la parte superior
st.markdown("## La mejor corrección automática del mundo")

# Cargar archivo DOCX en español
uploaded_file = st.file_uploader("Cargar archivo DOCX en español", type=["docx"])

# Botón para traducir
if st.button("Traducir"):
    if uploaded_file is not None:
        # Verificar si el archivo cargado es un archivo DOCX válido
        if os.path.splitext(uploaded_file.name)[1] != ".docx":
            st.error("Por favor, cargue un archivo DOCX válido.")
        else:
            try:
                # Abrir el archivo en modo de lectura
                file_stream = BytesIO(uploaded_file.read())
                docx = Document(file_stream)
                text_es = "\n".join([paragraph.text for paragraph in docx.paragraphs])

                # Traducir el texto al inglés utilizando la API de DeepL
                translation_en = translate_text(text_es, "ES", "EN")

                # Crear un nuevo documento DOCX con la traducción al inglés
                translated_docx_en = Document()
                translated_docx_en.add_paragraph(translation_en)

                # Guardar el documento DOCX en un objeto BytesIO
                docx_buffer_en = BytesIO()
                translated_docx_en.save(docx_buffer_en)
                docx_buffer_en.seek(0)

                # Descargar el archivo DOCX traducido al inglés
                st.download_button("Descargar traducción al inglés", data=docx_buffer_en, file_name="traduccion_ingles.docx")

                st.success("La traducción al inglés se ha guardado en el archivo 'traduccion_ingles.docx'")

                # Traducir el texto en inglés al español utilizando la API de DeepL
                translation_es = translate_text(translation_en, "EN", "ES")

                # Crear un nuevo documento DOCX con la traducción al español
                translated_docx_es = Document()
                translated_docx_es.add_paragraph(translation_es)

                # Guardar el documento DOCX en un objeto BytesIO
                docx_buffer_es = BytesIO()
                translated_docx_es.save(docx_buffer_es)
                docx_buffer_es.seek(0)

                # Descargar el archivo DOCX traducido al español
                st.download_button("Descargar traducción al español", data=docx_buffer_es, file_name="traduccion_espanol.docx")

                st.success("La traducción al español se ha guardado en el archivo 'traduccion_espanol.docx'")
            except Exception as e:
                st.error(f"Error al leer el archivo DOCX: {e}")
    else:
        st.error("Por favor, cargue un archivo DOCX en español.")
