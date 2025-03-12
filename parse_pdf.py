import glob
import os
from PyPDF2 import PdfReader

def parse_all_pdfs(folder_path):

    all_text = ""
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))

    for pdf in pdf_files:
        print(f"Processing: {pdf}")
        reader = PdfReader(pdf)
        number_of_pages = len(reader.pages)
        
        for page_num in range(number_of_pages):
            page = reader.pages[page_num]  
            text = page.extract_text()
            all_text += text + "\n\n"
    
    return all_text

def main():
    print("Extracting text from PDFs...")
    pdf_folder = "./pdfs"
    all_text = parse_all_pdfs(pdf_folder)
    print(all_text)

if __name__ == "__main__":
    main()