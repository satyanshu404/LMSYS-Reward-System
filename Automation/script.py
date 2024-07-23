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
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from time import sleep
import pyperclip
from Automation.constant import *
from bs4 import BeautifulSoup
import Automation.tools as tools
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LMSYSScraper:
    def __init__(self):
        '''Initialize the scraper'''
        self.locator = tools.Locator()

    def initialize(self):
        try:
            options = uc.ChromeOptions()
            options.add_argument("--disable-gpu")
            # options.headless = True
            self.driver = uc.Chrome(options=options)
            self.element = tools.FindElement(self.driver)
            sleep(0.2)
            self.driver.get(ScraperConstants.URL)
            self.alert = tools.AcceptAlert(self.driver).accept()
        except Exception as e:
            self.cleanup()
            print(f"Error initializing the driver: {e}")

    # def initialize(self):
    #     '''Initialize the driver'''
    #     options = webdriver.ChromeOptions() 
    #     options.add_argument("--disable-gpu")       
    #     self.driver = uc.Chrome(options=options)
    #     self.element = tools.FindElement(self.driver)
    #     self.driver.get(ScraperConstants.URL)
    #     self.alert = tools.AcceptAlert(self.driver).accept()

    def check_page(self):
        '''Check the correct page'''
        try:
            logging.log(logging.INFO, "Checking the page...")
            WebDriverWait(self.driver, CheckPageConstants.WAIT_DURATION).until(
                EC.presence_of_element_located(self.locator.by_text(CheckPageConstants.TEXT))
            )
            logging.log(logging.INFO, "Page loaded successfully")
            sleep(0.5)
            return True
        except Exception as e:
            logging.log(logging.ERROR, f"Couldn't load the page: {e}")
            return False
        
    def go_to_arena(self):
        '''Go to the arena page'''
        logging.log(logging.INFO, "Going to the arena page...")
        # Click on the chat button
        sleep(0.5)
        self.element.find(self.locator.by_id(ArenaElements.CHAT_ID)).click()
        return
    
    def is_element_present(self, locator:tuple) -> bool:
        try:
            self.driver.find_element(locator[0], locator[1])
            return True
        except NoSuchElementException:
            return False

    def select_model(self):
        '''Select the model from the listbox'''
        listbox = self.element.find(self.locator.by_id(ArenaElements.LISTBOX_ID))
        ActionChains(self.driver).move_to_element(listbox).click().send_keys(Keys.BACKSPACE*150).perform()
        ActionChains(self.driver).move_to_element(listbox).click().send_keys(ArenaElements.MODEL_NAME).perform()
        ActionChains(self.driver).move_to_element(listbox).click().send_keys(Keys.ENTER).perform()
    
    def genreate_response(self, message: str):
        '''Generate the response for the given message'''
        # message = message.replace("\n", "\\n")
        pyperclip.copy(message)
        # Select textarea 
        textarea = self.element.find(self.locator.by_id(ArenaElements.TEXTAREA_ID))
        logging.log(logging.INFO, "Sending the message...")
        # write the message
        write_action = ActionChains(self.driver).move_to_element(textarea).click()
        write_action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        sleep(0.5)
        ActionChains(self.driver).move_to_element(textarea).click().send_keys(Keys.ENTER).perform()
        # wait to genreate response
        logging.log(logging.INFO, "Waiting for the response...")
        sleep(1)
        if self.log_error():
            return False
        WebDriverWait(self.driver, ArenaElements.WAIT_DURATION).until(EC.element_to_be_clickable((By.ID, ArenaElements.CLEAR_HISTORY)))
        logging.log(logging.INFO, "Got Response...")
        return True
    
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
    
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.close()
            self.driver.quit()
            del self.driver

    def cleanup(self):
        if hasattr(self, 'driver'):
            self.driver.close()
            self.driver.quit()
            del self.driver

    def log_error(self):
        '''Check for timeout error'''
        if self.is_element_present((By.CLASS_NAME, "error")):
            logging.error("Timeout Error Occured. Retrying...")
            self.cleanup()
            return True
        return False

    def run(self, message: str, splitter_text: str | None = None, result_container: dict = None):
        '''Scrape the data from the website'''

        self.initialize()

        # check if the page is loaded successfully
        if not self.check_page():
            self.cleanup()
            result_container['result'] = None
            return

        self.go_to_arena()
        sleep(0.3)

        # check for timeout error
        if self.log_error():
            result_container['result'] = None
            return

        self.select_model()
        sleep(0.3)

        # check for timeout error
        if self.log_error():
            result_container['result'] = None
            return

        if self.genreate_response(message):
            data = self.scrape_data(splitter_text)
            self.cleanup()
            result_container['result'] = data
            return
        
        result_container['result'] = None
        return
        
        
            
