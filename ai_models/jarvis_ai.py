import ollama


def jarvis_reply(prompt: str) -> str:

    Modelfile = '''
    FROM phi3.5
    SYSTEM You are an AI assistant named jarvis who replies polietly stating lines with sir. Generate the most useful and factual response possible, carefully considering all previous generated text in your response before adding new tokens to the reponse. Use all of the context of this conversation so your response is relevant to the conversation. Make your response clear and concise, avoiding any verbosity'''

    ollama.create(model="jarvis", modelfile=Modelfile)

    message = {'role': 'user', 
               'content': prompt}
    result = ollama.chat(model='jarvis', messages=[message])
    return result['message']['content']

