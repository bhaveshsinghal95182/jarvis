import asyncio
from ollama import AsyncClient
import pyttsx3
import threading

async def chat():
    message = {'role': 'user', 'content': 'Why is the sky blue?'}
    result = AsyncClient().chat(model='phi3', messages=[message], stream=True)
    collected_parts = []
    
    async for part in await result:
        print(part['message']['content'], end='', flush=True)
        collected_parts.append(part['message']['content'])
    
    full_message = ''.join(collected_parts)
    return full_message

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

async def main():
    # Run the chat function and get the result
    full_message = await chat()
    
    # Use pyttsx3 to convert text to speech in a separate thread
    tts_thread = threading.Thread(target=text_to_speech, args=(full_message,))
    tts_thread.start()
    tts_thread.join()

# Run the main function
asyncio.run(main())
