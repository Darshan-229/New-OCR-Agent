import cv2
from PIL import Image
import numpy as np

def preprocess_image(image):
    """
    Preprocess the input image for OCR.
    :param image: Input image as a numpy.ndarray (loaded via OpenCV).
    :return: Preprocessed image as a numpy.ndarray.
    """
    try:
        # Ensure the input is a numpy array
        if not isinstance(image, np.ndarray):
            raise ValueError("Input to preprocess_image must be a numpy.ndarray.")

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Optional: Apply thresholding to improve OCR accuracy
        _, processed_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

        return processed_image
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {str(e)}")
        raise