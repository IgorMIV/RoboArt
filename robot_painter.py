from roboart import *
# from khirolib import *

roboart = RoboArt()

roboart.take_paint(BrushColors.red)
line1 = [(50, 50), (30, 30)]
roboart.draw_line(line1)

# roboart.clean_brush()
# roboart.take_paint(BrushColors.blue)
line2 = [(30, 50), (50, 30)]
roboart.draw_line(line2)

roboart.clean_brush()
roboart.take_paint(BrushColors.green)
line2 = [(100, 100), (60, 30), (90, 20)]
roboart.draw_line(line2)

roboart.clean_brush()
roboart.take_paint(BrushColors.black)
roboart.draw_point((110, 130))
roboart.draw_point((90, 95))

print("Full distance:", roboart.distance)

roboart.visualize()

# IP = "192.168.1.11"    # IP for K-Roset
# PORT = 23         # Port for K-Roset
# robot = khirolib(IP, PORT, connection_mode='single', log=True)
# robot.upload_program(program_name="init_prog", program_text=RoboArt.get_init_script())
# robot.execute_rcp("init_prog")
# robot.upload_program(program_name="cleanbrush", program_text=RoboArt.get_cleanbrush_script())

# painting = roboart.export_rcp()
# robot.upload_program(program_name="painting", program_text=painting)
# robot.execute_rcp("painting")
