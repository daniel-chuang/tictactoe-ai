# Imports
import os
import pyautogui
import time

time.sleep(1)

im = pyautogui.screenshot(region=(0,53,600,600))
im.save("./screen.png")