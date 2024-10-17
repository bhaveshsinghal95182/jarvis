from ai_models.jarvis_ai import jarvis_reply
from speech.SpeechToText import Speech_to_text
from speech.TextToSpeech import Co_speak
from workflow import *
import ollama
import streamlit as st
import threading


st.set_page_config(page_title="Jarvis Command Center", layout="centered")

dark_mode_css = """
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
        }
        .stTextInput > div > div > input {
            background-color: #333333;
            color: white;
        }
        .stButton > button {
            background-color: #333333;
            color: white;
        }
    </style>
    """
st.markdown(dark_mode_css, unsafe_allow_html=True)

st.title("This is a GUI for Jarvis")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': 
            prompt}],

        tools=[
        {
            "type": "function",
            "function": {
                "name": "take_screenshot",
                "description": "Takes a screenshot and saves it as a JPEG file.",
                "parameters": {
                "type": "object",
                "properties": {},
                "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "webcam_capture",
                "description": "Captures webcam and saves it as jpg file",
                "parameters": {
                "type": "object",
                "properties": {},
                "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "wish_me",
                "description": "Returns a greeting based on the current time, date, and battery status.",
                "parameters": {
                "type": "object",
                "properties": {},
                "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "jarvis_reply",
                "description": "Returns a reply about general queries with the personality of jarvis based on the question",
                "parameters": {
                "type": "object",
                "properties": {},
                "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "open_website_default",
                "description": "Opens a website in the default web browser.",
                "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "return the url for the site user wants to open as url.com"
                    }
                },
                "required": ["url"]
                }
            }
        },
    ],
    )

    if response["message"].get("tool_calls"):
        # print(f"\nThe model used some tools")
        available_functions = {
            "take_screenshot": take_screenshot,
            "wish_me": wish_me,
            "webcam_capture": webcam_capture,
            "jarvis_reply": jarvis_reply,
            "open_website_default": open_website_default
        }
        # print(f"\navailable_function: {available_functions}")
        for tool in response["message"]["tool_calls"]:
            # print(f"available tools: {tool}")
            function_to_call = available_functions[tool["function"]["name"]]
            print(f"function to call: {function_to_call}")

            if function_to_call == take_screenshot:
                take_screenshot()
                if is_Online():
                    encoding = encode_image_to_base64("screenshot.jpg")
                    function_response2 = vision_brain(encoding, prompt)
                else:
                    function_response2 = img_processor_llava(prompt, "screenshot.jpg")
                Co_speak(f"{function_response2}")
                continue
            elif function_to_call == webcam_capture:
                webcam_capture()
                if is_Online():
                    encoding = encode_image_to_base64("screenshot.jpg")
                    function_response2 = vision_brain(encoding, prompt)
                else:
                    function_response2 = img_processor_llava(prompt, "screenshot.jpg")
                Co_speak(f"{function_response2}")
                continue
            elif function_to_call == jarvis_reply:
                function_response2 = jarvis_reply(prompt)
                Co_speak(f"{function_response2}")
                continue
            elif function_to_call == open_website_default:
                function_response2 = function_to_call(
                    tool["function"]["arguments"]["url"]
                )
                Co_speak(f"{function_response2}")
                continue

            function_response1 = function_to_call()
            function_response2 = jarvis_reply(f"user: {prompt}, assistant: {function_response1}")
            Co_speak(f"{function_response2}")

        st.session_state.messages.append({"role": "assistant", "content": function_response2})
        st.chat_message("assistant").write(function_response2)

