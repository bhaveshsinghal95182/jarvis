from ai_models.jarvis_ai import jarvis_reply
from ai_models.intent_ai import intention
from speech.SpeechToText import Speech_to_text
from speech.TextToSpeech import speak_text
from colorama import Fore, init

init(autoreset=True)


while True:
    user = Speech_to_text()
    intent = intention(user)

    if ("greeting" in intent) or ("general query" in intent):
        response = jarvis_reply(user)
        speak_text(response)
    else:
        print("something with intent")