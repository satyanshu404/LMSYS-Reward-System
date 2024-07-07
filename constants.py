from dataclasses import dataclass, field

@dataclass
class ResponseGeneratorConstants:
    # FILE_PATH: str = 'data/small-train-gpt-4o-2024-05-13_1.csv'
    # FILE_PATH:str = 'data/small-train-nemotron-4-340b_1.csv'
    # FILE_PATH:str = 'data/small-train-claude-3-opus-20240229_1.csv'
    FILE_PATH:str = 'data/small-train-qwen2-72b-instruct.csv'
    # START: int = 17
    START: int = 0
    NUM_ROWS: int = 658
    NUM_OF_ITERATIONS: int = 10
    ERROR_LIST: list = field(default_factory=lambda: ['API REQUEST ERROR', 
                                                      'NETWORK ERROR DUE TO HIGH TRAFFIC'])
    
@dataclass
class ThreadConstants:
    WAIT_DURATION: int = 299