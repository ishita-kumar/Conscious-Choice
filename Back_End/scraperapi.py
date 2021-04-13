from flask import Flask,request,render_template, jsonify
from flask_cors import CORS, cross_origin
from scraper import run_code
import json 
import requests
import sys


app = Flask(__name__)
CORS(app)
@app.route('/scrape', methods=["POST"])
def _get_data():
    json_ = request.json
    for x in json_:
        url=x["URL"]
    result = run_code(url)
    string_result=""
    
    for val in result:
        if len(val['Other Product Details'])>1:
            for sent in val['Other Product Details']:
                string_result+=sent
        else:
            string_result=val['Other Product Details'] 

    try:
        response = requests.post("http://127.0.0.1:12345/prediction", data={"Statement": string_result})
        return response.json()
    except requests.exceptions.HTTPError as err:
        return err.response.text


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 5000
   
    app.run(port=port, debug=True)
