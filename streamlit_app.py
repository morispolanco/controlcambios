import streamlit as st
from docx import Document
import io

def generate_comparison_doc(original_text, translated_text):
    doc = Document()
    doc.add_heading('Comparación entre el documento original y traducido', 0)
    
    original_paragraphs = original_text.split('\n\n')
    translated_paragraphs = translated_text.split('\n\n')
    
    for i in range(min(len(original_paragraphs), len(translated_paragraphs))):
        doc.add_heading('Párrafo {}'.format(i+1), level=1)
        doc.add_heading('Original:', level=2)
        doc.add_paragraph(original_paragraphs[i])
        doc.add_heading('Traducido:', level=2)
        doc.add_paragraph(translated_paragraphs[i])
    
    return doc

st.title("Generador de documento de comparación con Streamlit")

uploaded_file = st.file_uploader("Cargar documento DOCX", type="docx")

if uploaded_file is not None:
    document = Document(uploaded_file)
    original_text = '\n\n'.join([paragraph.text for paragraph in document.paragraphs])
    
    st.header("Texto original")
    st.write(original_text)
    
    st.header("Generar documento de comparación")
    comparison_doc = generate_comparison_doc(original_text, original_text)

    # Guardar el documento en un objeto de datos binarios
    comparison_doc_data = io.BytesIO()
    comparison_doc.save(comparison_doc_data)
    comparison_doc_data.seek(0)

    st.download_button("Descargar documento de comparación", data=comparison_doc_data, file_name="comparison_doc.docx")
