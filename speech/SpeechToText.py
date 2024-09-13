import speech_recognition as sr
from mtranslate import translate
from colorama import Fore, init

init(autoreset=True)

def Translate_hindi_to_english(text):
    english_text = translate(text, "en-us")
    return english_text

def Speech_to_text() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source=source, duration=0.5)
        r.pause_threshold = 1
        r.phrase_threshold = 0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold = True
        r.operation_timeout = None
        r.non_speaking_duration = 0.5
        r.dynamic_energy_adjustment_ratio = 2
        r.dynamic_energy_adjustment_damping = 0.1
        r.energy_threshold = 4000
        r.phrase_time_limit = 10

        print(f"{Fore.LIGHTBLACK_EX}Listening.....", end='', flush=True)
        audio = r.listen(source)

        try:
            print(f"\r{Fore.LIGHTBLACK_EX}Recognizing....", end="", flush=True)
            recognize_text = r.recognize_google(audio).lower()
            if recognize_text:
                translated_text = Translate_hindi_to_english(recognize_text)
                print("\r" + Fore.BLUE + "Descentkatil: " + translated_text)
                return translated_text
            else:
                return ""
        except sr.UnknownValueError:
            print(f"\r{Fore.RED}Could not understand audio", flush=True)
            return "Could not understand audio"
        except sr.RequestError as e:
            print(f"\r{Fore.RED}Could not request results; {e}", flush=True)
            return f"Could not request results; {e}"
        finally:
            print("\r", end="", flush=True)