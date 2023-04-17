# Maze AI Prepended with Tic-Tac-Toe
#### Video Demo:  <URL HERE>
#### Description:
  
This project is two-fold. I created a class based pygame that implements and AI generated A* search, then I created a functional based CLI Tic-Tac-Toe game. In the Tic-Tac-Toe game, the AI you face is completely random, and doesn't implement any intelligent move choices.


## Maze AI

This is a pygame game that allows you to find the best path to the goal (the coin). Every step you take is marked with an 'X' and every move that did not lead you to the goal in the end is replaced by a question mark. Once you make it to the coin, you are provided with a score which is just a number of how many steps it took you to get to the goal.

The AI analyzes the game board, and makes the best move towards the goal according to A* search until it makes it to the goal. It is given information about where the ending is and how many steps it has taken to get to where it currently is. Whichever next move gets it closer to the goal while also minimizing the number of steps taken is the step that will be taken in search of the goal. If there are multiple possible best moves, then the best move is chosen from random out of the best moves.

In the case that the AI is walked into a box, the AI can still search from any possible square it has seen before in the future. It does this by keeping a queue of nodes inside of a frontier. This is what is used to search out of. In order to keep the documents reasonable, the nodes logic is seperated out into it's own file called "nodes.py." This file encodes the basic information needed to have a frontier with nodes holding the information I needed for the maze.

Along with the other files in this project, are a bunch of resource files. These resource files must lie in the same directory as the project file and it contains all the images needed for the pygame game.


## Tic-Tac-Toe

This is a simple game of tic-tac-toe. The rules are the same as they would normally be, but you play against an AI who chooses randomly. The game is completely interfaced via the command line, and you can choose your next space by typing in the number of the row and the column you wish to make your move into. If you provide an invalid input for almost anything in the command line, it will reprompt you again and again until you give a valid answer.

This game is what I used to create a test folder on and it allows for simpler test integration. It starts before the maze game does, and you do not get access to the maze game until you beat the AI in tic-tac-toe. After such an embarrassing loss, the AI shows you it's true knowledge with the maze.