import cv2
from PIL import ImageGrab
import pyperclip
import pyautogui as gui
import datetime
import datetime
import psutil
import webbrowser
from ai_models.img_ai import *

web_cam = cv2.VideoCapture(0)

def take_screenshot():
    path = 'screenshot.jpg'
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=60)

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
    webbrowser.open_new(url)

def open_website_in_browser(browser_name, url):
    """Opens a website in a specified web browser."""
    try:
        # Define paths to custom browsers if necessary
        browser_paths = {
            'brave': "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            'arc': '/path/to/arc-browser'       # Change this to the correct path
        }
        
        # Register the browser if it's a custom one
        if browser_name in browser_paths:
            webbrowser.register(browser_name, None, webbrowser.BackgroundBrowser(browser_paths[browser_name]))
        
        # Get the browser controller and open the URL
        webbrowser.get(browser_name).open(url)
    except webbrowser.Error as e:
        print(f"An error occurred: {e}")

def reply_screenshot(prompt: str) -> str:
    # try:
    #     response = img_processor_gemini(prompt=prompt, path='screenshot.jpg')
    # except:
    response = img_processor_llava(prompt=prompt, path='screenshot.jpg')
    tool_history = []

