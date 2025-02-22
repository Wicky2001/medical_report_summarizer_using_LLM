import streamlit as st
from utills.pdf_module import is_pdf_flattened,convert_flatten_to_searchable
from utills.llm_module import get_summerized_response,anonymize_text
import os
import time
import threading




def main():
    st.markdown("<h1 style='text-align: center; color: grey;'>MEDICAL REPORT SUMMARIZER</h1>", unsafe_allow_html=True)

    UPLOAD_FOLDER = "pdf_storage"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "csv", "png", "jpg"])

    if uploaded_file is not None:
        
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File successfully saved to: {file_path}")



if __name__ == "__main__":
    main()