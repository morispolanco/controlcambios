import streamlit as st
import spacy
from docx import Document
import tempfile

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
        temp_file = save_tmp_document(new_document)
        st.download_button("Descargar documento corregido", temp_file, 'documento_corregido.docx')

def correct_text(text, nlp):
    doc = nlp(text)
    corrected_text = ""
    for sentence in doc.sents:
        corrected_sentence = ""
        for token in sentence:
            # Realizar aquí la corrección de cada token utilizando Spacy
            corrected_sentence += token.text_with_ws
        corrected_text += corrected_sentence
    return corrected_text

def save_tmp_document(document):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_filename = temp_file.name
    document.save(temp_filename)
    return temp_filename

if __name__ == "__main__":
    main()
