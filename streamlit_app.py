import streamlit as st
import requests
from docx import Document
from io import BytesIO
import os

# Cambiar el título en la pestaña del navegador
st.set_page_config(page_title="AITranslate", layout="centered")

# URL base de la API de AI Translate
BASE_URL = "https://ai-translate.pro/api"

# Función para corregir texto
def correct_text(text, lang_from, lang_to, secret_key):
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
st.markdown("## La mejor corrección automática del mundo")
st.markdown("Las redes neuronales de AITranslate son capaces de captar hasta los más mínimos matices y reproducirlos en la corrección a diferencia de cualquier otro servicio. Para evaluar la calidad de nuestros modelos de corrección automática, realizamos regularmente pruebas a ciegas. En las pruebas a ciegas, los correctores profesionales seleccionan la corrección más precisa sin saber qué empresa la produjo. AITranslate supera a la competencia por un factor de 3:1.")

# Campo de entrada para la clave API
secret_key = st.text_input("Ingrese su clave API de AITranslate", type="password")

# Explicación sobre cómo obtener la clave API
st.markdown("Para obtener la clave API de AI Translate, por favor envíe un correo electrónico a info@editorialarje.com.")

# Cargar archivo DOCX en español
uploaded_file = st.file_uploader("Cargar archivo DOCX en español", type=["docx"])

# Botón para corregir
if st.button("Corregir"):
    if secret_key and uploaded_file is not None:
        # Verificar si el archivo cargado es un archivo DOCX válido
        if os.path.splitext(uploaded_file.name)[1] != ".docx":
            st.error("Por favor, cargue un archivo DOCX válido.")
        else:
            try:
                # Abrir el archivo en modo de lectura
                file_stream = BytesIO(uploaded_file.read())
                docx = Document(file_stream)
                text_es = "\n".join([paragraph.text for paragraph in docx.paragraphs])

                # Corregir el texto en español
                correction_es, available_chars = correct_text(text_es, "es", "es", secret_key)
                if correction_es:
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
                    st.info(f"Caracteres disponibles: {available_chars}")
                else:
                    st.error("Error al corregir el texto en español. Verifique su clave API o intente nuevamente.")
            except Exception as e:
                st.error(f"Error al leer el archivo DOCX: {e}")
    else:
        st.error("Por favor, ingrese su clave API de AI Translate y cargue un archivo DOCX en español.")
import streamlit as st
import requests
from docx import Document
from io import BytesIO
import os

# Cambiar el título en la pestaña del navegador
st.set_page_config(page_title="AITranslate", layout="centered")

# URL base de la API de AI Translate
BASE_URL = "https://ai-translate.pro/api"

# Función para corregir texto
def correct_text(text, lang_from, lang_to, secret_key):
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
st.markdown("## La mejor corrección automática del mundo")
st.markdown("Las redes neuronales de AITranslate son capaces de captar hasta los más mínimos matices y reproducirlos en la corrección a diferencia de cualquier otro servicio. Para evaluar la calidad de nuestros modelos de corrección automática, realizamos regularmente pruebas a ciegas. En las pruebas a ciegas, los correctores profesionales seleccionan la corrección más precisa sin saber qué empresa la produjo. AITranslate supera a la competencia por un factor de 3:1.")

# Campo de entrada para la clave API
secret_key = st.text_input("Ingrese su clave API de AITranslate", type="password")

# Explicación sobre cómo obtener la clave API
st.markdown("Para obtener la clave API de AI Translate, por favor envíe un correo electrónico a info@editorialarje.com.")

# Cargar archivo DOCX en español
uploaded_file = st.file_uploader("Cargar archivo DOCX en español", type=["docx"])

# Botón para corregir
if st.button("Corregir"):
    if secret_key and uploaded_file is not None:
        # Verificar si el archivo cargado es un archivo DOCX válido
        if os.path.splitext(uploaded_file.name)[1] != ".docx":
            st.error("Por favor, cargue un archivo DOCX válido.")
        else:
            try:
                # Abrir el archivo en modo de lectura
                file_stream = BytesIO(uploaded_file.read())
                docx = Document(file_stream)
                text_es = "\n".join([paragraph.text for paragraph in docx.paragraphs])

                # Corregir el texto en español
                correction_es, available_chars = correct_text(text_es, "es", "es", secret_key)
                if correction_es:
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
                    st.info(f"Caracteres disponibles: {available_chars}")
                else:
                    st.error("Error al corregir el texto en español. Verifique su clave API o intente nuevamente.")
            except Exception as e:
                st.error(f"Error al leer el archivo DOCX: {e}")
    else:
        st.error("Por favor, ingrese su clave API de AI Translate y cargue un archivo DOCX en español.")
