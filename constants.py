from dataclasses import dataclass, field

@dataclass
class ResponseGeneratorConstants:
    # FILE_PATH: str = 'data/small-train-gpt-4o-2024-05-13_1.csv'
    FILE_PATH:str = 'data/small-train-nemotron-4-340b_1.csv'
    START: int = 17
    NUM_ROWS: int = 30