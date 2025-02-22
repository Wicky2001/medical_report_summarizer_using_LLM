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

    uploaded_file = st.file_uploader("Upload your medical report", type=["pdf"])

    if uploaded_file is not None:
        
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File successfully saved to: {file_path}")

        # Create output file location to save pdfs wich converted to searchable
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_filename_for_flatten = os.path.join(UPLOAD_FOLDER, f"{file_name}_searchable.pdf")

        if st.button("Get summary"):
            with st.spinner("Processing.."):
                if is_pdf_flattened(file_path):
                    convert_flatten_to_searchable(pdf_file_path=file_path,output_pdf_path=output_filename_for_flatten)
                    file_path = output_filename_for_flatten

                summary = get_summerized_response(file_path)
                if(len(summary) != 0):
                    st.markdown(summary)



if __name__ == "__main__":
    main()