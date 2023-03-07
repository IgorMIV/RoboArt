import matplotlib.pyplot as plt

list_a4 = [(0, 0), (0, 297), (210, 297), (210, 0), (0, 0)]


class BrushColors:
    white = 'white'
    green = 'green'
    red = 'red'
    blue = 'blue'
    black = 'black'
    yellow = 'yellow'


class PictureLine:
    def __init__(self, points, color: BrushColors):
        self.points = points
        self.color = color

    @property
    def x(self):
        x, y = zip(*self.points)
        return x

    @property
    def y(self):
        x, y = zip(*self.points)
        return y


class RoboArt:
    def __init__(self):
        self._lines = []

    def draw_line(self, line, color):
        self._lines.append(PictureLine(line, color))

    def visualize(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        list_x, list_y = zip(*list_a4)
        plt.plot(list_x, list_y, '-', color='black')

        for line in self._lines:
            plt.plot(line.x, line.y, '-', color=line.color)
        
        ax.set_aspect('equal', 'box')
        plt.show()
