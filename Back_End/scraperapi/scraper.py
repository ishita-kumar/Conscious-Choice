  
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
from selenium.webdriver.chrome.options import Options

def create_webdriver() :

    path=os.path.abspath(os.path.dirname(__file__))
    print(path)
    chrome_options = Options()
    # chrome_options.add_argument('disable-infobars')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--lang=en')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')

    # driver=webdriver.Chrome("C://Users//Chotu//Desktop//Sustainability_Study//SustainableConsumption//Back_End//chromedriver.exe")
    driver=webdriver.Chrome(options=chrome_options)

    return driver
def get_other_details(soup):
    try:
        item_list=[]
        # //*[@id="detailBullets_feature_div"]/ul/li[4]/span/span[2]
        
        asinno=soup.find_elements_by_xpath('//*[@id="productTitle"]')
        price = soup.find_element_by_xpath("//span[@id='priceblock_ourprice']").text
        # asinno=soup.find_elements_by_xpath('//*[@id="detailBullets_feature_div"]/ul/li[4]/span/span[2]')
        if asinno:
            for item in asinno:
                item_list.append(item.text)
        item_list.append(price)
        about_this_item=soup.find_elements_by_xpath('.//*[@id="feature-bullets"]/ul/li')
        if about_this_item:
            for item in about_this_item:
                item_list.append(item.text)
        product_description=soup.find_element_by_xpath('//*[@id="productDescription"]')
        if product_description: 
            item_list.append(product_description.text)
        print(item_list)
        return item_list

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        item_list.append("No product")
        price = "$0"  
        # print(item_list)
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



