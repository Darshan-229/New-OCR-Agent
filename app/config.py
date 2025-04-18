import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths for input and output
INPUT_FOLDER = os.path.join(BASE_DIR, '..', 'input_images')
OUTPUT_FOLDER = os.path.join(BASE_DIR, '..', 'output_texts')

# Tesseract path (only needed for Windows; skip if you're on Linux/Mac and it's already in PATH)
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update if needed

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

# Ensure input/output folders exist
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
