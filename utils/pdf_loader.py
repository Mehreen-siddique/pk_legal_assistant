import os
import fitz

def load_pdf_text(file_path: str) -> str:
    """
    Reads a PDF file using PyMuPDF (fitz), extracts all text page by page,
    and returns the combined text.
    
    Args:
        file_path (str): Absolute or relative path to the PDF file.
        
    Returns:
        str: Extracted raw text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
        
    try:
        doc = fitz.open(file_path)
        text_list = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text_list.append(page.get_text())
        doc.close()
        return "\n".join(text_list)
    except Exception as e:
        print(f"Error reading PDF {file_path}: {str(e)}")
        raise RuntimeError(f"Failed to load PDF {file_path}: {str(e)}")
