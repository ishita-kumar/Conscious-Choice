import csv
import json
import os
import time
import argparse
from time import sleep
from datetime import datetime
from random import random
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pymongo
from bs4 import BeautifulSoup
#from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import joblib
import traceback
import pandas as pd
import numpy as np

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
    # chrome_options.add_argument('--allow-running-insecure-content')
    # chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--disable-browser-side-navigation')
    # chrome_options.add_argument('--mute-audio')
    # chrome_options.add_argument('--headless')
    driver=webdriver.Chrome(options=chrome_options)
    #driver=webdriver.Chrome("/home/soco/sustainable/Sustainable_App/SustainableConsumption/api/chromedriver_linux64/chromedriver.exe",options=chrome_options)
    return driver


def generate_url(search_term, page):
    base_template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
    stem = base_template.format(search_term)
    url_template = stem + '&page={}'
    if page == 1:
        return stem
    
    else:
        return url_template.format(page)


# Function to extract Product Title
def get_title(driver):
     
    try:
        # Outer Tag Object
        title = driver.find_element_by_xpath("//span[@id='productTitle']")
 
        # Inner NavigatableString Object
        title_value = title.text
 
        # Title as a string value
        title_string = title_value.strip()
 
 
    except Exception:
        title_string = "Unknown"   
 
    return title_string

def get_product_img(soup):
        try:
            #img=soup.find_element_by_xpath("//div[@id='imageBlock_feature_div']")
            img1=soup.find_element_by_xpath("//*[@id='landingImage']").get_attribute("src")
        except:
            img1="No Image Link"
        return img1

    
# Function to extract Product Price
def get_price(soup):
 
    try:
        #xpathprice='//span[@id="price_inside_buybox"]'
#       price=driver.find_element_by_xpath(xpathprice)

        price = soup.find_element_by_xpath("//span[@id='priceblock_ourprice']").text
       
 
    except Exception:
 
        try:
            # If there is some deal price
            price = soup.find_element_by_xpath("//span[@id='priceblock_saleprice']").text
 
        except:     
            price = "$0"  
 
    return price
 
# Function to extract Product Rating
def get_rating(soup):
 
    try:
        rating = soup.find_element_by_xpath("//span[@data-hook='rating-out-of-text']").text
        #print(rating)
         
    except Exception:
         
        try:
            rating = soup.find_element_by_xpath("//span[@data-hook='rating-out-of-text']").text
        except:
            rating = "None" 
 
    return rating
 
# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find_element_by_xpath("//span[@id='acrCustomerReviewText']").text.strip()
         
    except Exception:
        review_count = "0"   
 
    return review_count
 
# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find_element_by_xpath("//div[@id='availability']")
        available = available.find_element_by_tag_name("span").text.strip()
 
    except Exception:
        available = "Not Available"
 
    return available   


# def get_individual_rating_counts(driver):
#     try:
#         XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
#         total_ratings = driver.find_elements_by_xpath(XPATH_AGGREGATE_RATING)
#         ratings_dict={}
#         ratings_list=[]
#         for ratings in total_ratings:
#             extracted_rating = ratings.find_elements_by_xpath('.//td//a')
#             if extracted_rating:
#                 rating_key = extracted_rating[0].text
#                 raw_raing_value = extracted_rating[2]
#                 rating_value = raw_raing_value.text
#                 if rating_key:
#                     ratings_dict.update({rating_key: rating_value})
#         ratings_list.append(ratings_dict)
                
#     except:
#         ratings_list="No Review_Count Breakdown"
#     return ratings_list
        

# def get_productdetails(soup):
#     try:

#         no_rows=len(soup.find_elements_by_xpath("//table[@class='a-normal a-spacing-micro']/tbody/tr"))
      
#         no_cols=len(soup.find_elements_by_xpath("//table[@class='a-normal a-spacing-micro']/tbody/tr[1]/td"))
       
#         data=[]
#         for i in range(1,no_rows+1):
#             ro=[]
#             for j in range(1,no_cols+1):
                
#                 ro.append(soup.find_element_by_xpath('//table[@class="a-normal a-spacing-micro"]/tbody/tr['+str(i)+']/td['+str(j)+']').text)
#             data.append(ro)
       
 
        
#     except:
#         data.append("No Detail Found for the Product")
    
#     return data


def get_other_details(soup):
    try:
        item_list=[]
        about_this_item=soup.find_elements_by_xpath('//*[@id="feature-bullets"]/ul/li')
        for item in about_this_item:
            item_list.append(item.text)
           
        product_description=soup.find_element_by_xpath('//*[@id="productDescription"]').text
        item_list.append(product_description)
       
    except:
        item_list.append("No additional description of the Product")

            
    return item_list
    
def get_relatedproducts(soup):
                count=0
                related_products=[]
                while count<=2:
                   
                    try:

                      
                        lists=soup.find_elements_by_xpath('//div[@class="a-carousel-viewport"]')
                        #print(list)
                       
                        for card in range(len(lists)):
                            # related=soup.find_element_by_xpath('//li[@class="a-carousel-card"]['+str(card+1)+']').text
                            # related_products.append(related)
                            #print(related)
                            related_title=soup.find_element_by_xpath('//li[@class="a-carousel-card"]['+str(card+1)+']//a[@class="a-link-normal"]').text
                            print("R.....",related_title)
                            related_url=soup.find_element_by_xpath('//li[@class="a-carousel-card"]['+str(card+1)+']//a[@class="a-link-normal"]').get_attribute("href")
                            # related_img= soup.find_element_by_xpath('//li[@class="a-carousel-card"]['+str(card+1)+']//a[@class="a-link-normal"]').get_attribute("href")
                           #time.sleep(2)
                            #WebDriverWait(soup, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//li[@class="a-carousel-card"]['+str(card+1)+']//div[@class="a-row"]//span')))
                            # print("Down....")
                            rating_text=soup.find_element_by_xpath('//li[@class="a-carousel-card"]['+str(card+1)+']//div[@class="a-row"]//span').text
                            #rate=rating_text.text
                            # print("B....",rating_text)
                           #time.sleep(2)
                            related_img=soup.find_element_by_xpath('//li[@class="a-carousel-card"]['+str(card+1)+']//a[@class="a-link-normal"]//img').get_attribute("src")
                            price_text=soup.find_element_by_xpath('//li[@class="a-carousel-card"]['+str(card+1)+']//div[@class="a-row a-color-price"]//span').text
                            #pix=price_text.text
                           #time.sleep(2)
                            # print("C...",price_text)
                            related_dict = {
                            'Product_Name': related_title,
                            'Product_url': related_url,
                            'Price': price_text,
                            'IMG':related_img
                            }
                            print(related_dict)
                            related_products.append(related_dict)
                        count+=1

                    except Exception as e:
                        #break;
                        print("Exception",e)
                        related_products="Related Products not present for this Product"
                        count+=1
                        #condition=False
                        #print("In except")
                return related_products
            
            
            

                #print("After click()")
                
        
# def get_review_comments(driver):
#     try:
#         review_comment_list=[]
#         review_url=driver.find_element_by_xpath("//a[@data-hook='see-all-reviews-link-foot']").click()
#         reviews_lists=driver.find_elements_by_xpath("//div[@data-hook='review']")
#         print(reviews_lists)
#         for review in reviews_lists:
#             XPATH_RATING = './/i[@data-hook="review-star-rating"]//span[@class="a-icon-alt"]'
#             raw_review_rating = review.find_element_by_xpath(XPATH_RATING).get_attribute("innerHTML")
#             XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//span'
#             XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]'
#             XPATH_AUTHOR = './/span[contains(@class,"profile-name")]'
#             review_body=review.find_element_by_xpath(".//span[@data-hook='review-body']").text
#             raw_review_header = review.find_element_by_xpath(XPATH_REVIEW_HEADER).text
#             raw_review_posted_date = review.find_element_by_xpath(XPATH_REVIEW_POSTED_DATE).text
#             raw_review_author = review.find_element_by_xpath(XPATH_AUTHOR).text
           
#             review_dict={}
           
#             review_dict = {
            
#             'review_text': review_body,
#             'review_posted_date': raw_review_posted_date,
#             'review_header': raw_review_header,
#             'review_rating': raw_review_rating,
#             'review_author': raw_review_author
#             }
#             review_comment_list.append(review_dict)   
#             #print(review_comment_list)
#     except:
#         review_comment_list="No Reviews"
#     return review_comment_list   


def run(search):
    print("Hello")
    regr_multirf = joblib.load("randomfs.pkl")
    print("Model loaded")
    rnd_columns = joblib.load("rnd_columns.pkl")  # Load “rnd_columns.pkl”
    print("Model columns loaded")
    tf= joblib.load("tfidf.pkl")
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-s", "--search", required=True,
    #     help="Enter search term")
    # args = vars(ap.parse_args())
    driver = create_webdriver()
     
    driver.get(search)
    
    # for page in range(1, 2):  # max of 20 pages
    #             # load the next page
    #             search_url = generate_url(search, page)
    #             print(search_url)
    #             driver.get(search_url)
    #             driver.set_page_load_timeout(10)
    #             print('TIMEOUT while waiting for page to load')

               
    #             links=driver.find_elements_by_xpath('//a[@class="a-link-normal a-text-normal"]')
    #             link_list=[]
    #             counter=0
    #             for link in links:
    #                 if counter!=7:
    #                     link_list.append(link.get_attribute("href"))
    #                     counter+=1
    #                     print(counter)
                 
                
    #             for link in link_list:
    #                 driver.get(link)
    #                 driver.set_page_load_timeout(10)
    
                    # # Function calls to display all necessary product information
                    # print("Product Title =", get_title(driver))
                    # print("Product Price =", get_price(driver))
                    # print("Product Rating =", get_rating(driver))
                    # print("Number of Product Reviews =", get_review_count(driver))
                    # print("Availability =", get_availability(driver))
                    # # print("Product Details =", get_productdetails(driver))
                    # print()
                    # print()
                    
                    # #print("Related Products:",get_relatedproducts(driver))
                    
    title=get_title(driver)
    price=get_price(driver)
    rating=get_rating(driver)
    review_count=get_review_count(driver)
    availability=get_availability(driver)
                    # product_details=get_productdetails(driver)
    other_product_details=get_other_details(driver)
    related_product_details=get_relatedproducts(driver)
                    # individual_review_count=get_individual_rating_counts(driver)
    img_url=get_product_img(driver)
                    # review_counts=get_review_comments(driver)
                    

    final_data=[]
    data_dict={}

    # data_dict["Search-Term"]=search
    data_dict["Title"]=title
    data_dict["Price"]=price
    data_dict["Rating"]=rating
    data_dict["Review_Count"]=review_count
    data_dict["Availability"]=availability
                    # data_dict["Details"]=product_details
    data_dict["Other Product Details"]=other_product_details
    data_dict["Related Product Details"]=related_product_details
                    # data_dict["Individual Rating Count"]=individual_review_count
    data_dict["Product IMG Link"]=img_url
    string_result=""
    if len(data_dict["Other Product Details"])>1:
        for sent in data_dict["Other Product Details"]:
            string_result+=sent
            print("Here",string_result)
    else:
        string_result=data_dict["Other Product Details"]
        print("Here else",string_result)

    output={"Statement":string_result}
    # print(output)
    y = json.dumps(output)
       
    print(type(y))
    features2 = tf.transform([y])
    predict = list(regr_multirf.predict(features2))
    print("Prediction",predict)
    res = {
                    'people': predict[0][0],
                    'planet': predict[0][1],
                    'animal': predict[0][2]
                    }

    # print("New Result",res)

    data_dict["Sustainable_index"]=res
    final_data.append(data_dict)
    # print(final_data)
    mng_client=pymongo.MongoClient('mongodb://SustainableConsumption:SusCons4SoCoAtLuddy@socolab.luddy.indiana.edu:27017/SustainableConsumption?tls=true')
    collection_name = 'prod_predictions'
    mng_db = mng_client['SustainableConsumption'] 
    db_cm = mng_db[collection_name]
    # print(data_dict)
    db_cm.insert_one(data_dict)
                    # data_dict["Review Comments"]=review_counts
# run("https://www.amazon.com/Hanes-Tagless-Black-Grey-Undershirts-Crewneck/dp/B018MS5Y8E/ref=sr_1_1?dchild=1&keywords=t-shirt&qid=1622497621&s=books&sr=1-1")
                    
                    
                    


                    

                  
                  
                    
                    
                  


# run("car")
