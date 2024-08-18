from pdb import run
import streamlit as st
import openai
from gtts import gTTS
import os
from PyPDF2 import PdfFileReader
import io
from openai import OpenAI

# Set up OpenAI API key

#openai.api_key = 'Enter your API key' 

client = OpenAI(api_key='Enter your API key')


def translate_text(input_text, target_language):
    completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Translator"},
                {"role": "user", "content": f"Translate the following text to {target_language}:\n\n{input_text}"}
            ]
        )
    return completion.choices[0].message.content




def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("output.mp3")
    return "output.mp3"



def extract_text_from_pdf(file):
    pdf_reader = PdfFileReader(file)
    text = ""
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
    return text



st.title("Language Translation and Text-to-Speech Application")



# User input

input_text = st.text_area("Enter text to translate")

language = st.selectbox("Select target language", ["es", "fr", "de", "zh"])



if st.button("Translate"):
    if input_text:
        translated_text = translate_text(input_text, language)
        st.write("Translated Text:", translated_text)
        audio_file = text_to_speech(translated_text, language)
        audio = open(audio_file, "rb")
        audio_bytes = audio.read()

        st.audio(audio_bytes, format='audio/mp3')
    else:
        st.error("Please enter text to translate.")



uploaded_file = st.file_uploader("Upload a text or PDF file", type=["txt", "pdf"])



if uploaded_file:
    if uploaded_file.type == "text/plain":
        text = str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)

    st.write("Extracted Text:", text)

    translated_text = translate_text(text, language)
    st.write("Translated Text:", translated_text) 
    audio_file = text_to_speech(translated_text, language)
    audio = open(audio_file, "rb")
    audio_bytes = audio.read()

    st.audio(audio_bytes, format='audio/mp3')