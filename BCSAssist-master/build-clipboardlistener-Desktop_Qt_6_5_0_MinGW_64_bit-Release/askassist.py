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
count: int = 0
previous_question: tuple = ()
updated_previous: list[tuple] = list(())

# Get the current working directory
current_directory = os.getcwd()

# Name of the executable file
executable_name = 'clipboardlistener.exe'

filename = 'timestamp.txt'

filepath = os.path.join(current_directory, filename)
executable_path = os.path.join(current_directory, executable_name)

"""
# if the above file paths dont work past the your absolute path here
executable_path = r"C:\Code\askbcs\BCSAssist-master (1)\BCSAssist-master\build-clipboardlistener-Desktop_Qt_6_5_0_MinGW_64_bit-Release\clipboardlistener.exe"
filepath = r"C:\Code\askbcs\BCSAssist-master (1)\BCSAssist-master\build-clipboardlistener-Desktop_Qt_6_5_0_MinGW_64_bit-Release\timestamp.txt"
"""

def read_last_line_simple():
    with open(filepath, 'r') as file:
        lines = file.readlines()
        line = ""
        if lines:
            line = lines[-1].strip()
        return line

#click refresh button
def refresh():
    pyautogui.moveTo(*refresh_position,1)
    pyautogui.click(*refresh_position)
    time.sleep(5)

#extract previous question
def extract_previous():
    time.sleep(3)  # only for testing
    pyautogui.moveTo(*start_position,1)
    pyautogui.mouseDown()
    pyautogui.moveTo(*end_position, duration=1)
    pyautogui.mouseUp()
    pyautogui.hotkey('ctrl', 'c')
    time_updated = read_last_line_simple()
    question = pyperclip.paste()
    return str(question), str(time_updated)

#gets current time
def get_time():
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    return time_string

# Define a cleanup function that terminates the subprocess
def cleanup(process):
    try:
        if process.poll() is None:  # Check if the process is still running
            process.terminate()  # Send SIGTERM
            process.wait(timeout=5)  # Wait for the process to terminate
            if process.poll() is None:  # If still running, force kill
                process.kill()
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Signal handler for graceful exits
def signal_handler(sig, frame):
    print('Script is being terminated!')
    if process is not None:
        cleanup(process)
    sys.exit(0)

# Ensure the timestamp.txt file is empty before use
with open(filepath, 'w') as file:
    pass  # Opening in 'w' mode and closing it immediately clears the file.

process = None

try:
    process = subprocess.Popen([executable_path])

    print("Make sure you have the following set up: ")
    print("\t1. An instance of chrome running AskBCS")
    print("\t2. The instance of chome should be zoomed in 100%")
    print("\t3. Only two open windows. The python environment and the chrome instance.")
    print("\t4. Make sure your pc is not still on mute from while you were watching porn.")

    time.sleep(5)  # use this time to make the askbsc browser the main window on the screen

    #change the window
    window = gw.getWindowsWithTitle('Google Chrome')[0]

    window.activate()  # Bring the window to the foreground

    pyautogui.hotkey('alt', 'tab')

    time.sleep(5)  # Wait for window switch to complete

    # extract the last resolved question
    previous_question = extract_previous()

    print(f"previous question : {previous_question}")
    print()

    # do the process every 1 minute for 4 hours
    for i in range(240):

        print(f"Iteration {i}")

        # refresh the queue
        refresh()
        print(f"Refreshed at: {get_time()}")

        current_question = extract_previous()

        # store the value of the last resolved question
        updated_previous.append(current_question)

        print(f"Stored value: {updated_previous[i][0]}")
        print(f"Timestamp: {updated_previous[i][1]}")

        qx, tx = updated_previous[i]
        qy, ty = updated_previous[i - 1]

        bool_test = tx == ty

        # if the value has changed, a new question has popped up below the ask-238742
        if updated_previous[i][0] != previous_question[0]:
            for j in range(5):
                winsound.Beep(5000, 2000)
                time.sleep(0.5)
            print("The values are different, there is a new question")
            print()
            break
        elif updated_previous[i][0] == previous_question[0] and len(updated_previous) > 1 and bool_test:
            for j in range(5):
                winsound.Beep(5000, 2000)
                time.sleep(0.5)
            print("The values are different, there is a new question")
            print()
        elif updated_previous[i][0] == previous_question[0] and len(updated_previous) == 1 and \
                updated_previous[i][1] == previous_question[1]:
            for j in range(5):
                winsound.Beep(5000, 2000)
                time.sleep(0.5)
            print("The values are different, there is a new question")
            print()
        else:
            print("The values are the same, no new question")
            print()

        time.sleep(48)

    process.terminate()

    # Wait for a short time to allow the subprocess to terminate gracefully
    process.wait(timeout=5)

    print(process.poll())

    # If the subprocess is still running, use SIGKILL to forcefully terminate it
    if process.poll() is None:
        process.kill()

    print(process.poll())

except FileNotFoundError:
    print("Executable not found. Please provide the correct path.")
except Exception as e:
    print("An error occurred:", e)
finally:
    if process is not None:
        cleanup(process)
