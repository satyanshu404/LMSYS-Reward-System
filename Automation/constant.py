from dataclasses import dataclass, field

@dataclass
class ScraperConstants:
    URL: str = 'https://chat.lmsys.org/'
    BROWSER: str = 'chrome'
    WINDOW_SIZE: tuple = (1, 1)

@dataclass
class FindElementConstants:
    WAIT_DURATION: int = 10
    SCRIPT: str = 'arguments[0].scrollIntoView(true);'

@dataclass
class AcceptAlertConstants:
    WAIT_DURATION: int = 30

@dataclass
class CheckPageConstants:
    TEXT: str = 'Arena (battle)'
    WAIT_DURATION: int = 10

@dataclass
class ArenaElements:
    TEXT: str = 'Arena (battle)'
    CHAT_ID: str = 'component-99-button'
    LISTBOX_ID: str = 'component-104'
    # MODEL_NAME: str = 'qwen2-72b-instruct' 
    # MODEL_NAME: str = 'nemotron-4-340b'
    # MODEL_NAME: str = 'gemma-2-27b-it'
    MODEL_NAME: str = 'llama-3.1-405b-instruct'
    # MODEL_NAME: str = 'llama-3.1-70b-instruct'
    TEXTAREA_ID: str = 'component-109'
    SUBMIT_BUTTON_ID: str = 'component-111'
    WAIT_DURATION: int = 60
    PROGRESS_ELEMENT: str = 'progress-text'
    BOT_ID: str = 'data-testid'
    BOT_ID_VALUE: str = 'bot'
    SPLITER_TEXT_1: str = 'Scroll down and start chatting'
    SPLITER_TEXT_2: str = 'Textbox'
    CLEAR_HISTORY: str = 'component-118'
    

