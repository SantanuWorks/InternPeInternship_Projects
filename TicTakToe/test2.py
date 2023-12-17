from tkinter import *
import random

board_places = [1, 2, 3, 4, 5, 6]

App = Tk()
App.title("Tic Tak Toe")
App.minsize(400, 400)
App.maxsize(400, 400)

F1 = Frame(App, height = 100, width = 100, background="Red")
F1.grid(column=0, row=0, sticky="nsew")
F2 = Frame(App, height = 100, width = 100, background="Blue")
F2.grid(column=0, row=0, sticky="nsew")

print(F1, F2)

Fset = [ F1, F2 ]

def op(i):
    Fset[i].tkraise()


t1 = Button(App, height=3, width=4, text="Red", command= lambda o = 0: op(o)).grid()
t2 = Button(App, height=3, width=4, text="Red", command= lambda o = 1: op(o)).grid()

App.mainloop()