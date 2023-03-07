from roboart import *

roboart = RoboArt()

line1 = [(30, 30), (50, 50)]
roboart.draw_line(line1, BrushColors.red)

line2 = [(30, 50), (50, 30)]
roboart.draw_line(line2, BrushColors.blue)

roboart.visualize()
