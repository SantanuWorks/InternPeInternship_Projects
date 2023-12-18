# Import required modules
from tkinter import * # For GUI
import random # for random alloction of food
import time

# App 
class SnakeGameApp(Tk):
    # Initialize all the components of the app
    def __init__(self):
        # Call the parrent Tk()
        super().__init__()

        # Set the window titile, its size and resizability
        self.title("Snakey Snee")
        self.geometry("400x450")
        self.resizable(False, False)

        # define score of the user
        self.score = 0
        # define height and width of the game board
        self.HEIGHT = 400
        self.WIDTH = 400
        # define no of parts in snake body
        self.SNAKEPARTS = 3
        # define size or length of each part
        self.PARTSIZE = 15
        # speed of movement of snake
        self.SPEED = 150

        # define direction of the snake
        self.direction = "right"
        # define coordinates of snake
        self.snakexy = [] 
        # define snake body parts
        self.squares = [] 
        # define food coordinate
        self.foodxy = []

        # create a label for score
        self.scoreboard = Label(self, height=2, width=400, text="Score: "+str(self.score), font=("Console", 15, "bold"), border=0, background="#1a75ff",foreground="white")
        self.scoreboard.pack()

        # create the board for snake
        self.snakeboard = Canvas(self, height=400, width=400, highlightbackground="#1a75ff", background="lime")
        self.snakeboard.pack()

        # create initial snake body
        self.drawsnake()
        # guess initial food position
        self.drawfood()
        # start the game with default parameters
        self.start()

    # create initial body for snake
    def drawsnake(self):
        for i in range(0, self.SNAKEPARTS): 
            self.snakexy.append([0, 0]) 
        for x, y in self.snakexy: 
            square = self.snakeboard.create_rectangle(x, y, x + self.PARTSIZE, y + self.PARTSIZE, fill="yellow", tag="snake") 
            self.squares.append(square)

    # create food positions randomly
    def drawfood(self):
        x = random.randint(0, int(self.WIDTH / self.PARTSIZE)-1) * self.PARTSIZE 
        y = random.randint(0, int(self.HEIGHT / self.PARTSIZE)-1) * self.PARTSIZE 
        self.foodxy = [x, y] 
        self.snakeboard.create_oval(x, y, x + self.PARTSIZE, y + self.PARTSIZE, fill="red", tag="food")
    
    # check whether snake strike to wall or itself
    def iscollision(self):
        x, y = self.snakexy[0] 
        if x < 0 or y < 0 or x >= self.WIDTH or y >= self.HEIGHT:
            return True
        for xy in self.snakexy[1:]:
            if x == xy[0] and y == xy[1]:
                return True
        return False

    # run the game with respect to given parameters for the snake
    def start(self):
        # change the direction of the snake with respect to given arrow
        x, y = self.snakexy[0] 
        if self.direction == "up": 
            y -= self.PARTSIZE 
        elif self.direction == "down": 
            y += self.PARTSIZE 
        elif self.direction == "left": 
            x -= self.PARTSIZE 
        elif self.direction == "right": 
            x += self.PARTSIZE 

        # store new coordinates for the snake
        self.snakexy.insert(0, (x, y)) 
        # store its body parts
        square = self.snakeboard.create_rectangle(x, y, x+self.PARTSIZE, y+self.PARTSIZE, fill="yellow") 
        self.squares.insert(0, square) 

        # if food and head of the snake at same coordinates then increase score, increase snake length, get new food
        if x == self.foodxy[0] and y == self.foodxy[1]: 
            self.score += 1
            self.scoreboard.config(text="Score: "+str(self.score)) 
            self.snakeboard.delete("food") 
            self.drawfood()
        else: 
            del self.snakexy[-1]
            self.snakeboard.delete(self.squares[-1]) 
            del self.squares[-1]
        # check for collision if found then stop the game
        if self.iscollision():
            self.stop()
        # set the speed
        self.after(self.SPEED, self.start)
    
    # stop the game
    def stop(self):
        time.sleep(5)
        # self.snakeboard.delete(ALL) 
        self.snakeboard.create_text(self.WIDTH/2, self.HEIGHT/2, font=('arial', 40), text="Game Over!", fill="red", tag="gameover") 

    # set new direction
    def changedirection(self, dir):
        if (self.direction == "left" and dir == "right") or (self.direction == "right" and dir == "left"):
            return
        if (self.direction == "up" and dir == "down") or (self.direction == "down" and dir == "up"):
            return
        self.direction = dir
# start the app
if __name__ == "__main__":
    app = SnakeGameApp()
    # get user response keys
    app.bind('<Up>', lambda event: app.changedirection('up'))
    app.bind('<Down>', lambda event: app.changedirection('down'))
    app.bind('<Left>', lambda event: app.changedirection('left'))
    app.bind('<Right>', lambda event: app.changedirection('right'))
    app.mainloop()