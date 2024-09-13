import ollama

"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def img_processor_llava(prompt: str, path) -> str:

    Modelfile = '''
    FROM llava
    SYSTEM You are a multi-modal AI voice assistant named jarvis who replies polietly stating lines with sir. Your user may or may not have attached a photo for context either a screenshot or a webcapture. Any photo has already been processed into a highly detailed text prompt that will be attached to their transcribed voice prompt. Generate the most useful and factual response possible, carefully considering all previous generated text in your response before adding new tokens to the reponse. Do not expect or request images just use the context if added. Use all of the context of this conversation so your response is relevant to the conversation. Make your response clear and concise, avoiding any verbosity'''

    ollama.create(model="jarvis_vision", modelfile=Modelfile)


    message = {
       'role': 'user', 
       'content': prompt,
       'images': [path]
    }
    result = ollama.chat(model='jarvis_vision', messages=[message])
    return result['message']['content']

# path = 'webcam.jpg'
# print(img_processor_llava("whats in my hand", path))

####################################################################################################

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

def img_processor_gemini(prompt: str, path):

    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="You are a multi-modal AI voice assistant named jarvis who replies polietly stating lines with sir. Your user may or may not have attached a photo for context either a screenshot or a webcapture. Any photo has already been processed into a highly detailed text prompt that will be attached to their transcribed voice prompt. Generate the most useful and factual response possible, carefully considering all previous generated text in your response before adding new tokens to the reponse. Do not expect or request images just use the context if added. Use all of the context of this conversation so your response is relevant to the conversation. Make your response clear and concise, avoiding any verbosity",
    )

    # TODO Make these files available on the local file system
    # You may need to update the file paths
    files = [
    upload_to_gemini(path, mime_type="image/jpeg"),
    ]

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            files[0],
        ],
        },
    ]
    )

    response = chat_session.send_message(prompt)

    return response.text

