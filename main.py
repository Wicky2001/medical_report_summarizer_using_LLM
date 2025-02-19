from utills.pdf_module import is_pdf_flattened,convert_flatten_to_searchable
from utills.llm_module import get_summerized_response,anonymize_text
import time
import threading
from tqdm import tqdm
from IPython.display import display, Markdown


def progress_bar():
    with tqdm(total=100, desc="Processing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        while thread.is_alive():  
            pbar.update(10)  
            time.sleep(1)
        pbar.update(100 - pbar.n)  


print("--------------------WELCOME MEDICAL PDF SUMMERIZER---------------------- \n ")
print("**please upload your medical report int to 'pdf_storage folder'** ")

pdf_name = input("Please enter pdf name -> ")

pdf_path = f"pdf_storage/{pdf_name}.pdf"


if is_pdf_flattened(pdf_file_path=pdf_path):
    print("Need to use ocr to extract the text")
    output_pdf_path=f"pdf_storage/{pdf_name}_searchable.pdf"
    convert_flatten_to_searchable(pdf_file_path=pdf_path,output_pdf_path=output_pdf_path)

    pdf_path = output_pdf_path




thread = threading.Thread(target=get_summerized_response, args=(pdf_path,))
thread.start()
progress_bar()


thread.join()
print("Done!")









