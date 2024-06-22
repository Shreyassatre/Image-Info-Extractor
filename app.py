import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import easyocr
import torch
from langchain_groq.chat_models import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import streamlit as st
from prompts import *

# Set up Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
reader = easyocr.Reader(['en'], gpu=device.type == 'cuda')

def preprocess_and_extract_text_tesseract(image_path):
    image = cv2.imread(image_path)
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

def extract_text_easyocr(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return ""
    if image.shape[0] == 0 or image.shape[1] == 0:
        return ""
    try:
        result = reader.readtext(image_path, detail=0)
        easyocr_text = "\n".join(result)
        return easyocr_text
    except Exception as e:
        return ""

def extract_important_info(easyocr_text, tesseract_text, prompt):
    llm = ChatGroq(
        groq_api_key="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",
        model_name="Llama3-70b-8192"
    )
    template = PromptTemplate(
        input_variables=["tesseract_text", "easyocr_text", "prompt"],
        template="""
        I have extracted text from same image using 2 methods i.e. Tesseract and EasyOCR. I am providing both extracted text here.
        Here is the extracted information from Tesseract:
        {tesseract_text}
        And here is the extracted information from EasyOCR:
        {easyocr_text}

        You can use both texts (tesseract_text, easyocr_text) and extract important information. Note: Both texts are extracted from same image.
        
        -----------------------------------------------------------

        {prompt}        
        
        If any information is not found, return "Not Found" for that field.
        """
    )
    formatted_prompt = template.format(easyocr_text=easyocr_text, tesseract_text=tesseract_text, prompt=prompt)
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

def process_image(image_path, prompt):
    tesseract_text = preprocess_and_extract_text_tesseract(image_path)
    easyocr_text = extract_text_easyocr(image_path)
    extracted_info = extract_important_info(easyocr_text, tesseract_text, prompt)
    return extracted_info

# Streamlit UI
st.title("Document Information Extraction")

option = st.selectbox(
    'Select Type of Document',
    ('Driving Licence', 'ID', 'Passport')
)

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.')
    image_path = "temp_image.jpg"
    image.save(image_path)

    if st.button('Submit'):
        with st.spinner('Processing...'):
            # Select the appropriate prompt based on the dropdown selection
            if option == 'Driving Licence':
                selected_prompt = dl_prompt
            elif option == 'ID':
                selected_prompt = id_prompt
            else:
                selected_prompt = passport_prompt
            
            extracted_info = process_image(image_path, selected_prompt)
            st.write("Extracted Information:")
            st.json(extracted_info)
            # Clean up temporary file
            os.remove(image_path)
