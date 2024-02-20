import torch
from transformers import pipeline
import PyPDF2

def Process_PDF(input_file):
    try:
        with open(input_file,"r") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            extracted_text = ""

            for page_num in range(pdf_reader.numPages):

                page = pdf_reader.getPage(page_num)
                page_text = page.extractText()

                extracted_text += page_text

            return extracted_text
    except FileNotFoundError:
        print("file not found")



