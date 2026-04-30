import requests
from ultralytics import YOLO
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'weights', 'best.pt')
PLATE_RECOGNIZER_TOKEN = 'dddd344672634e818bf2105b96ce2d4f0c341a80'

model = YOLO(MODEL_PATH)

def run_occupancy(image_path):
    results = model(image_path)[0]
    headcount = 0
    for box in results.boxes:
        cls = int(box.cls[0])
        label = model.names[cls]
        if label == 'person':
            headcount += 1
    return headcount

# function to get number plate from image
def run_alpr(image_path):

    # opens the image as binary read mode
    with open(image_path, 'rb') as f:

        # sends request through PR API
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            headers={'Authorization': f'Token {PLATE_RECOGNIZER_TOKEN}'},
            files={'upload': f}
        )
    data = response.json()
    if data.get('results'):
        return data['results'][0]['plate'].upper()
    return 'UNDETECTED'

def process_image(image_path):
    headcount = run_occupancy(image_path)
    plate = run_alpr(image_path)
    return {
        'headcount': headcount,
        'number_plate': plate
    }