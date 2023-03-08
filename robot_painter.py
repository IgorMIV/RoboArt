from roboart import *

roboart = RoboArt()

# roboart.take_paint(BrushColors.red)

line1 = [(50, 50), (30, 30)]
roboart.draw_line(line1, BrushColors.red)

roboart.take_paint(BrushColors.blue)

line2 = [(30, 50), (50, 30)]
roboart.draw_line(line2, BrushColors.blue)

roboart.take_paint(BrushColors.green)

line2 = [(100, 100), (60, 30), (90, 20)]
roboart.draw_line(line2, BrushColors.green)

roboart.draw_point((110, 130), BrushColors.green)

roboart.draw_point((90, 95), BrushColors.green)

print("Full distance:", roboart.distance)

roboart.visualize()
