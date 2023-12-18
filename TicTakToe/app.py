# import required modules
from tkinter import * # for GUI
from PIL import Image, ImageTk # to show image 
import random # for random guess
from threading import Timer # set timing to methods

'''
Credit: Welcome Page Image
https://images.app.goo.gl/EGGjzVoy1NnwyMo66

'''
# Player class contains all the details about player of the game
class Player():
    player1 = ""
    player2 = ""

    pltype = 0
    
    pl1symbol = "O"
    pl2symbol = "X"

    pl1turnmsg = ""
    pl2turnmsg = ""

    currpl = 1
    currplname = ""
    currplsym = ""
    currturnmsg = "m"

    winsym = ""
    winner = ""

    def __init__(self, pltype):
        # Get player type ( 1 player or 2 player )
        Player.pltype = pltype

        # set player properties according to the given player type
        if( Player.pltype == 1 ):
            Player.player2 = "Computer"
            Player.player1 = "You"
            Player.pl2turnmsg = "Computer's Turn"
            Player.pl1turnmsg = "Your Turn"
        else:
            Player.player1 = "Player 1"
            Player.player2 = "Player 2"
            Player.pl1turnmsg = "Player 1's Turn"
            Player.pl2turnmsg = "Player 2's Turn"
        Player.currpl = 1
        Player.currplname = Player.player1
        Player.currplsym = Player.pl1symbol
        Player.currturnmsg = Player.pl1turnmsg
        GamePage.turnlabel.config(text=Player.currturnmsg)
    
    # switch player turns
    def switchplayer():
        if Player.currpl == 1:
            Player.currpl = 2
            Player.currplname = Player.player2
            Player.currplsym = Player.pl2symbol
            Player.currturnmsg = Player.pl2turnmsg
        else:
            Player.currpl = 1
            Player.currplname = Player.player1
            Player.currplsym = Player.pl1symbol
            Player.currturnmsg = Player.pl1turnmsg

# Class to show the result of the game
class ResultPage(Frame):
    result = None
    # Show the page
    def __init__(self, container, controller):
        super().__init__(container)
        self.config(background="#a6c1ff")
        ResultPage.result = Label(self, text = "", font=("Console", 18, "bold"), border=0, background = "#a6c1ff", foreground="#1a75ff")
        ResultPage.result.pack()
        ResultPage.result.place(relx=0.5, rely=0.45, anchor=CENTER)
        back = Button(self, text="Main Menu", font=("Roboto", 12, "bold"), width=10, pady=3, border=0, relief='sunken', background="lime", foreground="white", command= lambda: controller.switchpage(StartPage))
        back.place(relx=0.5, rely=0.55, anchor=CENTER)

    # Set the result
    def setresult(result):
        ResultPage.result.config(text = result)

# Defines the game page
class GamePage(Frame):
    turnlabel = None
    # Show the page
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        self.config(background="#a6c1ff")
        board = Frame(self)
        board.pack()
        board.place(relx=0.5, rely=0.55, anchor=CENTER)
        back = Button(self, text="Quit", font=("Roboto", 10, "bold"), width=8, pady=3, border=0, relief='sunken', background="lime", foreground="white", command= lambda: self.terminate(StartPage))
        back.place(relx=0.15, rely=0.07, anchor=CENTER)
        GamePage.turnlabel = Label(self, text="", font=("Roboto", 11, "bold"), background="#a6c1ff")
        GamePage.turnlabel.place(relx=0.5, rely=0.25, anchor=CENTER)
        # Initialize all the parameters of the game
        self.winflag = False
        self.selectedcells = []
        self.boardstates = [ "", "", "", "", "", "", "", "", "" ]
        self.cellobjs = [ None, None, None, None, None, None, None, None, None ]
        self.winstates = [ [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6] ]
        self.drawboard(board)
    
    # clear all the parameters after quiting 
    def cleargamestates(self):
        self.boardstates = [ "", "", "", "", "", "", "", "", "" ]
        self.winflag = False
        self.selectedcells = []
        for each in self.cellobjs:
            each.config(text="")

    # Terminaate the current game 
    def terminate(self, page):
        # self.cleargamestates()
        self.controller.switchpage(page)
        t = Timer(0.5, self.cleargamestates)
        t.start()

    # Check for win 
    def checkwin(self):
        for i in range(8):
            index = self.winstates[i]
            Player.winsym = self.boardstates[index[0]] + self.boardstates[index[1]] + self.boardstates[index[2]]
            if Player.winsym in [ "XXX", "OOO" ]:
                if Player.winsym[0] == Player.pl1symbol:
                    Player.winner = Player.player1
                else:
                    Player.winner = Player.player2
                return True
        return False
    
    # Get results of winner
    def getwinresult(self):
        winmsg = Player.winner + " Won!"
        return winmsg

    # For 1 player - computer guess
    def getcomputermove(self):
        while True:
            choose = random.randint(0, 8)
            if choose not in self.selectedcells:
                self.selectedcells.append(choose)
                break
        self.activecell(choose)
        return choose
    
    # Provides game actions duing game play
    def gameactions(self, plotindex):
        # for 2 player mode
        if Player.pltype == 2 :
            self.activecell(plotindex)
        # for 1 player mode
        else:
            # check for draw 
            if len(self.selectedcells) == 9:
                ResultPage.setresult("It's a tie!")
                self.cleargamestates()
                self.controller.switchpage(ResultPage)
            # if not draw continue with player switching
            else:
                # when player 2 turn - computer guess
                if Player.currpl == 2:
                    n = self.getcomputermove()
                    self.selectedcells.append(n)
                    self.activecell(n)
                # for player 1 guess wait
                else:
                    self.selectedcells.append(plotindex)
                    self.activecell(plotindex)
                    t = Timer(1, lambda: self.gameactions(0))
                    t.start()
                self.selectedcells = list(set(self.selectedcells))
        # check for the win 
        if self.checkwin():
            # move to next page and set result
            result = self.getwinresult()
            ResultPage.setresult(result)
            self.cleargamestates()
            self.controller.switchpage(ResultPage)
            return
        # switch player if no draw no win
        Player.switchplayer()
        # set turn message
        GamePage.turnlabel.config(text=Player.currturnmsg)
    
    # scratch on the cell - O or X
    def activecell(self, x):
        if self.boardstates[x] != "":
            return
        self.boardstates[x] = Player.currplsym
        self.cellobjs[x].config( text = Player.currplsym )

    # draw the board for play
    def drawboard(self, container):
        count = -1
        for i in range(3):
            for j in range(3):
                count = count + 1
                cell = Button(container, text = "", font = ("Console", 25), border=1, background = "white", foreground = "Red", relief='sunken', command = lambda cellindex = count: self.gameactions(cellindex))
                cell.config(height = 1, width = 3)
                cell.grid(row = i, column = j, sticky = "nsew")
                self.cellobjs[count] = cell
# Start page for user options and game modes
class StartPage(Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        header = Frame(self, height = 20, width = 350, background="#a6c1ff")
        header.pack(anchor="n") 
        toppane = Frame(self)
        toppane.config(height = 233, width = 350)
        toppane.pack(anchor = "w")
        img = ImageTk.PhotoImage(Image.open("wel.png"))
        imagecon = Label(toppane, image = img, borderwidth=0)
        imagecon.dontloseit = img
        imagecon.pack()
        downpane = Frame(self)
        downpane.config(height = 167, width = 350, background = "#a6c1ff")
        downpane.pack(anchor = "w")
        welcon = Label(downpane, text = "Let's Play!", font=("Console", 22, "bold"), borderwidth=0, background = "#a6c1ff", foreground="blue")
        welcon.place(relx=0.5, rely=0.2, anchor=CENTER)
        oneplayer = Button(downpane, text="1 Player", font=("Roboto", 12, "bold"), width=10, pady=5, border=0, relief='sunken', background="lime", foreground="white", command= lambda: self.start(controller, GamePage, 1))
        oneplayer.place(relx=0.3, rely=0.6, anchor=CENTER)
        twoplayer = Button(downpane, text="2 Player", font=("Roboto", 12, "bold"), width=10, pady=5, border=0, relief='sunken', background="lime", foreground="white", command= lambda: self.start(controller, GamePage, 2))
        twoplayer.place(relx=0.7, rely=0.6, anchor=CENTER)
    
    # start the game
    def start(self, controller, page, pltype):
        Player(pltype)
        controller.switchpage(page)

# App
class TicTacToeApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("350x400")
        self.resizable(False, False)
        container = Frame(self)
        container.pack(side = "top", fill = "both")
        self.pages = {}
        for PageClass in (StartPage, GamePage, ResultPage):
            page = PageClass(container, self)
            self.pages[PageClass] = page 
            page.grid(column=0, row=0, sticky="nsew")
        self.switchpage(StartPage)

    # switch pages
    def switchpage(self, pageclass):
        page = self.pages[pageclass]
        page.tkraise()
# start the app
if __name__ == "__main__":
    app = TicTacToeApp()
    app.mainloop()