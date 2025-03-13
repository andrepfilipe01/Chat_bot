import glob
import os
import spacy
from PyPDF2 import PdfReader

# Load the spaCy model for sentence segmentation
nlp = spacy.load("en_core_web_sm")

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
    
    # Process the text with spaCy to split it into sentences
    doc = nlp(all_text)
    
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip() != '']
    
    for sentence in sentences:
        print(sentence)

def main():
    print("Extracting text from PDFs...")
    pdf_folder = "./pdfs"
    parse_all_pdfs(pdf_folder)

if __name__ == "__main__":
    main()
