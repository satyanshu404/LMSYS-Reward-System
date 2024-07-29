from dataclasses import dataclass, field

@dataclass
class ResponseGeneratorConstants:
    FILE_PATH:str = 'data/train-sliced-5000-20000-llama-3.1.csv'
    START: int = 0
    NUM_ROWS: int = 18598
    NUM_OF_ITERATIONS: int = 10
    ERROR_LIST: list = field(default_factory=lambda: ['API REQUEST ERROR', 
                                                      'NETWORK ERROR DUE TO HIGH TRAFFIC'])
    
@dataclass
class ThreadConstants:
    WAIT_DURATION: int = 300


@dataclass
class CreateDataConstants:
    DEFAULT_FILE_PATH:str = 'data/train.csv'
    SLICE: str = '5000:20000'
    MAX_TEXT_SIZE: int = 4500
    DEFAULT_VALUE: str = 'No Value'
    OUTPUT_FILE_PATH: str = 'data/train-sliced-' + '-'.join(SLICE.split(':')) + '.csv'