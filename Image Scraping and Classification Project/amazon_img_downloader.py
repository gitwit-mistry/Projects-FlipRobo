#!/usr/bin/python

"""
Created on Wed Apr 27 18:22:32 2021

@author: Mistry Prathamesh
@email : mistryprathamesh@gmail.com
@linkedIn: www.linkedin.com/in/prathamesh-mistry-a111071b4
"""

import time
import os
import urllib
import shutil
from glob import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class Amazon_Image_Scaper:
    
    def __init__(self):
        self.split_type = 'train'
        self.cat_dict = {0: 'All Departments',
                         1: 'Arts & Crafts',
                         2: 'Automotive',
                         3: 'Baby',
                         4: 'Beauty & Personal Care',
                         5: 'Books',
                         6: 'Computers',
                         7: 'Digital Music',
                         8: 'Electronics',
                         9: 'Kindle Store',
                         10: 'Prime Video',
                         11: "Women's Fashion",
                         12: "Men's Fashion",
                         13: "Girls' Fashion",
                         14: "Boys' Fashion",
                         15: 'Deals',
                         16: 'Health & Household',
                         17: 'Home & Kitchen',
                         18: 'Industrial & Scientific',
                         19: 'Luggage',
                         20: 'Movies & TV',
                         21: 'Music, CDs & Vinyl',
                         22: 'Pet Supplies',
                         23: 'Software',
                         24: 'Sports & Outdoors',
                         25: 'Tools & Home Improvement',
                         26: 'Toys & Games',
                         27: 'Video Games'}
    
    def get_info(self):

        print("Please select the category of your item:")
        for i,j in self.cat_dict.items():
            print(i,":",j) 
        
        self.category = int(input("Enter your category number:"))
        
        self.item = input("Enter the name of your item:")
        
        self.img_count = int(input("How many images do you need?"))

        self.split_req = input("Do you need Train and Test and/or Val Split?(y=yes|any other key=no):\n")

        self.tts = 0.0
        if self.split_req == 'y':
            self.tts = float(input("Test Split Ratio [0-1]\n:")) # enter a value between 0 to 1       

        print(f"We will be getting {self.img_count} images of {self.item} from {self.cat_dict[self.category]} category! ")
        
        root_path = "downloaded_images"
        
        if not os.path.exists(root_path):
            os.makedirs(root_path)  


        arg = 'y'
        while True:

            self.path = input("directory to store image:")                
            self.dir_path = os.path.join(root_path, self.path)     

            if not os.path.exists(self.dir_path):

                os.makedirs(self.dir_path)

                if self.split_req == 'y':
                	os.makedirs(os.path.join(self.dir_path,"train"))
                	os.makedirs(os.path.join(self.dir_path,"test"))
                	self.image_path = os.path.join(self.dir_path, self.split_type)
                else:
                	self.image_path = self.dir_path
                	pass
                break
            else:
                if self.split_req == 'y':
                    self.image_path = os.path.join(self.dir_path, self.split_type)
                else:
                    self.image_path = self.dir_path
                arg = input("folder exists.. do you want to overwrite:(y=yes|any other key=no)")
            if arg == 'y':
                shutil.rmtree(f'downloaded_images/{self.path}')
                print('deltedone')
                os.makedirs(self.dir_path)
                if self.split_req == 'y':
	                os.makedirs(os.path.join(self.dir_path,"train"))
	                os.makedirs(os.path.join(self.dir_path,"test"))
                break

    def get_item_img(self):

        opts = Options()

        driver = webdriver.Chrome(r"C:\Users\Admin\.wdm\drivers\chromedriver\win32\90.0.4430.24\chromedriver.exe",options=opts)

        url = "https://www.amazon.com/"

        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.24 Safari/537.36")

        driver.get(url)
        
        driver.find_element_by_xpath(f'//option[contains(text(),"{self.cat_dict[self.category]}")]').click()

        inputElement = driver.find_element_by_id("twotabsearchtextbox")
        inputElement.send_keys(self.item, Keys.ENTER)
        
        count = 0    
        while True:
            for i in driver.find_elements_by_class_name("s-image"):
                count += 1
                urllib.request.urlretrieve(i.get_attribute('src'),self.image_path+f"/{count}.jpg") 

                if count > self.img_count*(1-self.tts):
                    self.split_type = 'test'
                    self.image_path = os.path.join(self.dir_path, self.split_type) 

                if count > self.img_count - 1:
                    break
            if count == self.img_count:
                break

            driver.find_element_by_xpath("//li[@class='a-last']/a").click()
            time.sleep(3)
        


    
if __name__ == '__main__':
    print("This script downloads images from amazon ...")
    while True:
        obj =  Amazon_Image_Scaper()    
        obj.get_info()
        obj.get_item_img()
        print("Your Images have been downloaded!!!")
        reiter = input("Do you want to download any other images from amazon(y=yes|any other key=no)")
        if reiter=='y':
            pass
        else:
            print("Thank You!...Exitting Gracefully")
            time.sleep(1)
            print(".")
            time.sleep(1)
            print("..")
            time.sleep(1)
            print("...")
            break