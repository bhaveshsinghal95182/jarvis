from ai_models.jarvis_ai import jarvis_reply
from speech.SpeechToText import Speech_to_text
from colorama import Fore, init

init(autoreset=True)


while True:
    user = Speech_to_text()
    print(f'{Fore.GREEN}{jarvis_reply(user)}')
    