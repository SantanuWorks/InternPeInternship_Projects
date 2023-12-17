from tkinter import *
import random

App = Tk()
App.title("Tic Tac Toe")
App.minsize(400, 400)
App.maxsize(400, 400)
App.config(background="black")

Board = Frame(App)
Board.pack()
Board.place(relx=0.5, rely=0.5, anchor=CENTER)

PlayerValue = "X"

BoardState = [ "", "", "", "", "", "", "", "", "" ]

CellObjs = [ None, None, None, None, None, None, None, None, None ]

WinIndex = [ [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6] ]

def SwtichTurn():
    global PlayerValue
    if PlayerValue == "X":
        PlayerValue = "O"
    else:
        PlayerValue = "X"

def CheckWin():
    for i in range(8):
        index = WinIndex[i]
        if (BoardState[index[0]] + BoardState[index[1]] + BoardState[index[2]]) in [ "XXX", "OOO" ]:
             print(index)
             print(BoardState)
             return True
    return False

def ActiveCell(x):
    if BoardState[x] != "":
        return
    BoardState[x] = PlayerValue
    CellObjs[x].config( text = PlayerValue )
    wflg = CheckWin()
    if  wflg:
        print("Win")
        return
    else:
        SwtichTurn()

def DrawBoard():
    count = -1
    for i in range(3):
        for j in range(3):
            count = count + 1
            Cell = Button(Board, text = "", font = ("Console", 25), height = 2, width = 5, background = "white", foreground = "Red", relief='sunken', command = lambda cellindex = count: ActiveCell(cellindex))
            Cell.grid(row = i, column = j, sticky = "nsew")
            CellObjs[count] = Cell

DrawBoard()

App.mainloop()