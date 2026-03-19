import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter  # ← yeh updated line

def load_pdf(file_path: str) -> str:
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

def split_text(text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)

def load_and_split(file_path: str) -> list:
    text = load_pdf(file_path)
    chunks = split_text(text)
    print(f"✅ Total chunks no: {len(chunks)}")
    return chunks