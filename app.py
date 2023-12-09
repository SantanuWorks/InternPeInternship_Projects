# Required modules
from tkinter import * # GUI interface
from time import strftime # Time utility
import math # Calculate point on circle

# Defining some colors 
RED = "Red"
BLACK = "Black"

# Defining height and width of clock body
HEIGHT = 400
WIDTH = 400

# Creating main window of clock application
ClockApp = Tk()

# Set name of the window
ClockApp.title("Hybrid Clock")

# Defining the minimum and maximum window size
ClockApp.minsize(460, 470)
ClockApp.maxsize(460, 470)

# Defiing clock body
ClockBody = Frame(ClockApp)
ClockBody.pack()

# defining clock dial - circular base
ClockDial = Canvas(ClockBody, height = HEIGHT, width = WIDTH)
ClockDial.pack(side = TOP)

# Defining digital display - digital interface
ClockDigitalDisplay = Label(ClockBody, font = ("ds-digital", 35), foreground = RED)
ClockDigitalDisplay.pack(side = BOTTOM)

'''

Concept for clock design:
-------------------------
Assuming clock as a circle on a graph, whose center is at (h, k)
Assuming clock hands i.e. second hand, minute hand and hour hand as lines on graph

Working of clock:
-----------------
Movement of clock hands can be realize as rotation of lines on circle around the center (h, k)
For each second, minute and hour, hands will rotate about 6 deg

angle = 6deg * time (sec/min/hr) 

One end of the line is at (h, k) and other end of the line at (x, y)
W.r.t each unit increase in time will change the (x, y) for the respective lines

Here, x = radius x cos(angle) + h
      y = radius x sin(angle) + k

angle in radian, radius is length of the line/hand

since, center is not at (0, 0), we have to add current center positions

'''


# Defining clock controller class
# Provides contraints and logic working of clock
class ClockController:
    # 
    h = HEIGHT/2
    k = WIDTH/2

    sec_rad = 180
    min_rad = 150
    hrr_rad = 100

    sec_theta = 0 
    min_theta = 0 
    hr_theta = 0
    
    def DrawClockDial(self):
        self.ClockDial.create_oval(10, 10, HEIGHT-10, WIDTH-10, fill = BLACK)
    
    def CalXYOnCircle():
        sec_x = ClockController.sec_rad * math.cos(ClockController.sec_theta) + ClockController.h
        sec_y = ClockController.sec_rad * math.sin(ClockController.sec_theta) + ClockController.k
        

    def DrawClockHands(self):
        
        second = int(strftime("%S"))
        minute = int(strftime("%M"))
        hour = int(strftime("%H"))
        
        sec_theta = math.radians(second * 6) - math.radians(90)
        min_theta = math.radians(minute * 6) - math.radians(90)
        hr_theta = math.radians(hour * 6) - math.radians(90)
        
        sec_x = ClockController.sec_rad * math.cos(ClockController.sec_theta) + ClockController.h
        sec_y = ClockController.sec_rad * math.sin(ClockController.sec_theta) + ClockController.k
        
        min_x = ClockController.min_rad * math.cos(ClockController.min_theta) + ClockController.h
        min_y = ClockController.min_rad * math.sin(ClockController.min_theta) + ClockController.k
        
        hr_x = ClockController.hrr_rad * math.cos(ClockController.hr_theta) + ClockController.h
        hr_y = ClockController.hrr_rad * math.sin(ClockController.hr_theta) + ClockController.h

        ClockDial.create_line(ClockController.h, ClockController.k, sec_x, sec_y, smooth = True)
        ClockDial.create_line(ClockController.h, ClockController.k, min_x, min_y, smooth = True)
        ClockDial.create_line(ClockController.h, ClockController.k, hr_x, hr_y, smooth = True)

    def Run(self):
        timestr = strftime("%H : %M : %S %p")
        ClockController.DrawClockHands()
        ClockDigitalDisplay.config(text = timestr)
        ClockBody.after(1000, self.Run)
        

# Initalizing the clock controller object
Clock = ClockController(ClockBody, ClockDial, ClockDigitalDisplay)

# Draw the clock dial
Clock.DrawClockDial()

# Start the clock
Clock.Run()

# Keep running the window
ClockApp.mainloop()