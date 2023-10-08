import streamlit as st
from docx import Document
from googletrans import Translator

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

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

st.title("Traductor de documentos con Streamlit")

uploaded_file = st.file_uploader("Cargar documento DOCX", type="docx")

if uploaded_file is not None:
    document = Document(uploaded_file)
    original_text = '\n\n'.join([paragraph.text for paragraph in document.paragraphs])
    
    st.header("Texto original (español)")
    st.write(original_text)
    
    st.header("Texto traducido al inglés")
    translated_text = translate_text(original_text, 'es', 'en')
    st.write(translated_text)
    
    st.header("Texto traducido de nuevo al español")
    translated_back_text = translate_text(translated_text, 'en', 'es')
    st.write(translated_back_text)
    
    st.header("Comparación entre el documento original y traducido")
    comparison_doc = generate_comparison_doc(original_text, translated_back_text)
    st.download_button("Descargar documento de comparación", data=comparison_doc.save, file_name="comparison_doc.docx")
