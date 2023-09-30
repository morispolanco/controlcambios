import streamlit as st
import requests
from docx import Document
from io import BytesIO
from python_docx_diff import compare, insertions, deletions

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

# Función para generar el documento con control de cambios
def generate_diff_document(original_doc, translated_doc):
    diff_doc = Document()
    changes = compare(original_doc, translated_doc)
    for change in changes:
        if isinstance(change, insertions.Insertion):
            diff_doc.add_paragraph(change.text, style='Inserted Text')
        elif isinstance(change, deletions.Deletion):
            diff_doc.add_paragraph(change.text, style='Deleted Text')
    return diff_doc

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

                # Generar el documento con control de cambios
                diff_doc = generate_diff_document(docx_es, docx_es_translated)

                # Guardar el documento con control de cambios en un objeto BytesIO
                docx_buffer = BytesIO()
                diff_doc.save(docx_buffer)
                docx_buffer.seek(0)

                # Descargar el archivo DOCX con control de cambios
                st.download_button("Descargar documento con control de cambios", data=docx_buffer, file_name="control_de_cambios.docx")

                st.success("El documento con control de cambios se ha guardado en el archivo 'control_de_cambios.docx'")
            else:
                st.error("Error al traducir el documento del inglés al español. Verifique su clave API o intente nuevamente.")
        else:
            st.error("Error al traducir el documento del español al inglés. Verifique su clave API o intente nuevamente.")
    else:
        st.error("Por favor, ingrese su clave API de AI Translate y cargue un archivo DOCX en español.")
