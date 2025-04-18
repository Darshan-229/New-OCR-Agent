import cv2
import pytesseract
import os
from PIL import Image
from utils.image_preprocessing import preprocess_image
from .math_table_agent import extract_math_expressions, extract_tables
import numpy as np
import traceback

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def perform_ocr(image_path, save_output=True):
    try:
        print(f"[INFO] Loading image: {image_path}")
        print(f"[DEBUG] Tesseract path: {pytesseract.pytesseract.tesseract_cmd}")

        # Load image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not loaded. Check file path or file format.")

        print("[INFO] Preprocessing image...")
        processed_image = preprocess_image(image)
        if processed_image is None or not isinstance(processed_image, np.ndarray):
            raise ValueError("Image preprocessing failed. Ensure preprocess_image returns a valid image.")

        print("[INFO] Converting image to RGB for OCR...")
        rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2RGB)
        pil_image = Image.fromarray(rgb_image)

        print("[INFO] Performing OCR...")
        text = pytesseract.image_to_string(pil_image)

        print("[INFO] Extracting math expressions...")
        math_data = extract_math_expressions(text)

        print("[INFO] Extracting tables...")
        table_data = extract_tables(text)

        result = {
            "text": text,
            "math_expressions": math_data,
            "tables": table_data
        }

        if save_output:
            os.makedirs("output/extracted_texts", exist_ok=True)
            base_name = os.path.basename(image_path).rsplit('.', 1)[0]
            output_path = os.path.join("output/extracted_texts", f"{base_name}_output.txt")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write("----- Extracted Text -----\n")
                f.write(text + "\n\n")
                f.write("----- Math Expressions -----\n")
                for eq in math_data:
                    f.write(eq + "\n")
                f.write("\n----- Table Structures -----\n")
                for table in table_data:
                    f.write(str(table) + "\n")

            print(f"[INFO] Output saved to {output_path}")

        return result

    except Exception as e:
        print(f"[ERROR] OCR failed: {str(e)}")
        traceback.print_exc()
        return None