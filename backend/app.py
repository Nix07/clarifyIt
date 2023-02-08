import time
import json
from flask import Flask, request, abort, request
from flask_cors import CORS

import preprocessing
import make_predictions
import read_data
import dbutils


models = read_data.get_trained_models()
vectorizers = read_data.get_vectorizers()
selectors = read_data.get_trained_selectors()
train_data_dic = read_data.get_features_extreme_values()

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return json.dumps({'status': 'live'})


@app.route('/session', methods=['GET', 'POST'])
def insertSessionData():
    if request.method == 'GET':
        response = json.loads(dbutils.fetchlastSessionId())
        return json.dumps(response, indent=4)
    else:
        data = request.get_json(force=True)
        print('Data Received:', data)
        response = json.loads(dbutils.insertSessionData(data))
        return json.dumps(response, indent=4)


@app.route('/create-task', methods=['POST'])
def insertCreatedTaskData():
    data = request.get_json(force=True)
    print('Data Received:', data)
    response = dbutils.insertCreatedTask(data)
    return json.dumps(response, indent=4)


@app.route('/evaluation', methods=['POST'])
def insertEvaluationData():
    data = request.get_json(force=True)
    print('Data Received:', data)
    response = dbutils.insertEvaluationData(data)
    return json.dumps(response, indent=4)


@app.route('/predict', methods=['POST'])
def computeTaskClarity():
    start = time.time()
    data = request.get_json(force=True)
    print('Data Received:', data)

    features = preprocessing.compute(data, train_data_dic)
    print(f'Feature completion time: {time.time() - start}')

    predictions = make_predictions.predict(
        features, models, selectors, vectorizers)

    response = dbutils.insertToolData(data, predictions)
    print(f'Complete time taken: {time.time() - start}')

    return json.dumps(response, indent=4)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
