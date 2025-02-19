import pytesseract
from pdf2image import convert_from_path
import io
from PyPDF2 import PdfReader, PdfWriter


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def is_pdf_flattened(pdf_file_path):

    with open(pdf_file_path, 'rb') as file:

        reader = PdfReader(file)

        page = reader.pages[0]  

        extracted_text = page.extract_text()

        if not extracted_text or len(extracted_text) < 10:  

            return True  
        return False




def convert_flatten_to_searchable(pdf_file_path, output_pdf_path="output_searchable.pdf"):
    
    pages = convert_from_path(pdf_file_path, 500)

   
    pdf_writer = PdfWriter()

    for page in pages:
        
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(page, extension="pdf")

       
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))

      
        pdf_writer.add_page(pdf_reader.pages[0])

   
    with open(output_pdf_path, "wb") as f:
        pdf_writer.write(f)

    print(f"OCR process completed! Searchable PDF saved as: {output_pdf_path}")












    
    


