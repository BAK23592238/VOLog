from flask import Blueprint, request, jsonify
import os
from mvc.model.inference import process_image
from mvc.model.database import insert_entry, get_all_entries

# create a blueprint for entry related nodes
entry_bp = Blueprint('entry', __name__)

# define path to store uploaded images (temporary folder for security)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')

@entry_bp.route('/api/entry', methods=['POST'])
def log_entry():
    # check if the request contains an image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    # get the gate ID from form data, default to 1 if not provided
    gate_id = request.form.get('gate_id', 1)

    # retrieve the uploaded image
    image = request.files['image']

    # build file path and save image to disk
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # image processing and extraction for database
    result = process_image(image_path)
    insert_entry(result['number_plate'], result['headcount'], gate_id)

    # return the processed result as JSON response
    return jsonify(result), 200

@entry_bp.route('/api/entries', methods=['GET'])
def get_entries():

    # fetch all stored entries from the database and returns
    entries = get_all_entries()
    return jsonify(entries), 200