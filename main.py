import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import torch
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from langchain_groq.chat_models import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from prompts import *

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

app = FastAPI()

def preprocess_and_extract_text_tesseract(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised_image = cv2.fastNlMeansDenoising(gray_image, None, 30, 7, 21)
    blurred_image = cv2.GaussianBlur(denoised_image, (5, 5), 0)
    thresholded_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = gray_image[y:y+h, x:x+w]
    pil_image = Image.fromarray(cropped_image)
    enhancer = ImageEnhance.Contrast(pil_image)
    enhanced_image = enhancer.enhance(2)
    sharpened_image = enhanced_image.filter(ImageFilter.SHARPEN)
    sharpened_image_np = np.array(sharpened_image)
    kernel = np.ones((2, 2), np.uint8)
    morphed_image = cv2.morphologyEx(sharpened_image_np, cv2.MORPH_CLOSE, kernel)
    custom_config = r'--oem 3 --psm 6'
    tesseract_text = pytesseract.image_to_string(morphed_image, config=custom_config)
    return tesseract_text

def extract_important_info(tesseract_text, prompt):
    llm = ChatGroq(
        groq_api_key="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",
        model_name="Llama3-70b-8192"
    )
    template = PromptTemplate(
        input_variables=["tesseract_text", "prompt"],
        template="""
        I have extracted text from an image using Tesseract. Here is the extracted information:
        {tesseract_text}

        Please extract the important information as requested.

        -----------------------------------------------------------

        {prompt}        
        
        If any information is not found, return "Not Found" for that field.
        """
    )
    formatted_prompt = template.format(tesseract_text=tesseract_text, prompt=prompt)
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
    tesseract_text = preprocess_and_extract_text_tesseract(image)
    extracted_info = extract_important_info(tesseract_text, prompt)
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
