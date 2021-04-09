# Imports
import os
from PIL import ImageGrab

# Allow for python game script to be run
os.system("chmod +x ../game/tictactoe-opponent.py")
os.system("python ../game/tictactoe-opponent.py & python imaging.py")