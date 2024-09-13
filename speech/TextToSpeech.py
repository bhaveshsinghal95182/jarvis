import pyttsx3
from colorama import Fore

def speak_text(text: str, voice_id: str = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0'):
    """
    Convert the input text to speech using the specified voice ID.
    
    :param text: The text to be spoken.
    :param voice_id: The ID of the voice to be used (default is DAVID voice).
    """
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set the voice using the voice ID
    engine.setProperty('voice', voice_id)

    # Print the text first
    print(f'{Fore.GREEN}Jarvis: {text}')

    # Speak the text
    engine.say(text)
    engine.runAndWait()


