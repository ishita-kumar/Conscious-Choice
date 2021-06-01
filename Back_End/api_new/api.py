#!/usr/bin/env python3

# Install Libraries
from typing import KeysView
from flask import Flask, request, render_template,jsonify
import joblib
import traceback
import pandas as pd
import extension_crawler
import numpy as np
from flask import Flask,session,app
from flask import jsonify
from flask import request,Response
from flask_cors import CORS
import multiprocessing
from multiprocessing import Process
from flask_pymongo  import PyMongo
from bson.binary import Binary
import json 
import pickle
# import new_crawler
import configparser
from flask_cors import CORS, cross_origin
from scraper import run_code


application = Flask(__name__)
cors=CORS(application)
# application.config['MONGO_DBNAME'] = 'sustainable'
# application.config['MONGO_URI'] = 'mongodb+srv://sustainableapp:crawl123@cluster0.ufueq.mongodb.net/Sustainable_Crawler?retryWrites=true&w=majority'


application.config['MONGO_DBNAME'] = 'crawled_products'
application.config['MONGO_URI'] = 'mongodb://SustainableConsumption:SusCons4SoCoAtLuddy@socolab.luddy.indiana.edu:27017/SustainableConsumption?tls=true'

mongo = PyMongo(application)

# @application.route('/prediction', methods=["POST"])
# # define function
# def predict():
#     print('Search Term sent')
#     data = request.json["search"]
#     print(data)

#     # data_record=mongo.db.searched_strings
#     # data_record.insert_one({"search":data})
       
#     record = mongo.db.crawled_products

#     if record.find_one({"Search-Term":data},{"_id":1})==None:
#         print("Inside if")
#         new_crawler.run(data)
    
#     else:
#         print("Inside else")
#         Statement_Record=record.find({"Search-Term":data},{"Other Product Details":1})
        
#         for statement in Statement_Record:
#             string_result=""
#             if len(statement["Other Product Details"])>1:
#                 for sent in statement["Other Product Details"]:
#                     string_result+=sent
#                     print("Here",string_result)
#             else:
#                 string_result=statement["Other Product Details"] 
#                 print("Here else",string_result)

#             output={"Statement":string_result}
#             print(output)

        
#             y = json.dumps(output)

#     #record = mongo.db.crawled_products

#     #if record.find_one({"Search-Term": data}, {"_id": 1}) == None:
#      #   print("Inside if")
#       #  new_crawler.run(data)

#     #else:
#      #   print("Inside else")
#       #  Statement_Record = record.find(
#        #     {"Search-Term": data}, {"Other Product Details": 1})

#         #for statement in Statement_Record:
#          #   string_result = ""
#           #  if len(statement["Other Product Details"]) > 1:
#            #     for sent in statement["Other Product Details"]:
#             #        string_result += sent
#              #       print("Here", string_result)
#             #else:
#              #   string_result = statement["Other Product Details"]
#               #  print("Here else", string_result)

#            ##output = {"Statement": string_result}
#            # print(output)

#             #y = json.dumps(output)

#             print(type(y))

#             features2 = tf.transform([y])
#             predict = list(regr_multirf.predict(features2))
#             print("Prediction",predict)
#             res = {
#             'people': predict[0][0],
#             'planet': predict[0][1],
#             'animal': predict[0][2]
#             }

#             print("New Result",res)
#             # ts=Binary(pickle.dumps(predict,protocol=2),subtype=128)
#             # #ts=predict.tostring()
#             # print("Output",ts)
#             #print(np.fromstring(ts,dtype=np.float64))
#             mongo.db.crawled_products.update_one({"_id":statement["_id"]},{"$set":{"Sustainable_index":res}})

#     final_record=mongo.db.crawled_products.find({"Search-Term":data},{"Title":1,"Price":1,"Rating":1,"Review_Count":1,"Availability":1,"Product IMG Link":1,"Related Product Details":1,"Other Product Details":1,"Sustainable_index":1})
#     length=final_record.count()
#     print("Length",length)
#     output1=[]
#     for ans1 in final_record:
#         output1.append({"Title":ans1['Title'],"Price":ans1['Price'],"Rating":ans1["Rating"],"Review_Count":ans1["Review_Count"],"Availability":ans1["Availability"],"ImageURL":ans1["Product IMG Link"],"Related Product Details":ans1["Related Product Details"],"Other Product Details":ans1["Other Product Details"],"Sustainable_Index":ans1["Sustainable_index"]})
#         print("Output 1:",output1)
#     return jsonify({"result": output1})
    
@application.route('/scrape', methods=["POST"])
@cross_origin()
def _get_data():
    json_ = request.json
    # print("JSON",json_)
    for x in json_:
        url=x["URL"]
    print("URL",url)
    result = run_code(url)
    res=result[0]['Other Product Details']
    desc=res[0]
    extension_crawler.run(url)

    # price=res[1]
    record = mongo.db.prod_predictions
    y=""
    # s=record.find()[0]
    if record.find_one({"Title":desc }) == None:
        print("not found")
        for val in res[1:]:
            y+=str(val)    
            # response = requests.post("http://127.0.0.1:12345/prediction", data={"Statement": string_result})
            # response = requests.post("http://156.56.83.10:13691/prediction", data={"Statement": string_result})
        features2 = tf.transform([y])
        predict = regr_multirf.predict(features2)
        ans = {
                'people': predict[0][0],
                'planet': predict[0][1],
                'animal': predict[0][2]
            }
        final_ans=jsonify(ans)
        record.deleteOne({"Title":desc })
    #     record.insert_one({"Title":desc,"Sustainable_Index":ans
    #   })
        # print("INSERTED RECORD")
        extension_crawler.run(url)
        return final_ans
        #  asynchr call my etencraw.run - insetred predction db 
    else:
        Statement_Record =record.find_one({"Title":desc })
        print(desc)
        res_dict=(Statement_Record['Sustainable_Index'])
        print("LOOKING INTO DB")
        ans = json.dumps(res_dict)
        return ans       

@application.route('/getRecommendations', methods=['POST'])
def Recommendations():
    record = mongo.db.prod_predictions
    json_ = request.json
    print("JSON",json_)
    x=""
    print("JOSON",json_)
   
    prod_name=json_['title']
    print(prod_name)
    if record.find_one({"Title":prod_name }):
        Statement_Record =record.find_one({"Title":prod_name })
        print("Hiiiiiiiiiiiiiiiii")
        print(Statement_Record)
    else:
        print("record not found")
    # for x in json_:
    #     Statement_Record['Title']
    #     title=x["title"]
    # Statement_Record =record.find_one({"Title":title })
    # print("lalal",Statement_Record)
    return x
    # result={
    #     "related_product_Name":Statement_Record["Related Product Details"]
        
    #         # "related_product_Name":Statement_Record["Related Product Details"]["Product_Name"],
    #         # "related_product_url":Statement_Record["Related Product Details"]["url"],
    #         # "related_product_img":Statement_Record["Related Product Details"]["Product_Name"]

    # }
    # result=jsonify(result)
    # print(result)
    # return result
    # # related_product_Name=Statement_Record["Related Product Details"]["Product_Name"]
    # related_product_url=Statement_Record["Related Product Details"]["url"]
    # related_product_img=Statement_Record["Related Product Details"]["Product_Name"]


    
    




@application.route('/fetchOnboardingLabels', methods=['GET'])
def fetchOnboardingLabels():
    # reading from labels.ini config file
    config = configparser.ConfigParser()
    config.read('labels.ini')
    arr = []
    for section_name in config.sections():
        for (key, val) in config.items(section_name):
            obj = {
                "id": key,
                "val": val
            }
            arr.append(obj)

    return jsonify({'result': arr})



@application.route('/saveOnBoardingResponse', methods=["POST"])
def saveOnBoardingData():
    user_collection = mongo.db.user_collection
    name = request.json["name"]
    email = request.json["email"]
    rating = request.json["rating"]
    if user_collection.find_one({"email": email}) == None:
        user_collection.insert_one(
            {"name": name, "email": email, "rating": rating})
        
        return jsonify({'result': "Details saved in db"})
    else:

        query = {"email": email}
        newvalues = {"$set": {"rating": rating}}
        user_collection.update_one(query, newvalues)

        #need to remove
        query = {"email": email}
        user_collection.delete_one(query)

        return jsonify({'result': "Participant already exists updated rating"})


if __name__ == "__main__":
    # try:
    #     port = int(sys.argv[1])
    # except:
    #     port = 12345
    regr_multirf = joblib.load("randomfs.pkl")
    print("Model loaded")
    rnd_columns = joblib.load("rnd_columns.pkl")  # Load “rnd_columns.pkl”
    print("Model columns loaded")
    tf= joblib.load("tfidf.pkl")
    application.run(host='0.0.0.0',port=13693, debug=True)