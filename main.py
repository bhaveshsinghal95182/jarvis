from ai_models.jarvis_ai import jarvis_reply
from ai_models.intent_ai import intention
from speech.SpeechToText import Speech_to_text
from speech.TextToSpeech import speak_text
from colorama import Fore, init
from workflow import *

init(autoreset=True)


print(wish_me())