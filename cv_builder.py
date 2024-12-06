import openai
import streamlit as st
from docx import Document
import os
openai_api_key = os.getenv("OPENAI_API_KEY")

# Función para leer texto de un archivo Word
def leer_docx(archivo):
    doc = Document(archivo)
    texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return texto

# Función para consultar el API de GPT-3.5
def obtener_palabras_clave(cv_texto, rol_texto):
    prompt = f"""
    You are an ATS expert. Analyze the following two texts:
    
    1. Candidate's CV:
    {cv_texto}
    
    2. Job Role Description:
    {rol_texto}
    
    Identify the key skills, tools, and qualifications missing from the CV that are present in the Job Role Description. 
    Focus on keywords relevant for ATS optimization. Provide the missing keywords in a bullet list format.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional career coach specialized in ATS optimization."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0
    )
    return response['choices'][0]['message']['content']

# Configuración de Streamlit
st.title("ATS Optimizer: Improve Your CV")
st.write("Upload your CV and the Job Role description to identify missing keywords for ATS optimization.")

# Subir CV
cv_archivo = st.file_uploader("Upload your CV (Word format)", type=["docx"])
rol_texto = st.text_area("Paste the Job Role Description here:")

# Procesar y comparar
if st.button("Analyze CV and Job Role"):
    if cv_archivo and rol_texto:
        # Leer texto del CV
        cv_texto = leer_docx(cv_archivo)
        st.subheader("CV Content")
        st.text_area("Your CV:", cv_texto, height=200, disabled=True)

        # Consultar el API de OpenAI
        st.subheader("Identified Missing Keywords")
        with st.spinner("Analyzing..."):
            resultado = obtener_palabras_clave(cv_texto, rol_texto)
        st.markdown(resultado)
    else:
        st.error("Please upload your CV and provide the Job Role description.")

