# Imports
import os
import pyautogui
import time
import keyboard
from pynput import keyboard

#time.sleep(2)

def on_press(key):
        try:
            pass
        except AttributeError:
            pass


def on_release(key):
    if key == keyboard.Key.space:
        im = pyautogui.screenshot(region=(0,53,600,600))
        im.save("./screen.png") 
    if key == keyboard.Key.esc:
        # Stop listener
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    pass