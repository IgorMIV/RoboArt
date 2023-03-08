import matplotlib.pyplot as plt
import math

sheet_a4 = [(0, 0), (0, 297), (210, 297), (210, 0), (0, 0)]
brush_diameter = 5
safety_z = 100

canvas_coordinate_system = (500, 500, 0, 0, 0, 0)
paints_coordinate_system = (800, 500, 0, 0, 0, 0)

delta_cs = ()
for i in range(len(canvas_coordinate_system)):
    delta_cs += (canvas_coordinate_system[i] - paints_coordinate_system[i],)


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

    def draw_line(self, line, color):
        self.get_previous_point

        if self._current_brush_color is None:
            self.take_paint(color)
        assert self._current_brush_color == color, "You are not set or change brush color"

        drawing_operation = DrawingOperation(color, OperationType.Line, data=line)
        self._full_distance += drawing_operation.distance
        self._lines.append(drawing_operation)

    def draw_point(self, point, color):
        self.get_previous_point

        if self._current_brush_color is None:
            self.take_paint(color)
        assert self._current_brush_color == color, "You are not set or change brush color"

        drawing_operation = DrawingOperation(color, OperationType.Point, data=point)
        self._full_distance += drawing_operation.distance
        self._lines.append(drawing_operation)

    def take_paint(self, color):
        print(self.get_previous_point)
        self._current_brush_color = color
        drawing_operation = DrawingOperation(color, OperationType.ChangeColor)
        # self._full_distance += drawing_operation.distance
        self._lines.append(drawing_operation)

    def clean_brush(self):
        pass

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
        pass

    @property
    def distance(self):
        return self._full_distance

    @property
    def get_previous_point(self):
        if len(self._lines) > 0:
            return self._lines[-1].last_point
        else:
            return None
