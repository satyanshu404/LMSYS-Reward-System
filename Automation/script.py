import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from time import sleep
from Automation.constant import *
from bs4 import BeautifulSoup
import Automation.tools as tools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LMSYSScraper:
    def init(self):
        options = webdriver.ChromeOptions() 
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = uc.Chrome(options=options)
        # self.driver = uc.Chrome()
        self.driver.get(ScraperConstants.URL)
        self.element = tools.FindElement(self.driver)
        self.locator = tools.Locator()
        self.alert = tools.AcceptAlert(self.driver).accept()
        sleep(1)

    def check_page(self):
        '''Check the correct page'''
        try:
            logging.log(logging.INFO, "Checking the page...")
            WebDriverWait(self.driver, CheckPageConstants.WAIT_DURATION).until(
                EC.presence_of_element_located(self.locator.by_text(CheckPageConstants.TEXT))
            )
            logging.log(logging.INFO, "Page loaded successfully")
            sleep(1)
            return True
        except Exception as e:
            logging.log(logging.ERROR, f"Couldn't load the page: {e}")
            return False
        
    def go_to_arena(self):
        '''Go to the arena page'''
        logging.log(logging.INFO, "Going to the arena page...")
        # Click on the chat button
        self.element.find(self.locator.by_id(ArenaElements.CHAT_ID)).click()

    def select_model(self):
        '''Select the model from the listbox'''
        listbox = self.element.find(self.locator.by_id(ArenaElements.LISTBOX_ID))
        ActionChains(self.driver).move_to_element(listbox).click().send_keys(Keys.BACKSPACE*150).perform()
        ActionChains(self.driver).move_to_element(listbox).click().send_keys(ArenaElements.MODEL_NAME).perform()
        ActionChains(self.driver).move_to_element(listbox).click().send_keys(Keys.ENTER).perform()
        sleep(1)
    
    def genreate_response(self, message: str):
        '''Generate the response for the given message'''
        message = message.replace("\n", "\\n")
        # Select textarea 
        textarea = self.element.find(self.locator.by_id(ArenaElements.TEXTAREA_ID))
        logging.log(logging.INFO, "Sending the message...")
        # write the message
        ActionChains(self.driver).move_to_element(textarea).click().send_keys(message).perform()
        ActionChains(self.driver).move_to_element(textarea).click().send_keys(Keys.ENTER).perform()
        # wait to genreate response
        logging.log(logging.INFO, "Waiting for the response...")
        sleep(5)
        WebDriverWait(self.driver, ArenaElements.WAIT_DURATION).until(EC.element_to_be_clickable((By.ID, ArenaElements.CLEAR_HISTORY)))
        sleep(1)
        logging.log(logging.INFO, "Got Response...")
    
    def scrape_data(self, splitter_text:str| None = None)-> list[str]:
        '''Scrape the data from the website'''
        page_source = self.driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        text = soup.text.split(ArenaElements.SPLITER_TEXT_1)[-1]
        text = text.split(ArenaElements.SPLITER_TEXT_2)[0]
        if splitter_text:
            return text.split(splitter_text)
        return [text]


    def run(self, message:str, splitter_text:str| None = None) -> list[str]:
        '''Scrape the data from the website'''

        self.init()
        if self.check_page():
            self.go_to_arena()
            sleep(1)
            self.select_model()
            sleep(1)       
            self.genreate_response(message)
            sleep(1)
            data = self.scrape_data(splitter_text)
        
        self.driver.quit()
        return data
