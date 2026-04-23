from flask import Blueprint, request, jsonify
import os
from mvc.model.inference import process_image
from mvc.model.database import insert_entry, get_all_entries

entry_bp = Blueprint('entry', __name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')

@entry_bp.route('/api/entry', methods=['POST'])
def log_entry():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    gate_id = request.form.get('gate_id', 1)
    image = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    result = process_image(image_path)
    insert_entry(result['number_plate'], result['headcount'], gate_id)

    return jsonify(result), 200

@entry_bp.route('/api/entries', methods=['GET'])
def get_entries():
    entries = get_all_entries()
    return jsonify(entries), 200