from roboart import *


roboart = RoboArt()

roboart.clean_brush()
roboart.take_paint(BrushColors.red)
line1 = [(70, 150), (100, 90)]
roboart.draw_line(line1)

# roboart.clean_brush()
# roboart.take_paint(BrushColors.blue)
# line2 = [(60, 50), (60, 30)]
# roboart.draw_line(line2)

roboart.clean_brush()
roboart.take_paint(BrushColors.green)
line2 = [(200, 200), (150, 130), (90, 20)]
roboart.draw_line(line2)

# roboart.clean_brush()
# roboart.take_paint(BrushColors.black)
# roboart.draw_point((110, 130))
# roboart.draw_point((90, 95))

roboart.clean_brush()

# roboart.visualize()

full, paint = roboart.calculate_distance()
print("Full:", full, "Paint:", paint)

program_text = roboart.get_program_text()
file = open("programfile.txt", "w")
file.write(program_text)
file.close()

# roboart.paint()