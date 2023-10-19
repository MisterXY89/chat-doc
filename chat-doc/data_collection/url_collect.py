"""
starting from this url: https://icd.who.int/browse11/l-m/en, 
collect data-ids that start with http://id.who.int/icd/entity/
and save them to a file

use selenium to load the page and then use beautifulsoup to parse the html
"""

import os
import time
import json
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from config import logger

# set the path to the output file
output_file = os.path.join(os.getcwd(), 'data', 'data_ids.txt')

# set the path to the log file
log_file = os.path.join(os.getcwd(), 'data', 'log.txt')

# set the path to the error file
error_file = os.path.join(os.getcwd(), 'data', 'error.txt')

# set the path to the data directory
data_dir = os.path.join(os.getcwd(), 'data')


class UrlCollect:

    def __init__(self, url, output_file, driver_path=None, log_file="log.txt", error_file="error.txt", data_dir="data"):
        self.base_url = url
        self.driver_path = driver_path
        self.output_file = output_file
        self.log_file = log_file
        self.error_file = error_file
        self.data_dir = data_dir
        self.data = {}
        self.clicked_links = []

    # initialize the driver
    def init_driver(self, driver_path=None):
        """
        initialize the driver, optionally passing in the driver_path to the chromedriver.exe
        """
        if not driver_path:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Chrome(driver_path)

        logger.info("driver initialized")

    def get_soup(self):
        """
        load the page and return the soup
        """
        self.driver.get(self.base_url)

        # wait for the page to load
        time.sleep(5)

        html = self.driver.page_source
        return BeautifulSoup(html, 'html.parser')

    def collect_children(self, parent_tag):
        pass

    def save_data(self):
        """
        self.data is a dict -> this continuesly saves the data to the output file (streaming)
        best way to do this is to use the json module
        """

        # check if the data directory exists
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        # save the data to the output file
        with open(self.output_file, 'w') as f:
            json.dump(self.data, f)

    
    def wrap_up(self):
        """
        close the driver, and write logs and errors to files
        """
        self.driver.close()

        # write to the log file
        with open(self.log_file, 'a') as f:
            f.write('data-ids collected\n')

        # write to the error file
        with open(self.error_file, 'a') as f:
            f.write('no errors\n')
        
    
    def setup_collect(self):
        """
        setup the data collection
        """
        self.init_driver()
        return self.get_soup()
    
    def open_link_tree(self, soup):
        """
        open the entire link-tree (all links with href="#")
        this is done recursivly by clicking on the respective links until 
        there are no more links to click on (save clicked link-objs to a list)
        """

        # find all elements with class: 'ygtv-collapsed'
        collapsed_elements = soup.find_all('table', {'class': 'ygtv-collapsed'})

        # replace 'ygtv-collapsed' with 'ygtv-expanded'
        for element in collapsed_elements:
            element['class'] = 'ygtv-expanded'
            time.sleep(0.75)
        
        # # get the first link
        # link = soup.find('a', href='#')
        # print(link)        
        # if link not in self.clicked_links:
        #     self.clicked_links.append(link)

        #     # expand the tree
        #     # if click on the link does not work, try clicking on the parent element:
        #     try:
        #         link.click() 
        #     except Exception as e:
        #         link.parent.click()
            
        #     # remove the link from the soup
        #     link.decompose()
        #     self.open_link_tree(self.get_soup())        
        # else:
        #     self.save_data()
        #     self.wrap_up()
        #     return



    def collect(self):
        soup = self.setup_collect()
        
        hierarchy = soup.find('div', {'id': 'hierarchy'})
        self.open_link_tree(hierarchy)
        





# if __name__ == '__main__':
#     url_collect = UrlCollect()
#     url_collect.collect()

