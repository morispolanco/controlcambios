import streamlit as st
import requests
from docx import Document
from io import BytesIO
import os

# Cambiar el título en la pestaña del navegador
st.set_page_config(page_title="AICorrect", layout="centered")

# Función para corregir texto utilizando la API de DeepL
def correct_text(text, lang_from, lang_to):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": "bf24d7da-c037-e26e-ea0a-becd1e742d97:fx",
        "text": text,
        "source_lang": lang_from,
        "target_lang": lang_to
    }
    response = requests.post(url, data=params)
    correction = response.json()["translations"][0]["text"]
    return correction

# Título de la aplicación
st.title("AI Correct")

# Agregar título y texto en la parte superior
st.markdown("## La mejor corrección automática del mundo")

# Cargar archivo DOCX en español
uploaded_file = st.file_uploader("Cargar archivo DOCX en español", type=["docx"])

# Botón para corregir
if st.button("Corregir"):
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

                # Verificar si el texto excede el límite de 500.000 caracteres
                if len(text_es) > 500000:
                    st.error("El texto excede el límite de 500.000 caracteres.")
                else:
                    # Corregir el texto en español utilizando la API de DeepL
                    correction_es = correct_text(text_es, "ES", "ES")

                    # Crear un nuevo documento DOCX con la corrección en español
                    corrected_docx_es = Document()
                    corrected_docx_es.add_paragraph(correction_es)

                    # Guardar el documento DOCX en un objeto BytesIO
                    docx_buffer_es = BytesIO()
                    corrected_docx_es.save(docx_buffer_es)
                    docx_buffer_es.seek(0)

                    # Descargar el archivo DOCX corregido en español
                    st.download_button("Descargar corrección en español", data=docx_buffer_es, file_name="correccion_espanol.docx")

                    st.success("La corrección en español se ha guardado en el archivo 'correccion_espanol.docx'")
            except Exception as e:
                st.error(f"Error al leer el archivo DOCX: {e}")
    else:
        st.error("Por favor, cargue un archivo DOCX en español.")
