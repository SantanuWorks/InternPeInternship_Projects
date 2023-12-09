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