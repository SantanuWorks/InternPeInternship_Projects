# import required modules
from tkinter import * # for GUI
from PIL import Image, ImageTk # to show image 
import random # for random guess
from threading import Timer # set timing to methods

'''
Credit: Welcome Page Image
https://images.app.goo.gl/rLtMaSm84HEcdXYH9

'''
# Player class contains all the details about player of the game
class Player():
    player1 = ""
    player2 = ""

    pltype = 0
    
    symbol = "⚫"

    pl1color = "Blue"
    pl2color = "#ff0059"

    pl1turnmsg = ""
    pl2turnmsg = ""

    currpl = 1
    currplname = ""
    currplsym = ""
    currturnmsg = ""

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
        Player.currplcolor = Player.pl1color
        Player.currturnmsg = Player.pl1turnmsg
        GamePage.turnlabel.config(text=Player.currturnmsg)
    
    # switch player turns
    def switchplayer():
        if Player.currpl == 1:
            Player.currpl = 2
            Player.currplname = Player.player2
            Player.currplcolor = Player.pl2color
            Player.currturnmsg = Player.pl2turnmsg
        else:
            Player.currpl = 1
            Player.currplname = Player.player1
            Player.currplcolor = Player.pl1color
            Player.currturnmsg = Player.pl1turnmsg

# Class to show the result of the game
class ResultPage(Frame):
    result = None
    # Show the page
    def __init__(self, container, controller):
        super().__init__(container)
        self.config(background="#d400ff")
        ResultPage.result = Label(self, text = "", font=("Console", 18, "bold"), border=0, background = "#d400ff", foreground="white")
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
        self.config(background="#d400ff")
        board = Frame(self)
        self.rows = 6
        self.cols = 7
        self.selectedcols = []
        board.pack()
        board.place(relx=0.5, rely=0.52, anchor=CENTER)
        back = Button(self, text="Quit", font=("Roboto", 10, "bold"), width=8, pady=3, border=0, relief='sunken', background="lime", foreground="white", command= lambda: self.terminate(StartPage))
        back.place(relx=0.105, rely=0.05, anchor=CENTER)
        GamePage.turnlabel = Label(self, text="", font=("Roboto", 11, "bold"), background="#d400ff", foreground="White")
        GamePage.turnlabel.place(relx=0.5, rely=0.05, anchor=CENTER)
        # Initialize all the parameters of the game
        self.winflag = False
        self.selectedcols = []
        self.boardstates = self.createEmpty(0)
        self.cellobjs = self.createEmpty(None)
        self.winstates = [ [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6] ]
        self.drawboard(board)
    
    def createEmpty(self, val):
        box = []
        for i in range(self.rows):
            empty = []
            for j in range(self.cols):
                empty.append(val)
            box.append(empty)
        return box

    # clear all the parameters after quiting 
    def cleargamestates(self):
        self.boardstates = self.createEmpty(0)
        self.winflag = False
        self.selectedcols = []
        for rowball in self.cellobjs:
            for colball in rowball:
                colball.config(foreground="gray")

    # Terminaate the current game 
    def terminate(self, page):
        # self.cleargamestates()
        self.controller.switchpage(page)
        t = Timer(0.5, self.cleargamestates)
        t.start()

    # Check for win 
    def checkwin(self, player):
        # Minimizing the naming complexity
        bs = self.boardstates

        # Vertical neighbour
        for i in range(self.rows):
            for j in range(self.cols - 3):
                if bs[i][j] == player and bs[i][j+1] == player and bs[i][j+2] == player and bs[i][j+3] == player:
                    return True

        # Horizontal neighbour
        for i in range(self.cols):
            for j in range(self.rows - 3):
                if bs[j][i] == player and bs[j+1][i] == player and bs[j+2][i] == player and bs[j+3][i] == player:
                    return True

        # LeftToRight Diagonal neighbour
        for i in range(self.rows-3, self.rows):
            for j in range(self.cols-1, self.cols-4, -1):
                if bs[i][j] == player and bs[i-1][j-1] == player and bs[i-2][j-2] == player and bs[i-3][j-3] == player:
                    return True

        # RightToLeft Diagonal neighbour
        for i in range(self.rows-3, self.rows):
            for j in range(self.cols - 3):
                if bs[i][j] == player and bs[i-1][j+1] == player and bs[i-2][j+2] == player and bs[i-3][j+3] == player:
                    return True
                
        return False
    
    # Get results of winner
    def getwinresult(self):
        winmsg = Player.winner + " Won!"
        return winmsg

    # For 1 player - computer guess
    def getcomputermove(self):
        while True:
            choose = random.randint(0, self.cols-1)
            if choose not in self.selectedcols:
                break
        return choose
    
    # Provides game actions duing game play
    def gameactions(self, col):
        if col != 0 and col in self.selectedcols:
            return
        
        # for 2 player mode
        if Player.pltype == 2 :
            self.activecell(col)
        # for 1 player mode
        else:
            # when player 2 turn - computer guess
            if Player.currpl == 2:
                n = self.getcomputermove()
                self.activecell(n)
            # for player 1 guess wait
            else:
                self.activecell(col)
                t = Timer(1, lambda: self.gameactions(0))
                t.start()
                
        print(self.boardstates)

        # check for the win 
        if self.checkwin(Player.currpl):
            # declare winner
            if Player.currpl == 1:
                Player.winner = Player.player1
            else:
                Player.winner = Player.player2

            # move to next page and set result
            result = self.getwinresult()
            ResultPage.setresult(result)
            self.cleargamestates()
            self.controller.switchpage(ResultPage)
            return
        
        # Check for tie
        if len(self.selectedcols) == self.cols:
            ResultPage.setresult("It's a tie!")
            self.cleargamestates()
            self.controller.switchpage(ResultPage)

        # switch player if no draw no win
        Player.switchplayer()
        # set turn message
        GamePage.turnlabel.config(text=Player.currturnmsg)
    
    def getinsertindex(self, col):
        c = 0
        i = self.rows - 1
        while i >= 0:
            if self.boardstates[i][col] != 0:
                c = c + 1
            i = i - 1
        c = self.rows - 1 - c
        if c == 0:
            self.selectedcols.append(col)
        return c

    # scratch on the cell - O or X
    def activecell(self, col):
        row = self.getinsertindex(col)
        if self.boardstates[row][col] != 0:
            return 
        self.boardstates[row][col] = Player.currpl
        self.cellobjs[row][col].config(foreground = Player.currplcolor)

    # draw the board for play
    def drawboard(self, container):
        for i in range(self.rows):
            rowballs = []
            for j in range(self.cols):
                cell = Button(container, text = Player.symbol, font = ("Console", 35), height=1, width=3, border=1, background = "white", foreground="gray", relief='sunken', command = lambda col = j: self.gameactions(col))
                cell.grid(row = i, column = j, sticky = "nsew")
                rowballs.append(cell)
            self.cellobjs[i] = rowballs

# Start page for user options and game modes
class StartPage(Frame):
    def __init__(self, container, controller):
        super().__init__(container, background="#ff9800")
        header = Frame(self, height = 100, width = 700, background="#ff9800")
        header.pack(anchor="n") 
        toppane = Frame(self, background="#ff9800")
        toppane.config(height = 310, width = 700)
        toppane.pack(anchor = "center")
        img = ImageTk.PhotoImage(Image.open("media/wel.png"))
        imagecon = Label(toppane, image = img, borderwidth=0)
        imagecon.dontloseit = img
        imagecon.pack(anchor=CENTER)
        downpane = Frame(self)
        downpane.config(height = 320, width = 700, background = "#ff9800")
        downpane.pack(anchor = "w")
        welcon = Label(downpane, text = "Let's Play!", font=("Console", 22, "bold"), borderwidth=0, background = "#ff9800", foreground="white")
        welcon.place(relx=0.5, rely=0.1, anchor=CENTER)
        oneplayer = Button(downpane, text="1 Player", font=("Roboto", 12, "bold"), width=10, pady=5, border=0, relief='sunken', background="#d400ff", foreground="white", command= lambda: self.start(controller, GamePage, 1))
        oneplayer.place(relx=0.40, rely=0.35, anchor=CENTER)
        twoplayer = Button(downpane, text="2 Player", font=("Roboto", 12, "bold"), width=10, pady=5, border=0, relief='sunken', background="#d400ff", foreground="white", command= lambda: self.start(controller, GamePage, 2))
        twoplayer.place(relx=0.60, rely=0.35, anchor=CENTER)
    
    # start the game
    def start(self, controller, page, pltype):
        Player(pltype)
        controller.switchpage(page)

# App
class Connect4App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Connect 4")
        self.geometry("700x650")
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
    app = Connect4App()
    app.mainloop()