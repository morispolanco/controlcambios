import streamlit as st
import spacy
from docx import Document

def main():
    st.title("Corrección de documentos Word en español")
    uploaded_file = st.file_uploader("Cargar documento Word", type=['docx'], key='docx')
    
    if uploaded_file is not None:
        document = Document(uploaded_file)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text

        nlp = spacy.load('es_core_news_sm')
        corrected_text = correct_text(text, nlp)

        new_document = Document()
        new_document.add_paragraph(corrected_text)
        st.download_button("Descargar documento corregido", download_document(new_document), 'documento_corregido.docx')

def correct_text(text, nlp):
    # Realizar aquí la corrección del texto con Spacy
    return corrected_text

def download_document(document):
    temp_doc = save_tmp_document(document)
    
    return temp_doc

def save_tmp_document(document):
    temp_doc = "temp_document.docx"
    document.save(temp_doc)
    
    return temp_doc

if __name__ == "__main__":
    main()
