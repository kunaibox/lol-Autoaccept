import time
import pyautogui
import json
import tkinter as tk
import keyboard
from datetime import datetime


# Define debouncer
on = False
window_closed = False
clicking = False  # Variable to track clicking state

# Function to toggle the "on" variable
def toggle():
    global on
    on = not on
    update_text()
def onhotkey(e):
    toggle()

# Function to update the label text based on the "on" variable
def update_text():
    if on:
        status_label.config(text="Accepting", fg="green")
        start_clicking()  # Start clicking when "on" is True
    else:
        status_label.config(text="Idle", fg="white")
        stop_clicking()   # Stop clicking when "on" is False

# Callback function to handle window closing
def on_closing():
    global window_closed, loop
    window_closed = True
    loop = False  # Set the loop flag to False to exit the main loop
    root.destroy()

def guix():
    global status_label, root

    root = tk.Tk()
    root.title("")

    # Set the background color to black
    root.configure(bg="black")

    # Set minimum size to allow moving the window
    root.minsize(200, 100)

    # Disable window resizing
    root.resizable(False, False)
    icon = tk.PhotoImage(file="icon.png")  # Replace with your image file path

    # Set the custom icon
    root.iconphoto(True, icon)
    # Create and configure a label for status text
    status_label = tk.Label(root, text="", font=("Helvetica", 16), bg="black")
    status_label.pack(pady=20)
    update_text()

    # Create a button to toggle the "on" variable
    toggle_button = tk.Button(root, text="Toggle", command=toggle, bg="black", fg="white")
    toggle_button.pack()
    root.attributes('-topmost', True)
    # Bind the window close event to on_closing function
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the periodic task to check the "on" variable and perform clicking
    root.after(1000, check_on_and_click)

    # Start the main loop
    root.mainloop()

# json config reader and interpreter
with open('config.json', 'r') as json_file:
    config_data = json.load(json_file)


gui_enabled = config_data["gui"]
hotkey_enabled = config_data["hotkey"]["enabled"]
hotkey_button = config_data["hotkey"]["button"]

if hotkey_enabled:
    keyboard.on_press_key(hotkey_button, onhotkey)
# Setup for clicker
image_path = "accept.png"  # Couldnt get my screenshots to work so I used the one https://github.com/matiasperz uploaded

confidence_threshold = 0.6

# Function for clicker
def click_image(image_path, confidence_threshold):
    global on
    screenshot = pyautogui.screenshot()
    location = pyautogui.locateOnScreen(image_path, confidence=confidence_threshold)
    if location is not None:
        center_x, center_y = pyautogui.center(location)
        pyautogui.click(center_x, center_y)
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        print("Accepted at", time)
        on = False
        update_text()
        stop_clicking()

def start_clicking():
    global clicking
    clicking = True

def stop_clicking():
    global clicking
    clicking = False

def check_on_and_click():
    if clicking and on:
        click_image(image_path, confidence_threshold)
    if not window_closed:
        root.after(1000, check_on_and_click)

def hotkey():
    toggle()
# Main intro
print("""
     _                      _           _   _   ___   
    / \   ___ ___ ___ _ __ | |_ ___  __| | / | / _ \  
   / _ \ / __/ __/ _ \ '_ \| __/ _ \/ _` | | || | | | 
  / ___ \ (_| (_|  __/ |_) | ||  __/ (_| | | || |_| | 
 /_/   \_\___\___\___| .__/ \__\___|\__,_| |_(_)___/  
                     |_|                              
                                                                           
https://github.com/kunaibox
""")
time.sleep(1)
print("Config loaded")
time.sleep(0.5)
print("GUI Enabled:", gui_enabled)
print("Hotkey Enabled:", hotkey_enabled)
print("Hotkey Button:", hotkey_button)
print("""
      
""")

# Main loop GUI non-GUI (GUI and overlay in the same)
loop = True
while loop:
    if gui_enabled:
        guix()
        if window_closed:
            exit()
