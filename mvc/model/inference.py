import requests
from ultralytics import YOLO
import os
from dotenv import load_dotenv

# load environement variables (API key)
load_dotenv()

# path + API token setup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'weights', 'best.pt')
PLATE_RECOGNIZER_TOKEN = os.getenv("PLATE_REC_TOKEN")

# load model once at startup (avoids reloading on every request)
model = YOLO(MODEL_PATH)

def run_occupancy(image_path):

    # run object detection on the image
    results = model(image_path)[0]
    headcount = 0

    # count detected obkected labelled as 'person'
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
    # converts the raw response into a dictionary
    data = response.json()

    # checks if any plates were actually found in results
    if data.get('results'):

        # extrates plates if detected and converts to uppercase
        return data['results'][0]['plate'].upper()
    
    # returns a default message if no plate was found 'fallback'
    return 'UNDETECTED'

def process_image(image_path):

    # runs both detection tasks
    headcount = run_occupancy(image_path)
    plate = run_alpr(image_path)

    # returns combined results
    return {
        'headcount': headcount,
        'number_plate': plate
    }