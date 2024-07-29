import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
            # self.driver.set_window_size(800, 1200)
            self.element = tools.FindElement(self.driver)
            sleep(0.2)
            self.driver.get(ScraperConstants.URL)
            self.alert = tools.AcceptAlert(self.driver).accept()
        except Exception as e:
            self.cleanup()
            logging.log(logging.ERROR, f"Error initializing the driver: {e}")


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
        sleep(0.2)
        write_action = ActionChains(self.driver).move_to_element(textarea).click()
        write_action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        sleep(0.2)
        ActionChains(self.driver).move_to_element(textarea).click().send_keys(Keys.ENTER).perform()
        # wait to genreate response
        logging.log(logging.INFO, "Waiting for the response...")
        sleep(0.5)
        if self.log_error():
            return False
        # wait until the progress element is present
        element_present = EC.presence_of_element_located((By.CLASS_NAME, ArenaElements.PROGRESS_ELEMENT))
        WebDriverWait(self.driver, 10).until(element_present)
        sleep(0.5)
        WebDriverWait(self.driver, ArenaElements.WAIT_DURATION).until(EC.element_to_be_clickable((By.ID, ArenaElements.CLEAR_HISTORY)))
        logging.log(logging.INFO, "Response Generated...")
        return True
    
    def scrape_data(self)-> list[str]:
        text = self.element.find(self.locator.by_element(ArenaElements.BOT_ID, ArenaElements.BOT_ID_VALUE)).text
        WebDriverWait(self.driver, ArenaElements.WAIT_DURATION).until(EC.element_to_be_clickable((By.ID, ArenaElements.CLEAR_HISTORY))).click()
        sleep(0.5)
        logging.log(logging.INFO, f"Got Response...")
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
    
    def run_with_initialization(self, message: str, result_container: dict = None):
        '''Scrape the data from the website with initialization'''

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
            data = self.scrape_data()
            # self.cleanup()
            result_container['result'] = data
            return
        
        self.cleanup()
        result_container['result'] = ['NA']
        return
    

    def run(self, message: str, result_container: dict = None):
        '''Scrape the data from the website'''

        # check for timeout error
        if self.log_error():
            result_container['result'] = None
            self.cleanup()
            return

        if self.genreate_response(message):
            data = self.scrape_data()
            result_container['result'] = data
            return
        
        self.cleanup()
        result_container['result'] = ['NA']
        return
        
        
            
