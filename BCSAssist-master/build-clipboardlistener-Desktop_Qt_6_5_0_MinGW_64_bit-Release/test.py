import pyperclip
import pyautogui
import time
import winsound
from datetime import datetime
import subprocess
import os
import signal
import sys
import pygetwindow as gw

refresh_position = 1271, 279
start_position = 430, 513
end_position = 515, 513

# Get a list of all open windows
windows = gw.getAllTitles()

# Print the titles of all open windowss
for window in windows:
    print(window)

window = gw.getWindowsWithTitle('Google Chrome')[0]

window.activate()  # Bring the window to the foreground

pyautogui.hotkey('alt','tab')

time.sleep(5)

def extract_previous():
    time.sleep(3)  # only for testing
    pyautogui.moveTo(*start_position)
    time.sleep(60)
    pyautogui.moveTo(*end_position, duration=1)


extract_previous()

print("moved")