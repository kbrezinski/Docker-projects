
# -*- coding: utf-8 -*-

import numpy as np
import pickle
import pandas as pd 
import sklearn

from flask import Flask, request
from PIL import Image

app = Flask(__name__)
classifier = pickle.load(open("classifier.pkl","rb"))

@app.route('/')
def welcome():
    return "Welcome All"

@app.route('/predict', methods=["Get"])
def predict_note_authentication():
    variance = request.args.get("variance")
    skewness = request.args.get("skewness")
    kurtosis = request.args.get("kurtosis")
    entropy = request.args.get("entropy")
    prediction = classifier.predict([[variance, skewness, kurtosis, entropy]])
    return str(prediction)

@app.route('/predict_file', methods=["Post"])
def predict_note_authentication_file():
    df_test = pd.read_csv(request.files.get("file"))
    prediction = classifier.predict(df_test)
    return str(list(prediction))

if __name__ == '__main__':
    app.run()
    