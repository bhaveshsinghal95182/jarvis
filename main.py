from ai_models.jarvis_ai import jarvis_reply
from speech.SpeechToText import Speech_to_text
from speech.TextToSpeech import speak_text
from colorama import Fore, init

init(autoreset=True)


while True:
    user = Speech_to_text()
    jarvis = jarvis_reply(user)
    speak_text(jarvis)
    
    