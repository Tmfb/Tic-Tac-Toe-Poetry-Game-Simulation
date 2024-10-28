from copy import copy
from Ficha import Ficha
from Player import Player
from math import floor
from random import random, choice
from copy import copy
import json

import time


#Initializes an empty board for the given dimensions + border. Filling it with a especial Ficha object
def createBoard ():

    aux_board = []
    empty_field = Ficha(" ",["O","O"],"space")
    #Creates border on both sides of each dimension and asociates rows with witdh, since the printed board will be rotated
    for i in range(width + 2*border):
        aux_board.append([])
        for j in range(height + 2*border):
            aux_board[i].append(empty_field)
    return aux_board


#Prints current board state to console, on both sides
#pendiente de fusionar color y main board en un solo acceso a array
def printBoard(color,board):

    #Print main board
    print (" "*83 + "This is " + color +"'s side\n\n")

    for i in range(height + border-1, border-1, -1):
        printeable_row, token_value = (" "*20 + "|",0)
        for j in range(border, width + border):
            if (color == "Yellow"):
                token_value = board[j][i].getWords(0)
            else:
                token_value = board[j][i].getWords(1)
            printeable_row += spaceItem(token_value) + "|"
        print (printeable_row + "\n")

    #Print color distribution
    print ("\n" + " "*83 + "This is are the color of the fichas")
    for i in range(height + border-1, border-1, -1):
            printeable_colors, token_value = (" "*20 + "|",0)
            for j in range(border, width + border):
                token_value = board[j][i].getColor()
                printeable_colors += spaceItem(token_value) + "|"
            print (printeable_colors + "\n")

    #Print column identifiers
    printeable_row = ""
    for n_column in range(1,width+1):
        printeable_row += spaceItem(str(n_column)) +" "
    print (" "*20 + printeable_row + "\n\n")


def showFichas(color_fichas):

    printeable_row = ""
    for i in range(1, len(color_fichas)+1):
        if (i%5 == 0):
            print (" "*45 + printeable_row)
            printeable_row = ""
        printeable_row += spaceItem(str(i) + " " + color_fichas[i-1].getWords())
    print (" "*45 + printeable_row)  

#Calculates the back and front spacing needed for the given string item when printed on the screen to stay within it's column.
#Returns a list containing back and front spacing strings in it's 0 and i indexes respectively
def spaceItem(item,total_spacing = 20):

    item_spacing = total_spacing - len(item)
    back_spacing = floor(item_spacing/2)
    front_spacing = item_spacing - back_spacing
    spaced_item = " "* back_spacing+ item + " "* front_spacing
    return spaced_item

#Loads each color word dictionary to y_words and b_words global variables from a .json.
def loadWords():

    y_words = {}
    b_words = {}
    y_fichas = []
    b_fichas = []
    y_schema = {}
    b_schema = {}
    #Access json data file and stores each color in their respective variables 
    with open(json_path) as json_file:
        json_dict = json.load(json_file)
        y_words, b_words = json_dict["yellow"],json_dict["blue"]

    #Iterates the yellow word dictionary and creates a list of all Ficha objects stored on y_fichas
    for typeKey in y_words:
        for i in range(len(y_words[typeKey])):
            ficha = Ficha("yellow",y_words[typeKey][i],typeKey)
            y_fichas.append(ficha)
        y_schema[typeKey] = len(y_words[typeKey])

    #Iterates the blue word dictionary and creates a list of all Ficha objects stored on b_fichas
    for typeKey in b_words:
        for i in range(len(b_words[typeKey])):
            ficha = Ficha("blue",b_words[typeKey][i],typeKey)
            b_fichas.append(ficha)
        b_schema[typeKey] = len(b_words[typeKey])


    return (y_fichas, b_fichas, y_schema, b_schema)

def firstEmpty(column, board):
    for j in range(border, height + border):
        if (board[column + border-1][j].getWords() == "O - O"):
            return (column + border-1, j)
    return False

#Given a position on the board, calculates the best move iterating all posible axis
def bestMove(valid_move, player, board):

    score_list = {"vertical": 0, "d_diagonal": 0, "horizontal": 0, "u_diagonal": 0}
    axes = {"vertical":(0,-1), "d_diagonal": (1,-1), "horizontal": (1,0), "u_diagonal": (1,1)}
    move_type = ""

    for axis in axes:
        i,j = valid_move
        x,z = axes[axis]
        color_count = 0

        #Calculates color streak for each axis
        while (board[i-x][j-z].getColor() == player.getColor()):
            i -= x
            j -= z

        while (board[i][j].getColor() == player.getColor() or (i,j) == valid_move):
            color_count += 1
            i += x
            j += z
        #Adding the color streak modifier to the score
        score_list[axis] += color_streak_modifier[color_count]

        #Refresing move cc's for sintax logic
        i,j = valid_move
        avaliable_types = player.getFichasSchema()

        #Goes back in the axis until a space is found
        while (board[i-x][j-z].getType() != "space"):
            i -= x
            j -= z

        #Advances the axis calculating the score and filling the best move for the player cc's, stoping after finding a space
        while True:
            if ((i,j) == (valid_move[0]-x, valid_move[1]-z)):
                pass
            elif ((i,j) == valid_move):
                #Calculates the best move given the previous
                #Previous logic. Calculates a type move
                if (board[i-x][j-z].getType() == "space"):
                    move_type = choice(avaliable_types)
                    modifier = (random() * random_modifier) - random_modifier/2
                    score_list[axis] += modifier

                else:
                    previous_index = ai_weights[len(ai_weights)-1].index(board[i-x][j-z].getType())
                    compatibility_row = list(copy(ai_weights[previous_index]))
                    max_value = 0.0
                    for value in compatibility_row:
                        modifier = (random() * random_modifier) - random_modifier/2
                        if value + modifier > max_value:
                            max_value = value + modifier
                            move_type = ai_weights[len(ai_weights)-1][compatibility_row.index(value)]
                    score_list[axis] += (max_value)

                #Next logic, calculates score given the move type
                if (board[i+x][j+z].getType() != "space"):
                    current_index = ai_weights[len(ai_weights)-1].index(move_type)
                    next_index = ai_weights[len(ai_weights)-1].index(board[i+x][j+z].getType())
                    compatibility_value = ai_weights[current_index][next_index]
                    modifier = (random() * random_modifier) - random_modifier/2
                    score_list[axis] += (compatibility_value + modifier)

            elif (board[i][j].getType() != "space" and board[i+x][j+z].getType() != "space" ):
                current_index = ai_weights[len(ai_weights)-1].index(board[i][j].getType())
                next_index = ai_weights[len(ai_weights)-1].index(board[i+x][j+z].getType())
                compatibility_value = ai_weights[current_index][next_index]
                modifier = (random() * random_modifier) - random_modifier/2
                score_list[axis] += (compatibility_value + modifier)

            else:
                score = 0
                for value in score_list:
                    if (score < score_list[value]):
                        score = score_list[value]

                return (score, move_type)

            #Advance in the axis
            i += x
            j += z
    
    


def aiMove(player,board):
    best_move = 0
    best_ficha = 0
    possible_moves = []
    for column in range (1, width + 1):
        possible_moves.append((0,0))
        valid_move = firstEmpty(column, board)
        if valid_move:
            aux = bestMove(valid_move, player, board)
            possible_moves[column - 1] = (aux[0], aux[1], column)

    best_move = max(possible_moves)
    for ficha in player.getFichas():
        if ficha.getType() == best_move[1]:
            best_ficha = player.popFicha(player.getFichas().index(ficha))
            break

    return makeMove(best_move[2], best_ficha, board)


            
def makeMove(column, ficha, board):

    validMove = firstEmpty(column,board)
    if validMove:
        board[validMove[0]][validMove[1]] = ficha
        return validMove
    else:
        makeMove(input("that column is full, choose another one."), ficha, board)

def winCondition(last_movement, board):
    axes = {"vertical":(0,-1), "d_diagonal": (1,-1), "horizontal": (1,0), "u_diagonal": (1,1)}
    color = board[last_movement[0]][last_movement[1]].getColor()   
    for axis in axes:
        i,j = last_movement
        x,z = axes[axis]
        color_count = 0

        #Backwards
        while (board[i-x][j-z].getColor() == color):
            i -= x
            j -= z

        #Foward
        while (board[i][j].getColor() == color or (i,j) == last_movement):
            color_count += 1
            if (color_count >= 4):
                return True
            i += x
            j += z

    return False


# Main Program config variables

border = 4      #Controls boder size
height = 6      #Board height
width = 7       #Board width
json_path = "words.json"
random_modifier = 0.30
color_streak_modifier = (0, 0.5, 1, 2, 4, 5, 6)
ai_weights = (
    (0.3,0.3,0.2,0.6,0.3,0.4,0.3,0.2,0.4,0.3,0.5),
    (0.5,0.1,0.4,0.5,0.3,0.0,0.1,0.2,0.0,0.4,0.0),
    (0.4,0.6,0.1,0.6,0.7,0.6,0.7,0.7,0.5,0.5,0.4),
    (0.9,0.6,0.3,0.1,0.6,0.3,0.0,0.0,0.2,0.3,0.4),
    (0.4,0.3,0.8,0.4,0.1,0.4,0.5,0.7,0.3,0.5,0.2),
    (0.1,0.1,0.1,0.1,0.1,0.0,0.1,0.1,0.1,0.1,0.1),
    (0.1,0.0,0.4,0.8,0.2,0.0,0.0,0.2,0.1,0.1,0.0),
    (0.8,0.2,0.7,0.3,0.7,0.6,0.2,0.1,0.3,0.5,0.7),
    (0.3,0.3,0.6,0.2,0.5,0.3,0.4,0.5,0.3,0.5,0.2),
    (0.2,0.4,0.2,0.4,0.4,0.2,0.4,0.4,0.1,0.0,0.0),
    (0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.1),
    ("adjetivos", "determinantes", "verbos", "sustantivos", "adverbios", "signos", "articulos", "pronombres", "conjunciones", "preposiciones", "interjecciones")
    )
# for data storage
turn_order = []



def main():
    while (True):
            
            # Input parameters
        players = (Player(input("\n\nYellow player is:\nPlayer\nAI\n"), "Yellow"), Player(input("\nBlue player is:\nPlayer\nAI\n"), "Blue"))
        n_games = int(input("\nChoose number of games to play (or type 0 to close the program)\n"))
        start = time.time()

        # Check for game exit condition
        if (n_games == 0): 
            print( "Goodbye!")
            exit()
        # Play as many games as specified
        for game in range (n_games):
            
            # Board and player initialization
            board = createBoard()
            y_fichas,b_fichas,y_schema,b_schema = loadWords()
            players[0].setFichas(y_fichas)
            players[0].setFichasSchema(y_schema)
            players[1].setFichas(b_fichas)
            players[1].setFichasSchema(b_schema)

            # Full game iterator, alternates player each turn
            for turn in range (height * width):
                choosing_player = players[turn%2]
                # Logic for AI player
                if choosing_player.getType() == "AI":
                    last_movement = aiMove(choosing_player, board)
                    if winCondition(last_movement, board):
                        printBoard(choosing_player.getColor(), board)
                        break
                
                # Logic for human player
                elif choosing_player.getType() == "Player":
                    print (" "*83 + "Game Nº" + str(game+1)  + "   " + choosing_player.getColor() +"'s Turn" "\n\n")
                    printBoard(choosing_player.getColor(), board)
                    showFichas(choosing_player.getFichas())
                    ficha_index = int(input("Wich ficha?\n"))
                    column_index = int(input("In wich column?\n"))
                    last_movement = makeMove(column_index, choosing_player.popFicha(ficha_index-1), board)
                    if input("Do you want to flip it? Y/N\n") == "Y":
                        board[last_movement[0]][last_movement[1]].flip()
                    if winCondition(last_movement, board):
                        print ("YOU WON")
                        break

                else:
                    print("INVALID PLAYER, CLOSING GAME")
                    exit()
        end = time.time()
        print ("total time: " + end-start)

if __name__ == "__main__":
    main()