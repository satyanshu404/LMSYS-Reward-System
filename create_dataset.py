import pandas as pd
import constants as c
import json
import re
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CreateData:
    def __init__(self):
        self.df = pd.read_csv(c.CreateDataConstants.DEFAULT_FILE_PATH)
        self.slice_obj = slice(*map(int, c.CreateDataConstants.SLICE.split(':')))
        pass

    def slice_data(self):
        df = self.df.iloc[self.slice_obj]
        logging.log(logging.INFO, f"Dataframe shape: {df.shape}")
        return df

    def clean_text(self, text: str) -> list[str]:
        cleaned_text = re.sub(
            r'[\uD800-\uDBFF][\uDC00-\uDFFF]',
            lambda m: f'\\u{ord(m.group()):04x}',
            text
        )
        return json.loads(cleaned_text)

    def split_lists(self, row):
        prompts = self.clean_text(row['prompt'])
        response_as = self.clean_text(row['response_a'])
        response_bs = self.clean_text(row['response_b'])
        # response = clean_text(row['response'])
        
        new_rows = []
        for prompt, response_a, response_b in zip(prompts, response_as, response_bs):
            new_row = row.copy()
            new_row['prompt'] = prompt
            new_row['response_a'] = response_a
            new_row['response_b'] = response_b
            new_rows.append(new_row)
        
        return pd.DataFrame(new_rows)
    
    def chunk_text(self, text):
    # Initialize the text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=c.CreateDataConstants.MAX_TEXT_SIZE,  # desired chunk size
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

        # Split the text
        chunks = text_splitter.split_text(text)

        return chunks[0]
    
    def apply_chunk_text(self, row):
        row['prompt'] = self.chunk_text(row['prompt'])
        row['response_a'] = self.chunk_text(row['response_a'])
        row['response_b'] = self.chunk_text(row['response_b'])
        return row
    
    
    def create_dataset(self):
        try:
            df = self.slice_data()

            split_df = pd.concat([self.split_lists(row) for _, row in df.iterrows()], ignore_index=True)
            split_df = split_df.replace(r'^\s*$', 'No Value Provided', regex=True).fillna('No Value Provided')
            split_df = split_df.apply(self.apply_chunk_text, axis=1)
            split_df['response'] = c.CreateDataConstants.DEFAULT_VALUE
            split_df.to_csv(c.CreateDataConstants.OUTPUT_FILE_PATH, index=False)
            logging.log(logging.INFO, f"Dataset created and saved at {c.CreateDataConstants.OUTPUT_FILE_PATH}")
        except Exception as e:
            logging.log(logging.ERROR, f"Error in creating dataset: {e}")

if __name__ == '__main__':
    cd = CreateData()
    cd.create_dataset()