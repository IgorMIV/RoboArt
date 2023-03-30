import euclid
import matplotlib.pyplot as plt
import math
import numpy as np
from subprocess import check_output
from khirolib import *


# sheet_a4 = [(0, 0), (0, 297), (210, 297), (210, 0), (0, 0)]
sheet_a4 = [(0, 0), (0, 210), (297, 210), (297, 0), (0, 0)]
brush_diameter = 5
safety_z = 150
unsafety_z = 50

safety_speed = 200
drawing_speed = 20

canvas_coordinate_system = (752, -70, -397, 0, 0, 90)
paints_coordinate_system = (743, -249, -397, 0, 0, 90)
canvas_vec = euclid.Vector2(canvas_coordinate_system[0], canvas_coordinate_system[1])
paints_vec = euclid.Vector2(paints_coordinate_system[0], paints_coordinate_system[1])

home_position = (0, 0, safety_z)  # in canvas_coordinate_system

# paints coordinate system
water_pos = (45, 50, 88)
water_pos_safe = (45, 50, safety_z)
water_amplitude = 20

white_pos = (68, 161, 109)
green_pos = (23, 111, 107)
red_pos = (68, 111, 109)
blue_pos = (23, 162, 109)
black_pos = (23, 210, 109)
yellow_pos = (68, 212, 109)

water_vec = euclid.Vector2(water_pos[0], water_pos[1])
white_vec = euclid.Vector2(white_pos[0], white_pos[1])
green_vec = euclid.Vector2(green_pos[0], green_pos[1])
red_vec = euclid.Vector2(red_pos[0], red_pos[1])
blue_vec = euclid.Vector2(blue_pos[0], blue_pos[1])
black_vec = euclid.Vector2(black_pos[0], black_pos[1])
yellow_vec = euclid.Vector2(yellow_pos[0], yellow_pos[1])


delta_cs = ()
for i in range(len(canvas_coordinate_system)):
    delta_cs += (canvas_coordinate_system[i] - paints_coordinate_system[i],)


def get_str(fl):
    return f"{fl:.2f}"


def dist_points(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def generate_pos_from_tuple(tpl, z=None):
    tpl = list(tpl)
    if z is not None:
        if len(tpl) > 2:
            tpl[2] = z
        if len(tpl) == 2:
            tpl += (z,)

    tmp_str = "TRANS("
    for coord in tpl:
        if type(coord) == str:
            tmp_str += str(coord) + ", "
        else:
            tmp_str += get_str(coord) + ", "
    tmp_str = tmp_str[:-2] + ")"
    return tmp_str


preparation_text = "water_comp = 0\n" \
                   "canvas_comp = 0\n" \
                   "white_comp = 0\n" \
                   "green_comp = 0\n" \
                   "red_comp = 0\n" \
                   "blue_comp = 0\n" \
                   "black_comp = 0\n" \
                   "yellow_comp = 0\n" \
                   "POINT paints_base = " + generate_pos_from_tuple(paints_coordinate_system) + "\n" \
                   "POINT canvas_base = " + generate_pos_from_tuple(canvas_coordinate_system) + "\n" \
                   "BASE NULL\n" \
                   "BASE paints_base"

# "POINT tool_test = TRANS(39.2, 2.5, 102.6, 0, 230, 90)\n" \
# "TOOL tool_test\n"

clean_brush_text =\
    "BASE NULL\n" \
    "BASE paints_base\n" \
    "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
    "ACCURACY 3 ALWAYS\n" \
    "POINT cur_pos = HERE\n" \
    "POINT cur_pos_safe = TRANS(DX(cur_pos), DY(cur_pos), " + str(safety_z) + ")\n" \
    "LMOVE cur_pos_safe\n" \
    "POINT water_pos_safe = " + generate_pos_from_tuple(water_pos_safe) + "\n" \
    "LMOVE water_pos_safe\n" \
    "POINT water_pos = " + generate_pos_from_tuple(water_pos) + "\n" \
    "POINT water_pos_r = TRANS(DX(water_pos), DY(water_pos), DZ(water_pos) + water_comp)\n" \
    "POINT water_pos_cl1 = TRANS(DX(water_pos), DY(water_pos), 130)\n" \
    "POINT water_pos_cl2 = TRANS(DX(water_pos), DY(water_pos)-50, 130)\n" \
    "POINT water_pos_cl3 = TRANS(DX(water_pos), DY(water_pos)-50, " + str(safety_z) + ")\n" \
    "POINT water_pos_r_1 = TRANS(DX(water_pos), " \
                                "DY(water_pos) + " + str(water_amplitude) + ", " \
                                "DZ(water_pos) + water_comp," \
                                "10,0,0)\n" \
    "POINT water_pos_r_2 = TRANS(DX(water_pos), " \
                                "DY(water_pos) - " + str(water_amplitude) + ", " \
                                "DZ(water_pos) + water_comp," \
                                "-10,0,0)\n" \
    "POINT water_pos_r_3 = TRANS(DX(water_pos) - " + str(water_amplitude) + ", " \
                                "DY(water_pos), " \
                                "DZ(water_pos) + water_comp," \
                                "0,10,0)\n" \
    "POINT water_pos_r_4 = TRANS(DX(water_pos) + " + str(water_amplitude) + ", " \
                                "DY(water_pos), " \
                                "DZ(water_pos) + water_comp," \
                                "0,-10,0)\n" \
    "CP ON\n" \
    "LMOVE water_pos_r\n" \
    "SPEED 160 mm/s ALWAYS\n" \
    "LMOVE water_pos_r_1\n" \
    "LMOVE water_pos_r_4\n" \
    "LMOVE water_pos_r_2\n" \
    "LMOVE water_pos_r_3\n" \
    "LMOVE water_pos_r_1\n" \
    "LMOVE water_pos_r_4\n" \
    "LMOVE water_pos_r_2\n" \
    "LMOVE water_pos_r_3\n" \
    "LMOVE water_pos_r_1\n" \
    "LMOVE water_pos_r_4\n" \
    "LMOVE water_pos_r_2\n" \
    "LMOVE water_pos_r_3\n" \
    "LMOVE water_pos_r\n" \
    "CP OFF\n" \
    "SPEED 50 mm/s ALWAYS\n" \
    "LMOVE water_pos_cl1 \n" \
    "LMOVE water_pos_cl2 \n" \
    "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
    "LMOVE water_pos_cl3 \n" \
    "LMOVE water_pos_safe\n" \
    "CP ON\n" \
    "LMOVE water_pos_r\n" \
    "SPEED 160 mm/s ALWAYS\n" \
    "LMOVE water_pos_r_1\n" \
    "LMOVE water_pos_r_4\n" \
    "LMOVE water_pos_r_2\n" \
    "LMOVE water_pos_r_3\n" \
    "LMOVE water_pos_r_1\n" \
    "LMOVE water_pos_r_4\n" \
    "LMOVE water_pos_r_2\n" \
    "LMOVE water_pos_r_3\n" \
    "LMOVE water_pos_r_1\n" \
    "LMOVE water_pos_r_4\n" \
    "LMOVE water_pos_r_2\n" \
    "LMOVE water_pos_r_3\n" \
    "LMOVE water_pos_r\n" \
    "CP OFF\n" \
    "SPEED 50 mm/s ALWAYS\n" \
    "LMOVE water_pos_cl1 \n" \
    "LMOVE water_pos_cl2 \n" \
    "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
    "LMOVE water_pos_cl3 \n" \
    "LMOVE water_pos_safe"


class BrushColors:
    white = 'white'
    green = 'green'
    red = 'red'
    blue = 'blue'
    black = 'black'
    yellow = 'yellow'

    list_of_colors = [[255, 255, 255], [0, 255, 0], [255, 0, 0], [0, 0, 255], [0, 0, 0], [255, 255, 0]]

    @staticmethod
    def closest_color(color):
        r = color[1:3]
        g = color[3:5]
        b = color[5:7]
        color = [int(r, 16), int(g, 16), int(b, 16)]

        colors = np.array(BrushColors.list_of_colors)
        color = np.array(color)
        distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        smallest_distance = colors[index_of_smallest]
        color_index = BrushColors.list_of_colors.index(list(smallest_distance[0]))

        if color_index == 0:
            return BrushColors.white
        if color_index == 1:
            return BrushColors.green
        if color_index == 2:
            return BrushColors.red
        if color_index == 3:
            return BrushColors.blue
        if color_index == 4:
            return BrushColors.black
        if color_index == 5:
            return BrushColors.yellow


def generate_take_color_text(color: BrushColors):
    if color == BrushColors.white:
        color_pos = white_pos
        compensation = 'white_comp'
    if color == BrushColors.green:
        color_pos = green_pos
        compensation = 'green_comp'
    if color == BrushColors.red:
        color_pos = red_pos
        compensation = 'red_comp'
    if color == BrushColors.blue:
        color_pos = blue_pos
        compensation = 'blue_comp'
    if color == BrushColors.black:
        color_pos = black_pos
        compensation = 'black_comp'
    if color == BrushColors.yellow:
        color_pos = yellow_pos
        compensation = 'yellow_comp'

    text = \
    "BASE NULL\n" \
    "BASE paints_base\n" \
    "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
    "ACCURACY 1 ALWAYS\n" \
    "POINT cur_pos = HERE\n" \
    "POINT cur_pos_safe = TRANS(DX(cur_pos), DY(cur_pos), " + str(safety_z) + ")\n" \
    "LMOVE cur_pos_safe\n" \
    "POINT .tmp_pos_safe = " + generate_pos_from_tuple(color_pos, z=safety_z) + "\n" \
    "LMOVE .tmp_pos_safe\n" \
    "POINT .tmp_pos = " + generate_pos_from_tuple(color_pos) + "\n" \
    "POINT .tmp_pos_r = TRANS(DX(.tmp_pos), DY(.tmp_pos), DZ(.tmp_pos) + " + compensation +")\n" \
    "LMOVE .tmp_pos_r\n" \
    "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
    "LMOVE .tmp_pos_safe"

    return text


class OperationType:
    Line = 'Line'
    Point = 'Point'
    CleanBrush = 'CleanBrush'
    ChangeColor = 'ChangeColor'


class DrawingOperation:
    def __init__(self, color: BrushColors, o_type: OperationType, data=None):
        self.points = data
        self.color = color
        self._type = o_type
        self._distance = 0

        if self._type == OperationType.Line:
            for i in range(len(self.points)-1):
                self._distance += math.sqrt((self.points[i][0]-self.points[i+1][0]) ** 2 +
                                            (self.points[i][1]-self.points[i+1][1]) ** 2)

    @property
    def x(self):
        if self._type == OperationType.Line:
            x, y = zip(*self.points)
            return x
        if self._type == OperationType.Point:
            return self.points[0]

    @property
    def y(self):
        if self._type == OperationType.Line:
            x, y = zip(*self.points)
            return y
        if self._type == OperationType.Point:
            return self.points[1]

    @property
    def last_point(self):
        if self._type == OperationType.Line:
            last_point = self.points[-1]
            return last_point
        if self._type == OperationType.Point:
            last_point = self.points
            return last_point
        if self._type == OperationType.CleanBrush:
            last_point = self.points
            return last_point

    @property
    def last_point_global(self):
        if self._type == OperationType.Line:
            last_point = euclid.Vector2(self.points[-1][0], self.points[-1][1])
            return paints_vec + last_point
        if self._type == OperationType.Point:
            last_point = euclid.Vector2(self.points[0], self.points[1])
            return paints_vec + last_point
        if self._type == OperationType.CleanBrush:
            return paints_vec + water_vec
        if self._type == OperationType.ChangeColor:
            if self.color == BrushColors.white:
                return paints_vec + white_vec
            if self.color == BrushColors.green:
                return paints_vec + green_vec
            if self.color == BrushColors.red:
                return paints_vec + red_vec
            if self.color == BrushColors.blue:
                return paints_vec + blue_vec
            if self.color == BrushColors.black:
                return paints_vec + black_vec
            if self.color == BrushColors.yellow:
                return paints_vec + yellow_vec

    @property
    def type(self):
        return self._type

    @property
    def distance(self):
        return self._distance


class RoboArt:
    def __init__(self):
        self._lines = []
        self._paint_distance = 0

        self._current_brush_color = None

    def draw_line(self, line):
        line_copy = line.copy()
        self.get_previous_point
        assert self._current_brush_color is not None, "You are not set brush color"

        "You are not set or change brush color"
        drawing_operation = DrawingOperation(self._current_brush_color, OperationType.Line, data=line_copy)
        self._paint_distance += drawing_operation.distance
        self._lines.append(drawing_operation)

    def draw_point(self, point):
        self.get_previous_point

        assert self._current_brush_color is not None, "You are not set brush color"

        drawing_operation = DrawingOperation(self._current_brush_color, OperationType.Point, data=point)
        self._paint_distance += drawing_operation.distance
        self._lines.append(drawing_operation)

    def clean_brush(self):
        drawing_operation = DrawingOperation(None, OperationType.CleanBrush)
        self._lines.append(drawing_operation)
        self._current_brush_color = None

    def take_paint(self, color):
        assert (self._current_brush_color is None) or (self._current_brush_color == color), "Your brush is not clear"

        self._current_brush_color = color
        drawing_operation = DrawingOperation(self._current_brush_color, OperationType.ChangeColor)
        self._lines.append(drawing_operation)

    def visualize(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        sheet_x, sheet_y = zip(*sheet_a4)
        plt.plot(sheet_x, sheet_y, '-', color='black')

        for drawing_object in self._lines:
            if drawing_object.type == OperationType.Line:
                plt.plot(drawing_object.x, drawing_object.y, '-', color=drawing_object.color, lw=brush_diameter)

            if drawing_object.type == OperationType.Point:
                plt.scatter(drawing_object.x, drawing_object.y, color=drawing_object.color, s=brush_diameter*5)

        ax.set_aspect('equal')
        plt.show()

    def export_rcp(self):
        program_text = "BASE NULL\n" \
                       "BASE canvas_base\n" \
                       "SPEED " + str(safety_speed) + " mm/s ALWAYS\n"
        # "POINT home_position = " + generate_pos_from_tuple(home_position) + "\n" + \
        # "LMOVE home_position\n"

        for element in self._lines:
            if element.type == OperationType.Line:
                if self.get_previous_object_type(element) == OperationType.Line:
                    height_z = unsafety_z
                else:
                    height_z = safety_z

                program_text += "BASE NULL\n" \
                       "BASE canvas_base\n" \
                       "ACCURACY 1 ALWAYS\n" \
                       "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
                       "POINT cur_pos = HERE\n" \
                       "POINT cur_pos_safe = TRANS(DX(cur_pos), DY(cur_pos), " + str(height_z) + ")\n" \
                       "LMOVE cur_pos_safe\n"

                trajectory_points = element.points
                program_text += "POINT start_up = " + generate_pos_from_tuple(trajectory_points[0], z=height_z) + "\n" \
                                "LMOVE start_up\n" \
                                "POINT start_down = " + generate_pos_from_tuple(trajectory_points[0], z='canvas_comp') + "\n" \
                                "LMOVE start_down\n" \
                                "SPEED " + str(drawing_speed) + " mm/s ALWAYS\n"

                if len(trajectory_points) < 20:
                    for point in trajectory_points[1:]:
                        program_text += "POINT pnt = " + generate_pos_from_tuple(point, z='canvas_comp') + "\n" \
                                        "LMOVE pnt\n"
                else:
                    counter = 0
                    for point in trajectory_points[1:]:
                        program_text += "POINT .pnt" + str(counter) + " = " + \
                                        generate_pos_from_tuple(point, z='canvas_comp') + "\n"
                        counter += 1

                    program_text += "CP ON\n"
                    counter = 0
                    for point in trajectory_points[1:]:
                        program_text += "LMOVE .pnt" + str(counter) + "\n"
                        counter += 1
                    program_text += "CP OFF\n"

            if element.type == OperationType.Point:
                program_text += "BASE NULL\n" \
                                "BASE canvas_base\n" \
                                "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
                                "POINT cur_pos = HERE\n" \
                                "POINT cur_pos_safe = TRANS(DX(cur_pos), DY(cur_pos), " + str(safety_z) + ")\n" \
                                "LMOVE cur_pos_safe\n"

                trajectory_point = element.points
                program_text += "POINT start_up = " + generate_pos_from_tuple(trajectory_point, z=safety_z) + "\n" \
                                "LMOVE start_up\n" \
                                "POINT .pnt = " + generate_pos_from_tuple(trajectory_point, z='canvas_comp-2') + "\n" \
                                "LMOVE .pnt\n" \
                                "TWAIT 0.2\n" \
                                "LMOVE start_up\n"

            if element.type == OperationType.CleanBrush:
                program_text += "CALL cleanbrush\n"

            if element.type == OperationType.ChangeColor:
                if element.color == BrushColors.white:
                    program_text += "CALL takewhite\n"

                if element.color == BrushColors.green:
                    program_text += "CALL takegreen\n"

                if element.color == BrushColors.red:
                    program_text += "CALL takered\n"

                if element.color == BrushColors.blue:
                    program_text += "CALL takeblue\n"

                if element.color == BrushColors.black:
                    program_text += "CALL takeblack\n"

                if element.color == BrushColors.yellow:
                    program_text += "CALL takeyellow\n"

        return program_text

    def calculate_distance(self):
        full_dist = 0
        for element in self._lines:
            prev_point = self.get_prev_point_global(element)
            if prev_point is not None:
                if element.type == OperationType.Line:
                    first_point = canvas_vec + euclid.Vector2(element.points[0][0], element.points[0][1])
                    full_dist += abs(first_point - prev_point)
                    full_dist += element.distance

                if element.type == OperationType.Point:
                    first_point = canvas_vec + euclid.Vector2(element.points[0], element.points[1])
                    full_dist += abs(first_point - prev_point)

                if element.type == OperationType.CleanBrush:
                    first_point = paints_vec + water_vec
                    full_dist += abs(first_point - prev_point)

                if element.type == OperationType.ChangeColor:
                    color_vec = None
                    if element.color == BrushColors.white:
                        color_vec = paints_vec + white_vec
                    if element.color == BrushColors.green:
                        color_vec = paints_vec + green_vec
                    if element.color == BrushColors.red:
                        color_vec = paints_vec + red_vec
                    if element.color == BrushColors.blue:
                        color_vec = paints_vec + blue_vec
                    if element.color == BrushColors.black:
                        color_vec = paints_vec + black_vec
                    if element.color == BrushColors.yellow:
                        color_vec = paints_vec + yellow_vec

                    full_dist += abs(color_vec - prev_point)
        return full_dist, self._paint_distance

    def paint(self):
        f = open("/home/available_users", "r")
        users_list = f.read().split('\n')

        current_user = check_output(['/usr/bin/whoami']).strip().decode()
        if current_user in users_list:
            IP = "192.168.1.11"
            PORT = 23
            robot = khirolib(IP, PORT, connection_mode='single')

            painting = self.export_rcp()
            robot.upload_program(program_name="painting", program_text=painting)
            robot.execute_rcp("painting")
        else:
            print("Printing is not available now for your user")

    def get_program_text(self):
        program_text = self.export_rcp()
        return program_text

    def get_init_script():
        return preparation_text

    def get_cleanbrush_script():
        return clean_brush_text

    def get_takecolor_script(brush_color):
        return generate_take_color_text(brush_color)

    @property
    def get_previous_point(self):
        if len(self._lines) > 0:
            return self._lines[-1].last_point
        else:
            return None

    def get_previous_object_type(self, element):
        index = self._lines.index(element)
        if index > 0:
            return self._lines[index-1].type
        else:
            return None

    def get_prev_point_global(self, element):
        index = self._lines.index(element)
        if len(self._lines) > 0:
            return self._lines[index-1].last_point_global
        else:
            return None

