from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import io
import os
from pdf2image import convert_from_path
import pdf2image.exceptions
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})


@app.route('/ocr', methods=['POST'])

def ocr():
    if 'image' in request.files:
        image_file = request.files['image']
        image_path = save_file(image_file, "image")
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        os.remove(image_path)  # Remove the temporary image file
        print(text)
        return {'text': text}

    if 'pdf' in request.files:
        pdf_file = request.files['pdf']
        pdf_path = save_file(pdf_file, "pdf")
        text = extract_text_from_pdf(pdf_path)
        os.remove(pdf_path)  # Remove the temporary PDF file
        print(text)
        return {'text': text}

    return {'error': 'No image or PDF file provided.'}

def save_file(file, file_type):
    if file_type == "image":
        save_path = "temp_image.png"
    elif file_type == "pdf":
        save_path = "temp_pdf.pdf"
    else:
        return None

    file.save(save_path)
    return save_path

def extract_text_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path, dpi=300, poppler_path=r'\popler\Library\bin')
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
        return text
    except pdf2image.exceptions.PDFInfoNotInstalledError:
        raise Exception("Poppler not installed or not in PATH.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6500, debug=True)