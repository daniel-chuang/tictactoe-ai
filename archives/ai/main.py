# Imports
import os
from PIL import ImageGrab

# Allow for python game script to be run
os.system("chmod +x ../game/tictactoe_opponent.py")
os.system("python ../game/tictactoe_opponent.py & python imaging.py")