import os
import sys
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import traceback

# Add root path for local imports
sys.path.append(str(Path(__file__).parent))

# Import your own modules
from app.ocr_agent import perform_ocr
from app.utils import is_allowed_file

# Flask setup
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({'message': 'OCR Agent is Running!'})

@app.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        print("[ERROR] No file part in request")
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']
    if file.filename == '':
        print("[ERROR] No selected file")
        return jsonify({'error': 'No selected file'}), 400

    if file and is_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        print(f"[INFO] File saved at: {file_path}")

        try:
            # Debugging: Log the file path being passed to perform_ocr
            print(f"[DEBUG] Passing file to perform_ocr: {file_path}")
            extracted_result = perform_ocr(file_path)

            if not extracted_result:
                print("[ERROR] OCR failed or result is None")
                return jsonify({'error': 'OCR failed or image unreadable'}), 500

            # Debugging: Log the extracted result
            print(f"[DEBUG] OCR result: {extracted_result}")

            result = {
                'text': extracted_result.get('text', ''),
                'math_expressions': extracted_result.get('math_expressions', []),
                'tables': extracted_result.get('tables', [])
            }

            return jsonify(result)

        except Exception as e:
            print(f"[FATAL ERROR] Unhandled Exception in /extract route: {str(e)}")
            traceback.print_exc()
            return jsonify({'error': 'Server encountered an unexpected error.'}), 500

    print("[ERROR] Unsupported file type")
    return jsonify({'error': 'Unsupported file type'}), 400

if __name__ == "__main__":
    app.run(debug=True)