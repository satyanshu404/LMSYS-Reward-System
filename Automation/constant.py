from dataclasses import dataclass, field

@dataclass
class ScraperConstants:
    URL: str = 'https://chat.lmsys.org/'
    BROWSER: str = 'chrome'

@dataclass
class FindElementConstants:
    WAIT_DURATION: int = 60
    SCRIPT: str = 'arguments[0].scrollIntoView(true);'

@dataclass
class AcceptAlertConstants:
    WAIT_DURATION: int = 60

@dataclass
class CheckPageConstants:
    TEXT: str = 'Arena (battle)'
    WAIT_DURATION: int = 60

@dataclass
class ArenaElements:
    TEXT: str = 'Arena (battle)'
    CHAT_ID: str = 'component-98-button'
    LISTBOX_ID: str = 'component-103'
    # MODEL_NAME: str = 'claude-3-opus-20240229'
    # MODEL_NAME:str = 'gpt-4o-2024-05-13'
    MODEL_NAME: str = 'nemotron-4-340b'
    TEXTAREA_ID: str = 'component-108'
    SUBMIT_BUTTON_ID: str = 'component-110'
    WAIT_DURATION: int = 300
    SPLITER_TEXT_1: str = 'Scroll down and start chatting'
    SPLITER_TEXT_2: str = 'Textbox'
    CLEAR_HISTORY: str = 'component-117'
    

