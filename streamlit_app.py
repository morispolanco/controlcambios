import streamlit as st
import language_tool_python
from docx import Document

# Crear una instancia de LanguageTool para el idioma español
tool = language_tool_python.LanguageTool('es')

# Función para corregir el texto
def corregir_texto(texto):
    correcciones = tool.check(texto)
    texto_corregido = language_tool_python.correct(texto, correcciones)
    return texto_corregido

# Configuración de la aplicación Streamlit
st.title("Corrección Gramatical en Español")
archivo_input = st.file_uploader("Cargar archivo .docx", type=['docx'])

if archivo_input is not None:
    doc = Document(archivo_input)
    texto = ' '.join([p.text for p in doc.paragraphs])
    texto_corregido = corregir_texto(texto)

    st.text("Texto corregido:")
    st.write(texto_corregido)

    # Descargar el texto corregido en un nuevo archivo .docx
    doc_corregido = Document()
    doc_corregido.add_paragraph(texto_corregido)
    st.download_button("Descargar texto corregido", data=doc_corregido.save, file_name="texto_corregido.docx")
