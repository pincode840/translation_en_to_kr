import cv2
import numpy as np
import pytesseract
import pandas as pd
from tensorflow.keras.models import load_model

# Tesseract OCR 경로 설정 (윈도우의 경우)
pytesseract.pytesseract.tesseract_cmd = r'C:\PJ_python'

# CNN 모델 로드 (모델을 미리 훈련시켜야 합니다. 여기는 로드만 하는 예시)
# model = load_model('path_to_your_trained_model.h5')

def preprocess_image(image_path):
    # 이미지 읽기
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # 이미지 이진화
    _, binary_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)

    # 외곽선 검출
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return image, binary_image, contours

def extract_table(image, binary_image, contours):
    # 테이블을 인식하고 추출
    table_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    table_image = None
    for contour in table_contours:
        x, y, w, h = cv2.boundingRect(contour)
        table_image = image[y:y+h, x:x+w]
        break

    return table_image

def extract_text_from_image(image):
    # 텍스트 추출 (OCR)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def text_to_csv(text, csv_output_path):
    # 텍스트를 CSV로 변환
    data = []
    for row in text.split('\n'):
        data.append(row.split())
    
    df = pd.DataFrame(data)
    df.to_csv(csv_output_path, index=False, header=False)

def main(image_path, csv_output_path):
    image, binary_image, contours = preprocess_image(image_path)
    table_image = extract_table(image, binary_image, contours)
    
    if table_image is not None:
        text = extract_text_from_image(table_image)
        text_to_csv(text, csv_output_path)
        print(f"CSV 파일이 저장되었습니다: {csv_output_path}")
    else:
        print("테이블을 찾을 수 없습니다.")

# 사용 예시
image_path = 'path_to_your_image_with_table.jpg'
csv_output_path = 'output_table.csv'
main(image_path, csv_output_path)
