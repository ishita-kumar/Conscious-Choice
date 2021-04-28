# Install Libraries
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sys
import joblib
import traceback
import pandas as pd
import numpy as np
import json 


application = Flask(__name__)
CORS(application, support_credentials=True)
@application.route('/')
def hello_world():
    return 'Hey, we have Flask in a Docker container!'

@application.route('/prediction', methods=["POST"])
@cross_origin(supports_credentials=True)

# define function
def predict():

    json_ = request.json
    y = json.dumps(json_)
    # query = pd.get_dummies(pd.DataFrame(json_))
    # query = query.reindex(columns=rnd_columns, fill_value=0)
    # print(type(y))

    features2 = tf.transform([y])
    predict = regr_multirf.predict(features2)
    res = {
        'people': predict[0][0],
        'planet': predict[0][1],
        'animal': predict[0][2]
    }
    return jsonify(res)
    

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 5001
    regr_multirf = joblib.load("randomfs.pkl")
    # print("Model loaded")
    rnd_columns = joblib.load("rnd_columns.pkl")  # Load “rnd_columns.pkl”
    # print("Model columns loaded")
    tf= joblib.load("tfidf.pkl")
    # application.run(port=port, debug=True, host='0.0.0.0')
    application.run(port=13691,debug=True, host="0.0.0.0")

    # application.run(port=port, debug=True)
