# Tictactoe AI Player

Demonstration video:
[Video](https://www.youtube.com/watch?v=aoQbNZRJz0U&feature=youtu.be)

# Instructions:
In order to run this project, you must first download this repository using the release of the project. Then you unzip it.

Change your terminal to the downloaded directory and run: 
> pip install -r requirements.txt

Then, you can run the project using the following command:
> python runner.py

This runs the game, which calls the AI to take the moves of the opposing player. You can click on the tictactoe squares to select which spots you want to claim.

# Files in archive
The files in archive are as such:
- main.py runs imaging.py and tictactoe_opponent.py together.
- imaging.py is a program that turns the image of the board into a numpy matrix
- tictactoe_opponent.py is another tictactoe game that I programmed with a different type of ai.

# Previous logs:
This project aims to create a tictactoe AI player that plays perfectly. It will do so by training against a perfectly optimized tictactoe bot.

This project is a practice project for my other, bigger scale project: to create a tetris AI player. I decided to create this project first to gain some experience before beginning that project.

This project involves 4 programming elements:
- The actual tictactoe game
- Using image thresholding to input the grid to the AI player, converting the initial image input to a numpy array, which is easier to operate on.
- Creating an AI player that trains.
- Using pyGUI to input the moves of the AI player to the actual game.