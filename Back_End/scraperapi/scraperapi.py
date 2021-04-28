from flask import Flask,request,render_template, jsonify
from flask_cors import CORS, cross_origin
from scraper import run_code
import json 
import requests
import sys
from flask_pymongo  import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'crawled_products'
app.config['MONGO_URI'] = 'mongodb://SustainableConsumption:SusCons4SoCoAtLuddy@socolab.luddy.indiana.edu:27017/SustainableConsumption?tls=true'
mongo = PyMongo(app)

@app.route('/')
def hello_world():
    return 'Running mainapi!'

CORS(app)
@app.route('/scrape', methods=["POST"])
def _get_data():
    json_ = request.json
    for x in json_:
        url=x["URL"]
    result = run_code(url)
    res=result[0]['Other Product Details']
    desc=res[0]
    price=res[1]
    record = mongo.db.crawled_products
    string_result=""
    # s=record.find()[0]
    if record.find_one({"Title":desc }) == None:
        print("not found")
        for val in res[2:]:
            string_result+=str(val)    
        try:
            # response = requests.post("http://127.0.0.1:12345/prediction", data={"Statement": string_result})
            response = requests.post("http://156.56.83.10:13691/prediction", data={"Statement": string_result})
            return response.json()
        except requests.exceptions.HTTPError as err:
            return err.response.text
    else:
        Statement_Record =record.find_one({"Title":desc })
        res_dict=(Statement_Record['Sustainable_index'])
        ans = json.dumps(res_dict)
        return ans


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 8081
#    http://127.0.0.1:8081/
#        application.run(debug=True, host="0.0.0.0")
print("scraper api running")
app.run(port=13692,debug=True, host="0.0.0.0")
