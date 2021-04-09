"""
Tictactoe toe canvas always spawns in at (0, 53), (600, 600)

RGB System --> BGR System (from Pygame to cv2)
Player 1 color: (255, 0, 0) --> (0, 0, 255)
Player 2 color: (0, 0, 255) --> (255, 0, 0)
Player 1 cursor color: (150, 0, 0) --> (0, 0, 150)
Player 2 cursor color: (0, 0, 150) --> (150, 0, 0)
"""

# Imports
import os
import pyautogui
import time
from pynput import keyboard
import cv2
import numpy as np

# Set constants
BLOCKSIZE = 200
BLOCKRED = (0, 0, 255)
BLOCKBLUE = (255, 0, 0)
BLOCKBLACK = (0, 0, 0)
CURSORRED = (0, 0, 150)
CURSORBLUE = (150, 0, 0)
colorBlockMatrixConversion = {BLOCKBLACK: 0, BLOCKRED: 1, BLOCKBLUE: 2}

# Makes a class for information
class Info():
    def __init__(self, filename: str, matrix, image, imgarray, cursorx: int, cursory: int):
        self.image = image
        self.imgarray = cv2.imread(filename)
        self.matrix = matrix
        self.x = x
        self.y = y

# Set broadcasting for when the computer presses space

def on_press(key):
        try:
            pass
        except AttributeError: 
            pass

def on_release(key):
    # When space is pressed
    if key == keyboard.Key.space:
        # Take and save screenshot
        im = pyautogui.screenshot(region=(0,53,600,600))
        im.save("./screen.png") 
        img = cv2.imread("./screen.png")

        # Make imgarray with opencv representing board
        imgarray = np.zeros(9).reshape(3, 3)
        for x in range(1, 4):
            for y in range(1, 4):
                imgarray[y - 1, x - 1] = colorBlockMatrixConversion[tuple(img[y * BLOCKSIZE - 20, x * BLOCKSIZE - 20])]
        print(imgarray)

    # When arrow keys are pressed
    if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
        # Take and save screenshot
        im = pyautogui.screenshot(region=(0,53,600,600))
        im.save("./screen.png") 
        img = cv2.imread("./screen.png")

        # Find coordinates for cursor
        for x in range(1, 4):
            for y in range(1, 4):
                if tuple(img[y * BLOCKSIZE - int(BLOCKSIZE/2), x * BLOCKSIZE - int(BLOCKSIZE/2)]) == CURSORRED:
                    cursorx, cursory = x - 1, y - 1
        print("X:", cursorx, "| Y:", cursory)

    # When escape is pressed
    if key == keyboard.Key.esc:
        # Stop listener
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    pass