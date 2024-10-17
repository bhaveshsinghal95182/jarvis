import ollama


def intention(prompt: str) -> str:

    
    Modelfile = '''
        FROM llama3.2
        SYSTEM You are an AI function calling model. You will determine whether extracting the users clipboard content, taking a screenshot, capturing the webcam or calling no function is best for a voice assistant to respond to the users prompt. The webcam can be assumed to be normal laptop webcam facing the user. You will respond with only one selection from this list : ["extract clipboard", "take screenshot", "capture webcam", "general query", "greeting", "open app"]. Do not respond with anything but the most logical selection from that list with no explanation. Format the function call name exactly as I listed. If the content is inappropriatte then reply according to the sense of the rest of the text omitting the inappropriate words.
        PARAMETER temperature 0.9
        '''

    ollama.create(model="jarvis", modelfile=Modelfile)

    message = {'role': 'user', 
               'content': prompt}
    result = ollama.chat(model='jarvis', messages=[message])
    return result['message']['content']
