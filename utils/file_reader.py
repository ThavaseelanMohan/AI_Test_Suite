# utils/file_reader.py

import pandas as pd
from docx import Document
from PyPDF2 import PdfReader

def read_file(file):
    """
    Reads uploaded files and returns content.
    Returns:
        - str for text-based files (.txt, .docx, .pdf)
        - pandas DataFrame for spreadsheet files (.csv, .xls, .xlsx)
    Supported file types: txt, docx, pdf, csv, xls, xlsx
    """
    filename = file.filename.lower()
    
    if filename.endswith(".txt"):
        return file.read().decode("utf-8")
    
    elif filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    
    elif filename.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Avoid NoneType
                text += page_text + "\n"
        return text.strip()
    
    elif filename.endswith(".csv"):
        df = pd.read_csv(file.stream)
        return df
    
    elif filename.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file.stream)
        return df
    
    else:
        raise ValueError(f"Unsupported file type: {filename}")