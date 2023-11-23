from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin
from wasteDetection.pipeline.training_pipeline import TrainingPipeline
from wasteDetection.utils import read_yaml, create_directories, decodeImage
from wasteDetection.constants import *
from wasteDetection.pipeline.prediction_pipeline import PredictionPipeline
import os


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/train')
def trainRoute():
    training_pipeline = TrainingPipeline()
    training_pipeline.train()
    return 'Model trained successfully'


@app.route('/predict', methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        config = read_yaml(CONFIG_FILE_PATH)
        prediction_config = config.prediction
        create_directories([prediction_config.root_dir])

        file_name = os.path.join(prediction_config.root_dir, 'inputImage.jpg')
        waste_detection = PredictionPipeline()

        image = request.json['image']
        decodeImage(image, file_name)
        result = waste_detection.predict(file_name)
        return jsonify(result)
    
    except Exception as e:
        raise e

@app.route('/live', methods=['GET'])
@cross_origin()
def predictLive():
    try:
        waste_detection = PredictionPipeline()
        waste_detection.livePredict()
    
    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)