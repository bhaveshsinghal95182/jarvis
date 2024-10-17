import cv2
from PIL import ImageGrab
import pyperclip
import pyautogui as gui
import datetime
import datetime
import psutil
import webbrowser
from ai_models.img_ai import *
import json
import requests
import base64

web_cam = cv2.VideoCapture(0)

def take_screenshot():
    path = 'screenshot.jpg'
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=100)

def webcam_capture():
    if not web_cam.isOpened():
        print('Error: Camera did not open successfully')
        exit()
    
    path = 'webcam.jpg'
    ret, frame = web_cam.read()
    cv2.imwrite(path, frame)

def get_clipboard():
    clipboard_content = pyperclip.paste()
    if isinstance(clipboard_content, str):
        return clipboard_content
    else:
        print('No clipboard text to copy')
        return None
    

def get_battery_status():
    """Returns the current battery status as a string."""
    battery = psutil.sensors_battery()
    battery_percent = battery.percent
    plugged = battery.power_plugged
    
    if plugged:
        charging_status = "The laptop is plugged in and charging."
    else:
        charging_status = "The laptop is running on battery."

    return f"The battery is at {battery_percent}% capacity. {charging_status}"

def wish_me():
    """Returns a greeting based on the current time, date, and battery status."""
    # Get current date and time
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    # Get battery status
    battery_status = get_battery_status()

    # Determine greeting based on the current time
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    elif 17 <= hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good night"

    # Combine all the information
    statement = (
        f"{greeting}! The current date is {current_date} and the time is {current_time}. "
        f"{battery_status}"
    )

    return statement

def open_website_default(url):
    """Opens a website in the default web browser."""
    try:
        webbrowser.open(url)
        return 'done'
    except Exception as e:
        print(e)
        return False

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def vision_brain(encoded_image, prompt):
    url = "https://api.deepinfra.com/v1/openai/chat/completions"

    headers = {
        "accept": "text/event-stream",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        "x-deepinfra-source": "model-embed"
    }

    payload = {
        "model": "llava-hf/llava-1.5-7b-hf",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # Convert the payload to JSON
    payload_json = json.dumps(payload)

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload_json)

    # Check if the request was successful
    if response.status_code == 200:
        response_str = response.content.decode('utf-8')
        data = json.loads(response_str)
        answer = data['choices'][0]['message']['content']
        return answer
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        return None

def is_Online(url = "https://www.google.com",timeout=5):
    try:
        response = requests.get(url,timeout=timeout)
        if response.status_code >= 200 and response.status_code<300:
            return True
    except requests.ConnectionError:
        return False