#! /usr/bin/python3

import os
import random

print("Welcome to TicTakToe!")

def getNumPlayers():
    numPlayersValid = False
    while not(numPlayersValid):
        numPlayers = int(input("Enter the number of players: [1/2] "))
        if 0 < numPlayers <= 2:
            numPlayersValid = True
        else:
            print("Please choose the correct number of players. The available options are 1 and 2\n")
    return numPlayers

def getPlayerName(player):
    return input("Enter Player {}'s Name: ".format(player))

def getPlayerKey(player):
    validToken = False
    char = ""
    while not(validToken):
        char = input("Enter the character you would like to use: [A-Z] ")
        if len(char) == 1 and  65 <= ord(char) <= 90:
            validToken = True
        else:
            print("Please enter only one character only using capital letters.")
    return char

def getFirstPlayer():
    return "p1"

def switchTurn(turn):
    if turn == "p1":
        return "p2"
    else:
        return "p1"

def getBotPlacement(board):
    choices = []
    for x in board:
        if str(board[x]).isdigit():
            choices.append(board[x])
    botChoice = random.choice(choices)
    return botChoice - 1


#Initializes the game
def initialize():

    numOfPlayers = getNumPlayers()

    gameInfo = dict(
        numOfPlayers = numOfPlayers,
        p1Name = getPlayerName(1),
        p2Name = getPlayerName(2) if numOfPlayers == 2 else "Computer",
        boardState = dict(cell0=1, cell1=2, cell2=3, cell3=4, cell4=5, cell5=6, cell6=7, cell7=8, cell8=9),
        p1Token = getPlayerKey(1),
        p2Token = (getPlayerKey(2) if numOfPlayers != 1 else chr(random.randint(65,90))),
        turn = "p1" if numOfPlayers == 1 else getFirstPlayer(),
        recordsFile = "pyc_pyk_poe.txt",
        p1Wins = 0,
        p1Loses = 0,
        p1Draws = 0,
        p2Wins = 0,
        p2Loses = 0,
        p2Draws = 0,
        gamesPlayed = 0,
        winner = None
    )

    return gameInfo

def checkWin(gameInfo):
    winner = [False, "", ""]
    winConditions = (
        #Horizontals
        [0,1,2],
        [3,4,5],
        [6,7,8],
        #Verticals
        [0,3,6],
        [1,4,7],
        [2,5,8],
        #Diagonals
        [0,4,8],
        [2,4,6]
    )

    possible = []
    for x in gameInfo["boardState"]:
        if str(gameInfo["boardState"][x]).isdigit():
            possible.append(gameInfo["boardState"][x])

    if len(possible) == 0:
        winner[0] = True
        winner[1] = "Nobody"

    for x in winConditions:
        current = []
        for y in gameInfo["boardState"]:
            for z in x:
                if y.endswith(str(z)):
                    current.append(gameInfo["boardState"][y])

        if current[0] is current[1] is current[2]:
            winner[1] = gameInfo[gameInfo["turn"]+"Name"]
            winner[2] = gameInfo["turn"]
            winner[0] = True
            break
    #Function returns winner array if bool in winner is True else it returns False
    return winner

def placeToken(gameInfo):
    validInput = False
    if(gameInfo["turn"] == "p1"):
        while not(validInput):
            cellNum = None
            cell = input(gameInfo["p1Name"] + " it is your turn which cell number would you like to place your token? [1-9]\n")
            if cell.isdigit():
                cellNum = (int(cell) - 1)
                if 0 <= cellNum < 9 and str(gameInfo["boardState"]["cell"+str(cellNum)]).isdigit():
                    print(gameInfo["boardState"]["cell"+str(cellNum)])
                    cell = int(cell)
                    validInput = True
                else:
                    possible = []
                    for x in gameInfo["boardState"]:
                        if str(gameInfo["boardState"][x]).isdigit():
                            possible.append(gameInfo["boardState"][x])
                    print("Please choose one of the following cells: {}".format(possible))
        return cellNum

    elif(gameInfo["numOfPlayers"] == 2 and gameInfo["turn"] == "p2"):
        while not(validInput):
            cellNum = None
            cell = input(gameInfo["p2Name"] + " it is your turn which cell number would you like to place your token? [1-9]\n")
            if cell.isdigit():
                cellNum = (int(cell) - 1)
                if 0 <= cellNum < 9 and str(gameInfo["boardState"]["cell"+str(cellNum)]).isdigit():
                    print(gameInfo["boardState"]["cell"+str(cellNum)])
                    cell = int(cell)
                    validInput = True
                else:
                    possible = []
                    for x in gameInfo["boardState"]:
                        if str(gameInfo["boardState"][x]).isdigit():
                            possible.append(gameInfo["boardState"][x])
                    print("Please choose one of the following cells: {}".format(possible))
        return cellNum
    else:
        return getBotPlacement(gameInfo["boardState"])

#Draws the board with its current state on the terminal
def draw(game):
    #Clears the terminal for better visuals of the board
    if(os.name=="posix"):
        os.system("clear")
    else:
        os.system("cls")

    #Outputs the board with current values in the game
    print(game["p1Name"]+"'s Wins: " + str(game["p1Wins"]) + "  | " + game["p2Name"]+"'s Wins: " + str(game["p2Wins"]))
    print(game["p1Name"]+"'s Loses: " + str(game["p1Loses"]) + " | " + game["p2Name"]+"'s Loses: " + str(game["p2Loses"]))
    print(game["p1Name"]+"'s Draws: " + str(game["p1Draws"]) + " | " + game["p2Name"]+"'s Draws: " + str(game["p2Draws"]))
    print()
    print("  {cell0} \u2758 {cell1} \u2758 {cell2} \n  \u2014 + \u2014 + \u2014 \n  {cell3} \u2758 {cell4} \u2758 {cell5} \n  \u2014 + \u2014 + \u2014  \n  {cell6} \u2758 {cell7} \u2758 {cell8} ".format(**game["boardState"]))
    print()

playGame = True
firstRun = True
gameInfo = None
while(playGame):
    if(firstRun):
        #Checks for record file
        gameInfo = initialize()
        draw(gameInfo)
        gameInfo["boardState"]["cell"+str(placeToken(gameInfo))] = gameInfo[gameInfo["turn"]+"Token"]
        gameInfo["turn"] = switchTurn(gameInfo["turn"])
        firstRun = False
    else:
        draw(gameInfo)
        gameInfo["boardState"]["cell"+str(placeToken(gameInfo))] = gameInfo[gameInfo["turn"]+"Token"]
        draw(gameInfo)
        winner = checkWin(gameInfo);
        if winner[0]:
            if winner[1] != "Nobody":
                print(winner[1] + " is the winner!\nCONGRATULATIONS!!!!\n")
                #Do things for taking care of wins
                if winner[2] == "p1":
                    gameInfo["p1Wins"] += 1
                    gameInfo["p2Loses"] += 1
                elif winner[2] == "p2":
                    gameInfo["p2Wins"] += 1
                    gameInfo["p1Loses"] += 1
            else:
                print("DRAW!!!")
                print(winner[1] + " is the winner.\n")
                gameInfo["p1Draws"] += 1
                gameInfo["p2Draws"] += 1

            if input("Would you like to play again? [y/N]").lower() != "y":
                playGame = False
            else:
                gameInfo["boardState"] = dict(cell0=1, cell1=2, cell2=3, cell3=4, cell4=5, cell5=6, cell6=7, cell7=8, cell8=9)
        else:
            gameInfo["turn"] = switchTurn(gameInfo["turn"])
