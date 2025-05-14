from ultralytics import YOLO
from utils import split_save_train_val_test, masks_to_labels, save_masked_by_yolo, cropp_and_save_masked
from utils import copy_matching_files, read_water_meter
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Загрузка моделей при старте
segment_model = YOLO('models/segment_model.pt')
detect_model = YOLO('models/detect_model.pt')

@app.route('/')
def index():
    return 'Meter Reader API is running.'

@app.route('/ping')
def ping():
    return '', 200

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_path = os.path.join('data', 'temp.jpg')
    image_file.save(image_path)

    try:
        result = read_water_meter(
            image_path,
            segmentation_model_path='models/segment_model.pt',
            detection_model_path='models/detect_model.pt',
            path_to_save_predictions='predictions'
        )
        return jsonify({'value': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
