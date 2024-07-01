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
    
    def create_prompt(self, query: str, response_a: str, response_b: str):
        return prompt_template(query, response_a, response_b)

    def clean_text(self, text: str) -> list[str]:
        cleaned_text = re.sub(
        r'[\uD800-\uDBFF][\uDC00-\uDFFF]',
        lambda m: f'\\u{ord(m.group()):04x}',
        text)
        return json.loads(cleaned_text)

    def generate(self, ele: dict) -> list[str]:
        '''Generate the response for each row'''
        message = self.create_prompt(ele['prompt'], ele['response_a'], ele['response_b'])
        return self.scraper.run(message, "Output:")[-1]

    
    def run(self):
        try:
            logging.log(logging.INFO, "Generating responses...")
            df = self.load_data()

            for index in range(ResponseGeneratorConstants.START, ResponseGeneratorConstants.NUM_ROWS + ResponseGeneratorConstants.START+1):
                row = df.iloc[index]

                if row['response'] != 'No Value':
                    continue
                logging.log(logging.INFO, f"Generating response for row {index+1}...")
                df.at[index, 'response'] = self.generate(row)
                df.to_csv(ResponseGeneratorConstants.FILE_PATH, index=False)
                logging.log(logging.INFO, f"Response generated for row {index+1} successfully!")
            logging.log(logging.INFO, "Responses generated successfully!")
        except Exception as e:
            logging.log(logging.ERROR, f"Error in generating responses: {e}")


if __name__ == '__main__':
    generator = ResponseGenerator()
    generator.run()