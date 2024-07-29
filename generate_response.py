import sys
import os
import re

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ast
import json
import pandas as pd
from constants import *
from Automation.script import LMSYSScraper
import pandas as pd
import tools
import threading
from prompt import prompt_template
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResponseGenerator:
    def __init__(self):
        self.scraper = LMSYSScraper()

    def load_data(self):
        '''Load the data from the csv file'''
        return pd.read_csv(ResponseGeneratorConstants.FILE_PATH)
    
    def create_prompt(self, query: str, response_a: str, response_b: str, correct_label: str) -> str:
        return prompt_template(query, response_a, response_b, correct_label)
    
    def find_label(self, ele:dict) -> str:
        '''Find the correct label for the response'''
        if int(ele['winner_model_a']) == 1:
            return 'A'
        elif int(ele['winner_model_b']) == 1:
            return 'B'
        return 'AB'
    
    def check_error(self, response: list[str]):
        '''Check if the response contains any error message'''
        for error in ResponseGeneratorConstants().ERROR_LIST:
            if error in response[-1]:
                self.scraper.cleanup()
                logging.log(logging.ERROR, f"{error}, Retrying...")
                return True
        return False
    
    def get_results(self, message: str, run_with_initialization:bool):
        result_container = {}
        if run_with_initialization:
            thread = threading.Thread(target=self.scraper.run_with_initialization, args=(message, result_container))
        else:
            thread = threading.Thread(target=self.scraper.run, args=(message, result_container))
        thread.start()
        thread.join(ThreadConstants.WAIT_DURATION)
        
        if thread.is_alive():
            logging.log(logging.ERROR, f"Script exceeded the time limit of {ThreadConstants.WAIT_DURATION}, Terminating...")
            self.scraper.cleanup()
            return None
        
        return result_container.get('result', None)
    
    def generate(self, ele: dict, run_with_initialization:bool) -> list[str]:
        '''Generate the response for each row'''
        
        correct_label = self.find_label(ele)

        message = self.create_prompt(ele['prompt'], ele['response_a'], ele['response_b'], correct_label)
        response = self.get_results(message, run_with_initialization)
        
        if response is None:
            self.scraper.cleanup()
            return None
        if self.check_error(response):
            return None
        
        return response[-1]

    
    def run(self, num_of_iteratios: int):
        try:
            run_with_initialization = True
            iteration_count = 0
            logging.log(logging.INFO, "Generating responses...")
            df = self.load_data()

            index = ResponseGeneratorConstants.START
            end_index = ResponseGeneratorConstants.NUM_ROWS + ResponseGeneratorConstants.START

            while index <= end_index:
                row = df.iloc[index]

                if row['response'] != 'No Value':
                    index += 1
                    continue

                logging.log(logging.INFO, f"Generating response for row {index}...")
                response = self.generate(row, run_with_initialization)
                
                if response is None:
                    run_with_initialization = True
                    continue
                if iteration_count > 100:
                    self.scraper.cleanup()
                    run_with_initialization = True
                    iteration_count = 0

                run_with_initialization = False
                iteration_count += 1
                # print(f"{index}: {response}")
                df.at[index, 'response'] = response                    
                df.to_csv(ResponseGeneratorConstants.FILE_PATH, index=False)

                logging.log(logging.INFO, f"Response generated for row {index} successfully!")
                index += 1
            logging.log(logging.INFO, "All Responses generated successfully!")
        
        except Exception as e:
            num_of_iteratios += 1
            logging.log(logging.ERROR, f"Error in generating responses: {e}")
            
            if num_of_iteratios < ResponseGeneratorConstants.NUM_OF_ITERATIONS:
                logging.log(logging.INFO, f"Trying again...{num_of_iteratios}")
                self.run(num_of_iteratios)
        


if __name__ == '__main__':
    generator = ResponseGenerator()
    num_of_iteratios: int = 0
    generator.run(num_of_iteratios)