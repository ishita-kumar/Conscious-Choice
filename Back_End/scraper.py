  
import csv
import json
from flask import Flask, render_template
import os
import time
import argparse
from datetime import datetime
from flask import Flask, request, jsonify

from random import random
from selenium.common import exceptions
from selenium import webdriver
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def create_webdriver() :

    path=os.path.abspath(os.path.dirname(__file__))
    print(path)
    # driver=webdriver.Chrome("C://Users//Chotu//Desktop//Sustainability_Study//SustainableConsumption//Back_End//chromedriver.exe")
    driver=webdriver.Chrome("./chromedriver.exe")

    return driver
def get_other_details(soup):
    
    try:
        item_list=[]
        about_this_item=soup.find_elements_by_xpath('.//*[@id="feature-bullets"]/ul/li')
        for item in about_this_item:
            item_list.append(item.text)
            print(item.text)
        product_description=soup.find_element_by_xpath('//*[@id="productDescription"]')
        item_list.append(product_description.text)
         
        return item_list

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

        item_list.append("No product")
        return item_list
def run_code(url):
    final_data=[]
    data_dict={}
    driver = create_webdriver()
    driver.get(url)
    other_product_details=get_other_details(driver)
    data_dict["Other Product Details"]=other_product_details
    final_data.append(data_dict)
    return final_data



