import openai
import streamlit as st
from utils import transcriptor, structurer, formatter

api_key = st.text_input("Enter OpenAI API Key:", type="password")

openai.api_key = "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"

def main():
    st.title("Whisperer: Articles from Audio")

    uploaded_file = st.file_uploader("Choose an audio file (mp3 format)")

    if uploaded_file is not None:
        # UI components for user preferences
        model_size = st.selectbox("Select model size for transcription:", ["base", "small", "medium", "large"])
        language = st.selectbox("Select language:", ["English", "Spanish", "French", "German"])  # Add more languages as needed
        structure_pref = st.selectbox("Select desired note structure:", ["Article", "Simple Note", "Nested List"])
        format_pref = st.multiselect("Select formatting preferences:", ["All lowercase", "Spellcheck", "Correct orthography"])

        # Transcribe the audio
        raw_transcription = transcriptor(uploaded_file, model_size, language)

        st.text_area("", raw_transcription, height=50, key='raw')

        # Structure the transcription
        structured_transcription = structurer(raw_transcription, structure_pref)

        st.text_area("", structured_transcription, height=300, key='structure')


        # Format the transcription
        formatted_transcription = formatter(structured_transcription, format_pref)

        # Display the result
        st.subheader("Transcribed Note:")
        st.text_area("", formatted_transcription, height=300, key='format')

if __name__ == "__main__":
    main()
