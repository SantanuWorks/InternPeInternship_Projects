import tkinter as TK
from time import strftime
import math

app = TK.Tk()
app.title("FirstApp")

WIDTH = 400
HEIGHT = 400

h = HEIGHT/2
k = WIDTH/2

sec_theta, min_theta, hr_theta = 0, 0, 0

sec_rad, min_rad, hr_rad = 180, 150, 100

sec_x, sec_y, min_x, min_y, hr_x, hr_y = 0, 0, 0, 0, 0, 0

canvas = TK.Canvas(app, height=HEIGHT, width=WIDTH, background="red")
canvas.pack()

clocklabel = TK.Label(app, width=WIDTH, font=('calibri', 35, 'bold'), background="purple", foreground="white")
clocklabel.pack(anchor="center")

def draw_dial():
    canvas.create_oval(0, 0, HEIGHT, WIDTH, width=0, fill="blue", outline="white")
    draw_hands()

def draw_hands():
    sec_x = sec_rad * math.cos(sec_theta) + h
    sec_y = sec_rad * math.sin(sec_theta) + k
    
    min_x = min_rad * math.cos(min_theta) + h
    min_y = min_rad * math.sin(min_theta) + k
    
    hr_x = hr_rad * math.cos(hr_theta) + h
    hr_y = hr_rad * math.sin(hr_theta) + h

    canvas.create_line(h, k, sec_x, sec_y, smooth=True)
    canvas.create_line(h, k, min_x, min_y, smooth=True)
    canvas.create_line(h, k, hr_x, hr_y, smooth=True)

def SetTime():
    second = int(strftime("%S"))
    minute = int(strftime("%M"))
    hour = int(strftime("%H"))

    global sec_theta, min_theta, hr_theta
    
    sec_theta = math.radians(second * 6) - math.radians(90)
    min_theta = math.radians(minute * 6) - math.radians(90)
    hr_theta = math.radians(hour * 6) - math.radians(90)
    
    draw_dial()
    
    timestr = strftime("%H : %M : %S %p")
    clocklabel.config(text=timestr)
    clocklabel.after(1000, SetTime)

SetTime()

app.mainloop()