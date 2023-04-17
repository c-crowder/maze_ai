import pygame
import random
import time
from nodes import *

"""
    All of the logic for this game and AI are contained within the Maze class
    The first half of the methods detail the logic required to run the game
    The init method loads all of the content of the game and prepares the knowledge for the AI later
"""
class Maze:
    def __init__(self):
        pygame.init()

        # Starts a new game and loads necessary .png files
        self.new_game()
        self.load_images()

        # Variables for use later with the AI 
        # self.movements is also used for the move method functionality
        self.movements = {'UP': (-1, 0), 'DOWN': (1, 0), 'RIGHT': (0, 1), 'LEFT': (0, -1)}
        self.moves_made = []
        self.frontier = Frontier()
        self.current_node = None

        # Determines how large to make the screen
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_height()

        # Sets a uniform game font
        self.game_font = pygame.font.SysFont("Arial", 36)

        window_width = self.width * self.scale
        window_height = self.height * self.scale

        self.window = pygame.display.set_mode((window_width, window_height + self.scale))

        pygame.display.set_caption("Maze AI")

        # Starts the main loop of the game - this is where the display and events are repeated
        self.main_loop()

    # Loads every .png in the list of file names
    def load_images(self):
        print("Loading Images...")
        self.images = []
        for image in ['Wall', 'Path', 'Chosen', 'Goal', 'Searched', 'Player']:
            self.images.append(pygame.image.load(f"{image}.png"))
        print("Images Loaded")

    # Resets all needed value to their base value and designs the start map state
    # This includes values needed for the AI
    def new_game(self):
        self.won = False
        self.moves = 0
        self.moves_made = []
        self.frontier = Frontier()
        self.current_node = None
        # The map of the game is based off of this 2D array
        # You can adjust this to change the map - only one coin and one player are allowed at a time
        self.map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 5, 1, 1, 0, 1, 1, 1, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    # Checks all events and draws the window after events
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
    
    # Basic events include movement keys, start/stop keys, and 'A' key to run the AI
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                elif event.key == pygame.K_UP:
                    self.move('UP')
                elif event.key == pygame.K_DOWN:
                    self.move('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.move('RIGHT')
                elif event.key == pygame.K_r:
                    self.new_game()
                elif event.key == pygame.K_t:
                    print(self.distance_to_goal(self.position()))
                elif event.key == pygame.K_a:
                    self.game_ai()
                
                elif event.key == pygame.K_y and self.won:
                    self.new_game()
                elif event.key == pygame.K_n and self.won:
                    exit()

    # Returns the current position of the player
    def position(self):
        if self.moves == 0:
            for y in range(self.height):
                for x in range(self.width):
                    location = [y, x]
                    if self.map[location[0]][location[1]] == 5:
                        self.current_position = location
                        return location
        return self.current_position        

    # Takes a direction ('UP', 'DOWN', 'LEFT', 'RIGHT') and moves the player based on that direction
    def move(self, direction):
        # Stop all movement if we already won
        if self.won:
            return
        location = self.position()
        
        move = (location[0] + self.movements[direction][0], location[1] + self.movements[direction][1])
        # IF the move is invalid, don't do anything
        if location[0] > 0 and location[0] < self.height and location[1] > 0 and location[1] < self.width:
            pass
        else:
            return

        # This logic determines what to do based on what the move would end up doing
        new_location = self.map[move[0]][move[1]]
        if new_location == 1 or new_location == 4:
            self.moves += 1
            self.map[location[0]][location[1]] = 2
            self.map[move[0]][move[1]] = 5
            self.current_position = move
        # Set the win variable to True and that will end the game later
        elif new_location == 3:
            self.moves += 1
            self.won = True
        elif new_location == 2:
            self.moves += 1
            self.map[location[0]][location[1]] = 4
            self.map[move[0]][move[1]] = 5
            self.current_position = move

    # This function returns the location of the goal for the AI
    def goal_location(self):
        for y in range(self.height):
            for x in range(self.height):
                if self.map[y][x] == 3:
                    return (y, x)

    # Returns all possible moves in self.movements for the AI to choose from
    def valid_moves(self, location):
        location = location

        possible_moves = []

        for key, move in self.movements.items():
            if self.map[location[0]+move[0]][location[1]+move[1]] != 0:
                possible_moves.append({key: move})

        return possible_moves

    # Calculates how far the parameter location is from the goal
    def distance_to_goal(self, location):
        goal = self.goal_location()
        distance = (abs(goal[0] - location[0]) + abs(goal[1] - location[1]))
        return distance

    # returns a new location based on a current location and a direction
    def move_translation(self, location, direction):
        new_location = (location[0] + self.movements[direction][0], location[1] + self.movements[direction][1])
        return new_location

    """
    This is the main logic of the AI - it is used to create nodes and add these nodes to the frontier
    Each node keeps track of the parent node, current location, and move made to get to this node
    From the current node, we expand that node and add them to the frontier if they are not already in the frontier
    We then choose a node from the frontier based on A-Star search (if it is least movement when adding the closest
    node to the goal with the amount of moves made, then it is the node that is removed)
    When a node is removed from the frontier, it is now the current node that restarts the process
    If the current node is the location that we are looking for, then we expand that node's family tree
    Using that family tree we determine the moves made to get there, and pass it into the self.move function
    """
    def game_ai(self):
        location = self.position()
        self.current_node = Node(location)
        print("AI Thinking...")
        while True:
            possible_moves = self.valid_moves(self.current_node.location)
            for move in possible_moves:
                for direction, move in move.items():
                    new_location = self.move_translation(self.current_node.location, direction)
                    node = Node(new_location, parent=self.current_node, move=direction)
                    if node.location not in self.frontier.explored:
                        self.frontier.add(node)
            lowest = 100000000000000
            best = None
            for node in self.frontier:
                a_star = self.distance_to_goal(node.location) + len(self.moves_made)
                if a_star < lowest:
                    lowest = a_star
                    best = node
            if best != None:
                self.frontier.remove(best)
                self.moves_made.append(best.move)
                self.current_node = best
            else:
                print("no moves")
                break
            if best.location == self.goal_location():
                moves = self.return_moves(best) 
                print("Moving Player...")
                for move in moves[1:]:
                    self.move(move)
                break

    # Returns the list of moves from the given node to get to that node
    def return_moves(self, final_node):
        if final_node.parent == None:
            return [final_node.move]
        return self.return_moves(final_node.parent) + [final_node.move]

    # Logic to draw the window - draws different things based on the win state of the game
    def draw_window(self):
        self.window.fill((255,255,255))

        for y in range(self.height):
            for x in range(self.width):
                image = self.map[y][x]
                self.window.blit(self.images[image], ((x*self.scale + self.scale/2) - (self.images[image].get_width()/2), ((y*self.scale + self.scale/2) - ((self.images[image].get_height())/2))))

        game_text = self.game_font.render(f"Moves: {self.moves}", True, (0, 0, 0))
        self.window.blit(game_text, (50, self.height * self.scale + (self.scale/2 - game_text.get_height()/2)))

        game_text = self.game_font.render(f"(ESC) to exit (R) to retry (A) AI", True, (0, 0, 0))
        self.window.blit(game_text, (250, self.height * self.scale + (self.scale/2 - game_text.get_height()/2)))

        if self.won:
            game_text = self.game_font.render("Congratulations! You beat all the levels!", True, (255, 255, 255))
            game_text2 = self.game_font.render("Restart? (y/n)", True, (255, 255, 255))
            game_text3 = self.game_font.render(f"Total Moves: {self.moves}", True, (255, 255, 255))
            game_textx = (self.width*self.scale)/2 - game_text.get_width()/2
            game_texty = (self.height*self.scale)/2 - game_text.get_height()/2
            game_text2x = (self.width*self.scale)/2 - game_text2.get_width()/2
            game_text2y = (self.height*self.scale)/2 - game_text2.get_height()/2 + 50
            game_text3x = (self.width*self.scale)/2 - game_text3.get_width()/2
            game_text3y = (self.height*self.scale)/2 - game_text3.get_height()/2 + 200

            pygame.draw.rect(self.window, (0, 0, 255), (game_textx-10, game_texty, game_text.get_width()+20, game_text.get_height()))
            self.window.blit(game_text, (game_textx, game_texty))
            pygame.draw.rect(self.window, (0, 0, 255), (game_text2x-10, game_text2y, game_text2.get_width()+20, game_text2.get_height()))
            self.window.blit(game_text2, (game_text2x, game_text2y))
            pygame.draw.rect(self.window, (0, 0, 255), (game_text3x-10, game_text3y, game_text3.get_width()+20, game_text3.get_height()))
            self.window.blit(game_text3, (game_text3x, game_text3y))

        pygame.display.flip()


def main():
    tic_tac_toe()
    game = Maze()


def tic_tac_toe():
    winner = False
    board = [[0,0,0],[0,0,0],[0,0,0]]
    user = get_user()
    draw_board(board)
    while not winner:
        player = get_player(board)
        if player == user:
            move = get_move(board)
        else:
            move = ai_move(board)
        board, winner = make_move(board, player, move)
        draw_board(board)
    winner = "X" if winner == 1 else "O"
    print(f"Winner is {winner}!")


def ai_move(board):
    moves = []
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == 0:
                moves.append((i, j))
    move = random.choice(moves)
    print("AI moving...")
    time.sleep(.5)
    return move


def get_user():
    while True:
        user = input("Play as X or O? ").upper()
        if user == "X" or user == "O":
            return 1 if user == "X" else 2
        print("Invalid input - try again")


def draw_board(board):
    for i in board:
        print("    ", end='')
        for j in i:
            if j == 0:
                print("_  ", end='')
            elif j == 1:
                print("X  ", end='')
            elif j == 2:
                print("O  ", end='')
        print()


def get_move(board):
    while True:
        row = input("What row (1, 2, 3)? ")
        if row not in ['1', '2', '3']:
            print("Invalid row - try again")
            continue
        column = input("What column (1, 2, 3)? ")
        if column not in ['1', '2', '3']:
            print("Invalid column - try again")
            continue
        row = int(row) - 1
        column = int(column) - 1
        if board[row][column] == 0:
            return (row, column)
        print("Move invalid - try again")


def make_move(board, player, move):
    board[move[0]][move[1]] = player
    winner = get_winner(board)
    if winner:
        return board, winner
    return board, winner


def get_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] != 0:
                return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] != 0:
                return board[0][i]

    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] != 0:
            return board[1][1]
    elif board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] != 0:
            return board[1][1]

    return None


def get_player(board):
    players = {0: 0, 1: 0, 2: 0}

    for row in board:
        for column in row:
            players[column] += 1

    if players[1] > players[2]:
        return 2
    return 1


# Runs the Maze() class object
if __name__ == "__main__":
    main()
