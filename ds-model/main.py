
import pandas as pd
import numpy as np

from pycaret.regression import *
from flask import Flask, request, jsonify, render_template

# pre-amble
app = Flask(__name__)

model = load_model('binaries/deployment_28042020')
cols = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    int_features = list(request.form.values())
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final], columns=cols)
    prediction = predict_model(model, data=data_unseen, round=0) 
    prediction = int(prediction.Label[0])
    return render_template("home.html", pred=f"Expected bill would be {prediction}")

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)