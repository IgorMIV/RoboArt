import matplotlib.pyplot as plt
import math

sheet_a4 = [(0, 0), (0, 297), (210, 297), (210, 0), (0, 0)]
brush_diameter = 5
safety_z = 100

safety_speed = 50
drawing_speed = 20

canvas_coordinate_system = (593, -65, -370, 0, 0, 0)
paints_coordinate_system = (595, -107, -370, 0, 0, 0)

home_position = (0, 0, safety_z)  # in canvas_coordinate_system

# paints coordinate system
water_pos = (10, 10, 50)
water_pos_safe = (10, 10, safety_z)
water_amplitude = 20

delta_cs = ()
for i in range(len(canvas_coordinate_system)):
    delta_cs += (canvas_coordinate_system[i] - paints_coordinate_system[i],)


def dist_points(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def generate_pos_from_tuple(tpl, z=None):
    tpl = list(tpl)
    if z is not None:
        if len(tpl) > 2:
            print(tpl)
            tpl[2] = z
        if len(tpl) == 2:
            tpl += (z,)

    tmp_str = "TRANS("
    for coord in tpl:
        tmp_str += str(coord) + ", "
    tmp_str = tmp_str[:-2] + ")"
    return tmp_str


preparation_text = "water_compensation = 0\n" \
                   "canvas_compensation = 0\n" \
                   "white_compensation = 0\n" \
                   "green_compensation = 0\n" \
                   "red_compensation = 0\n" \
                   "blue_compensation = 0\n" \
                   "black_compensation = 0\n" \
                   "yellow_compensation = 0\n" \
                   "POINT tool_test = TRANS(39, 3, 102, 4, 231, -1)\n" \
                   "TOOL tool_test\n" \
                   "POINT paints_base = " + generate_pos_from_tuple(paints_coordinate_system) + "\n" \
                   "POINT canvas_base = " + generate_pos_from_tuple(canvas_coordinate_system)

clean_brush_text =\
    "BASE NULL\n" \
    "BASE paints_base\n" \
    "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
    "ACCURACY 1 ALWAYS\n" \
    "POINT cur_pos = HERE\n" \
    "POINT cur_pos_safe = TRANS(DX(cur_pos), DY(cur_pos), " + str(safety_z) + ")\n" \
    "LMOVE cur_pos_safe\n" \
    "POINT water_pos_safe = " + generate_pos_from_tuple(water_pos_safe) + "\n" \
    "LMOVE water_pos_safe\n" \
    "POINT water_pos = " + generate_pos_from_tuple(water_pos) + "\n" \
    "POINT water_pos_r = TRANS(DX(water_pos), DY(water_pos), DZ(water_pos) + water_compensation)\n" \
    "POINT water_pos_r_1 = TRANS(DX(water_pos) + " + str(water_amplitude) + ", " \
                                "DY(water_pos) + " + str(water_amplitude) + ", " \
                                "DZ(water_pos) + water_compensation)\n" \
    "POINT water_pos_r_2 = TRANS(DX(water_pos) + " + str(water_amplitude) + ", " \
                                "DY(water_pos) - " + str(water_amplitude) + ", " \
                                "DZ(water_pos) + water_compensation)\n" \
    "POINT water_pos_r_3 = TRANS(DX(water_pos) - " + str(water_amplitude) + ", " \
                                "DY(water_pos) - " + str(water_amplitude) + ", " \
                                "DZ(water_pos) + water_compensation)\n" \
    "POINT water_pos_r_4 = TRANS(DX(water_pos) - " + str(water_amplitude) + ", " \
                                "DY(water_pos) + " + str(water_amplitude) + ", " \
                                "DZ(water_pos) + water_compensation)\n" \
    "LMOVE water_pos_r\n" \
    "SPEED 60 mm/s ALWAYS\n" \
    "JMOVE water_pos_r_1\n" \
    "JMOVE water_pos_r_2\n" \
    "JMOVE water_pos_r_3\n" \
    "JMOVE water_pos_r_4\n" \
    "JMOVE water_pos_r\n" \
    "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
    "LMOVE water_pos_safe"


class BrushColors:
    white = 'white'
    green = 'green'
    red = 'red'
    blue = 'blue'
    black = 'black'
    yellow = 'yellow'


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
    def type(self):
        return self._type

    @property
    def distance(self):
        return self._distance


class RoboArt:
    def __init__(self):
        self._lines = []
        self._full_distance = 0

        self._current_brush_color = None

    def draw_line(self, line):
        self.get_previous_point
        assert self._current_brush_color is not None, "You are not set brush color"

        "You are not set or change brush color"
        drawing_operation = DrawingOperation(self._current_brush_color, OperationType.Line, data=line)
        self._full_distance += drawing_operation.distance
        self._lines.append(drawing_operation)

    def draw_point(self, point):
        self.get_previous_point

        assert self._current_brush_color is not None, "You are not set brush color"

        drawing_operation = DrawingOperation(self._current_brush_color, OperationType.Point, data=point)
        self._full_distance += drawing_operation.distance
        self._lines.append(drawing_operation)

    def clean_brush(self):
        drawing_operation = DrawingOperation(None, OperationType.CleanBrush)
        self._lines.append(drawing_operation)
        self._current_brush_color = None

    def take_paint(self, color):
        assert self._current_brush_color is None, "Your brush is not clear"

        if self.get_previous_point is None:
            self._full_distance += dist_points(home_position, delta_cs)

        self._current_brush_color = color
        drawing_operation = DrawingOperation(self._current_brush_color, OperationType.ChangeColor)
        # self._full_distance += drawing_operation.distance
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
                       "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
                       "POINT home_position = " + generate_pos_from_tuple(home_position) + "\n" + \
                       "LMOVE home_position\n"

        for element in self._lines:
            if element.type == OperationType.Line:
                program_text += "BASE NULL\n" \
                       "BASE canvas_base\n" \
                       "SPEED " + str(safety_speed) + " mm/s ALWAYS\n" \
                       "POINT cur_pos = HERE\n" \
                       "POINT cur_pos_safe = TRANS(DX(cur_pos), DY(cur_pos), " + str(safety_z) + ")\n" \
                       "LMOVE cur_pos_safe\n"

                trajectory_points = element.points
                program_text += "POINT start_up = " + generate_pos_from_tuple(trajectory_points[0], z=safety_z) + "\n" \
                                "LMOVE start_up\n" \
                                "POINT start_down = " + generate_pos_from_tuple(trajectory_points[0], z='canvas_compensation') + "\n" \
                                "LMOVE start_down\n" \
                                "SPEED " + str(drawing_speed) + " mm/s ALWAYS\n"

                for point in trajectory_points[1:]:
                    program_text += "POINT pnt = " + generate_pos_from_tuple(point, z='canvas_compensation') + "\n" \
                                    "LMOVE pnt\n"

            if element.type == OperationType.Point:
                pass

            if element.type == OperationType.CleanBrush:
                program_text += "CALL cleanbrush\n"

            if element.type == OperationType.ChangeColor:
                pass

        return program_text

    def get_init_script():
        return preparation_text

    def get_cleanbrush_script():
        return clean_brush_text

    @property
    def distance(self):
        return self._full_distance

    @property
    def get_previous_point(self):
        if len(self._lines) > 0:
            return self._lines[-1].last_point
        else:
            return None
