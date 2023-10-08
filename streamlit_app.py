import streamlit as st
import spacy
import tempfile

def main():
    st.title("Corrección de documentos Word en español")
    uploaded_file = st.file_uploader("Cargar documento Word", type=['docx'], key='docx')
    
    if uploaded_file is not None:
        text = extract_text_from_docx(uploaded_file)

        nlp = spacy.load('es_core_news_sm')
        corrected_text = correct_text(text, nlp)

        temp_file = save_tmp_document(corrected_text)
        st.download_button("Descargar documento corregido", temp_file, 'documento_corregido.txt')

def extract_text_from_docx(docx_file):
    text = ""
    for paragraph in docx_file.paragraphs:
        text += paragraph.text + "\n"
    return text

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

def save_tmp_document(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    temp_filename = temp_file.name
    with open(temp_filename, "w", encoding="utf-8") as file:
        file.write(text)
    return temp_filename

if __name__ == "__main__":
    main()
