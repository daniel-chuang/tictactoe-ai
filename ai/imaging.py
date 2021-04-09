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
from PIL import Image, ImageGrab
import mss
import mss.tools
import sys

bbox = {'top': 53, 'left': 0, 'width': 600, 'height': 600}
sct = mss.mss()

# Set constants
BLOCKSIZE = 200
BLOCKRED = (0, 0, 255)
BLOCKBLUE = (255, 0, 0)
BLOCKBLACK = (0, 0, 0)
CURSORRED = (0, 0, 150)
CURSORBLUE = (150, 0, 0)
colorBlockMatrixConversion = {BLOCKBLACK: 0, BLOCKRED: 1, BLOCKBLUE: 2}
SCREENSIZE = pyautogui.size()

# Polling
complete = False

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
        if pyautogui.size()[0] == 1440:
            im = sct.grab(bbox)
        else:
            im = sct.grab(bbox)
        mss.tools.to_png(im.rgb, im.size, output="screen.png")
        img = cv2.imread("screen.png")
        img = cv2.resize(img, (600, 600))

        # Make imgarray with opencv representing board
        imgarray = np.zeros(9).reshape(3, 3)
        for x in range(1, 4):
            for y in range(1, 4):
                try:
                    imgarray[y - 1, x - 1] = colorBlockMatrixConversion[tuple(img[y * BLOCKSIZE - 20, x * BLOCKSIZE - 20])]
                except:
                    print("Imaging complete!")
                    complete = True
                    return False
        print(imgarray)

    # When arrow keys are pressed
    if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]:
        # Take and save screenshot
        if pyautogui.size()[0] == 1440:
            im = sct.grab(bbox)
        else:
            im = sct.grab(bbox)
        mss.tools.to_png(im.rgb, im.size, output="screen.png")
        img = cv2.imread("screen.png")
        img = cv2.resize(img, (600, 600))

        # Find coordinates for cursor
        for x in range(1, 4):
            for y in range(1, 4):
                if tuple(img[y * BLOCKSIZE - int(BLOCKSIZE/2), x * BLOCKSIZE - int(BLOCKSIZE/2)]) == CURSORRED:
                    cursorx, cursory = x - 1, y - 1
                elif tuple(img[y * BLOCKSIZE - int(BLOCKSIZE/2), x * BLOCKSIZE - int(BLOCKSIZE/2)]) not in [(0,0,0), BLOCKRED, BLOCKBLUE]:
                    print("Imaging complete!")
                    complete = True
                    return False
        print("X:", cursorx, "| Y:", cursory)

    # When escape is pressed
    if key == keyboard.Key.esc:
        # Stop listener
        print("Imaging ended with esc")
        return False

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    pass