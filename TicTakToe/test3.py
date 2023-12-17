# Import modules
from tkinter import *
from PIL import Image, ImageTk
import random


class MainPage(Frame):
    def __init__(self, con, cont):
        super().__init__(con)
        self.config(height=100, width=20, background="green")

        but = Button(self, text="First Page", command=lambda: cont.switch_page(FirstPage))
        but.pack()


class FirstPage(Frame):
    def __init__(self, con, cont):
        super().__init__(con)
        self.config(height=100, width=20, background="red")

        but = Button(self, text="Second Page", command=lambda: cont.switch_page(SecondPage))
        but.pack()


class SecondPage(Frame):
    def __init__(self, con, cont):
        super().__init__(con)
        self.config(height=100, width=20, background="blue")

        but = Button(self, text="Main Page", command=lambda: cont.switch_page(MainPage))
        but.pack()


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("400x400")
        self.resizable(False, False)

        con = Frame(self)
        con.pack(side = "top", fill = "both", expand = True)

        self.pages = {}

        for F in (MainPage, FirstPage, SecondPage):
  
            page = F(con, self)

            self.pages[F] = page 

            page.grid(sticky="nsew")

        self.switch_page(MainPage)

    def switch_page(self, pi):
        f = self.pages[pi]
        f.tkraise()

tictactoe = App()

tictactoe.mainloop()