import os


from pdf2image import convert_from_path,convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from googletrans import Translator
from flask import Flask, render_template, request, url_for
import pytesseract
from PIL import Image
import cv2 
file_translate = Translator()


__author__ = 'ibininja'

app = Flask(__name__)

def path_image(image_data,file_name):
    path=os.path.join('E:/Gowtham/Project/Python/Online Ocr/Source', file_name)
    image_data.save(path)
    return path

@app.route("/")
def index():
    
    return render_template("upload.html")

@app.route("/", methods=['POST'])
def upload():
    global scanned_text
    image_data = request.files['file']
    file_name=request.files['file'].filename
    print(file_name)
   
    print(image_data)
    
    ext=file_name.split('.')[-1].lower()
    print(ext)
    if ext == 'pdf':
        path=path_image(image_data,file_name)
        images=convert_from_path(path,poppler_path=r"C:/Program Files/poppler-0.68.0/bin")
        scanned_text=""
        count=0
        for pg,img in enumerate(images):
            if count==0:
                scanned_text=pytesseract.image_to_string(img,lang="eng")
                count=count+1 
                scanned_text ="".join([s for s in scanned_text.strip().splitlines(True) if s.strip()])
                print(scanned_text)
        
        os.remove(path)          
      
        
    else:
        scanned_text = pytesseract.image_to_string(Image.open(image_data),lang="tam")
        scanned_text ="".join([s for s in scanned_text.strip().splitlines(True) if s.strip()])
        print(scanned_text)
    return render_template("upload.html", extracted_text=scanned_text )


@app.route("/Translate",methods=['POST'])
def Translate():
    ocr_txt=request.form['OCR_TEXT']
    value=request.form.get('Trans_lang')
    print(value)
    print("Translate")
    result=file_translate.translate(ocr_txt,dest=value)   
    print(result.text) 
    return render_template("upload.html", Translated_text=result.text,extracted_text=ocr_txt)



if __name__ == "__main__":
    app.run(debug=False)
