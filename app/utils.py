import os
from werkzeug.utils import secure_filename
from app.config import ALLOWED_EXTENSIONS, INPUT_FOLDER  # 👈 absolute import

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file):
    if file and is_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(INPUT_FOLDER, filename)
        file.save(filepath)
        return filepath
    else:
        raise ValueError("Invalid file type. Allowed: PNG, JPG, JPEG, BMP")
