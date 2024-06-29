import cv2
import numpy as np
import easyocr
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from langchain_groq.chat_models import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from prompts import *

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

reader = easyocr.Reader(['en'])

app = FastAPI()

# def preprocess_and_extract_text_tesseract(image):
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     thresholded_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

#     result = reader.readtext(thresholded_image, detail=0)
#     easyocr_text1 = "\n".join(result)
#     return easyocr_text1

def extract_text_easyocr(image):
    try:
        result = reader.readtext(image, detail=0)
        easyocr_text = "\n".join(result)
        return easyocr_text
    except Exception as e:
        return ""

def extract_important_info(easyocr_text, prompt):
    llm = ChatGroq(
        groq_api_key="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",
        model_name="Llama3-70b-8192"
    )
    template = PromptTemplate(
        input_variables=["easyocr_text", "prompt"],
        template="""
        I have extracted text from image using OCR method i.e. EasyOCR. I am providing extracted text here.
        Here is the extracted information:
        {easyocr_text}

        -----------------------------------------------------------

        {prompt}        
        
        If any information is not found, return "Not Found" for that field.
        """
    )
    formatted_prompt = template.format(easyocr_text=easyocr_text, prompt=prompt)
    messages = [HumanMessage(content=formatted_prompt)]
    response = llm.invoke(messages)
    extracted_info = response.content
    info_lines = extracted_info.split('\n')
    info_dict = {}
    for line in info_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            info_dict[key.strip()] = value.strip()

    info_dict = {key: value for key, value in info_dict.items() if value != ""}
        
    return info_dict

def process_image(image, prompt):
    # easyocr_text1 = preprocess_and_extract_text_tesseract(image)
    easyocr_text = extract_text_easyocr(image)
    extracted_info = extract_important_info(easyocr_text, prompt)
    return extracted_info

@app.post("/process-image/")
async def process_image_endpoint(file: UploadFile = File(...), document_type: str = Form(...)):
    contents = await file.read()
    image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return JSONResponse(status_code=400, content={"message": "Invalid image file"})
    
    if document_type == 'Driving Licence':
        selected_prompt = dl_prompt
    elif document_type == 'ID':
        selected_prompt = id_prompt
    elif document_type == 'Passport':
        selected_prompt = passport_prompt
    else:
        return JSONResponse(status_code=400, content={"message": "Invalid document type"})
    
    try:
        result = process_image(image, selected_prompt)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
