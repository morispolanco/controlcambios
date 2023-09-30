import streamlit as st
import docx2txt
import openai

# Título de la aplicación
st.title("Corrector de Textos en Español con ChatGPT")

# Cargar el documento .docx ingresado por el usuario
uploaded_file = st.file_uploader("Cargar documento (.docx)", type="docx")

# Botón para corregir el texto
if st.button("Corregir"):
    if uploaded_file is not None:
        # Leer el contenido del documento .docx
        document_text = docx2txt.process(uploaded_file)
        
        # Dividir el texto en chunks más pequeños
        chunk_size = 500  # Tamaño del chunk en caracteres
        chunks = [document_text[i:i+chunk_size] for i in range(0, len(document_text), chunk_size)]
        
        # Corregir cada chunk utilizando ChatGPT
        corrected_chunks = []
        for chunk in chunks:
            # Llamar a la API de OpenAI para corregir el chunk
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=chunk,
                max_tokens=100,
                
                n=1,
                stop=None,
                temperature=0.7
            )
            
            # Obtener la respuesta generada por ChatGPT
            corrected_chunk = response.choices[0].text.strip()
            corrected_chunks.append(corrected_chunk)
        
        # Unir los chunks corregidos en un solo texto
        corrected_text = " ".join(corrected_chunks)
        
        # Mostrar el texto corregido
        st.subheader("Texto corregido:")
        st.write(corrected_text)
    else:
        st.warning("Por favor, carga un documento antes de corregir.")
