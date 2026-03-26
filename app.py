import streamlit as st
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import PyPDF2
import io

# ========== CONFIG ==========
st.set_page_config(page_title="OCR Extractor", layout="wide")

# ========== FUNCTIONS ==========

def extract_from_image(file):
    img = Image.open(file).convert("L")
    return pytesseract.image_to_string(img)

def extract_from_text_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_from_scanned_pdf(file):
    images = convert_from_bytes(file.read())
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

def detect_pdf_type(file):
    try:
        reader = PyPDF2.PdfReader(file)
        sample = reader.pages[0].extract_text()
        file.seek(0)
        return "text_pdf" if sample else "scanned_pdf"
    except:
        file.seek(0)
        return "scanned_pdf"

# ========== UI ==========

st.title("📄 Image & PDF to Text Extractor")
st.write("Upload an image or PDF to extract text automatically.")

uploaded_file = st.file_uploader(
    "Upload File",
    type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_file:
    file_type = ""

    # Detect type
    if uploaded_file.type.startswith("image"):
        file_type = "image"
    elif uploaded_file.type == "application/pdf":
        file_type = detect_pdf_type(uploaded_file)
    else:
        file_type = "unsupported"

    text = ""

    # ========== SWITCH CASE ==========
    match file_type:
        case "image":
            st.info("🖼️ Processing Image...")
            text = extract_from_image(uploaded_file)

        case "text_pdf":
            st.info("📄 Processing Text PDF...")
            text = extract_from_text_pdf(uploaded_file)

        case "scanned_pdf":
            st.info("📄 Processing Scanned PDF...")
            text = extract_from_scanned_pdf(uploaded_file)

        case _:
            st.error("Unsupported file type")

    # ========== OUTPUT ==========
    if text:
        st.subheader("Extracted Text")
        st.text_area("", text, height=300)

        st.download_button(
            label="Download Text",
            data=text,
            file_name="output.txt",
            mime="text/plain"
        )
