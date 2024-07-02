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
import tools
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

    def clean_text(self, text: str) -> list[str]:
        cleaned_text = re.sub(
        r'[\uD800-\uDBFF][\uDC00-\uDFFF]',
        lambda m: f'\\u{ord(m.group()):04x}',
        text)
        return json.loads(cleaned_text)

    def generate(self, ele: dict) -> list[str]:
        '''Generate the response for each row'''
        
        if int(ele['winner_model_a']) == 1:
            correct_label = 'A'
        elif int(ele['winner_model_b']) == 1:
            correct_label = 'B'
        else:
            correct_label = 'AB'

        message = self.create_prompt(ele['prompt'], ele['response_a'], ele['response_b'], correct_label)
        response = self.scraper.run(message, "Output:")
        if response is None:
            return None
        return response[-1]

    
    def run(self, num_of_iteratios: int):
        try:
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
                response = self.generate(row)
                
                if response is None:
                    continue
                
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