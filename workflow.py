import cv2
from PIL import ImageGrab

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

webcam_capture()
take_screenshot()