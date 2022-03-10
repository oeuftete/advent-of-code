from adventofcode.common.coordinate import Coordinate
from adventofcode.common.year2019.intcode_computer import (
    Intcode,
    IntcodeHaltedException,
)

BLACK = 0
WHITE = 1

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class PaintedPanel(Coordinate):
    def __init__(self, x, y, paint_color=BLACK, **kwargs):
        super(PaintedPanel, self).__init__(x, y, **kwargs)
        self.paint_color = paint_color


class PainterRobot(object):
    def __init__(self):
        self.position = Coordinate(0, 0)
        self.direction = UP
        self.outbut_buffer = list()

    def turn(self, turn_direction):
        self.direction += 1 if turn_direction else -1
        self.direction %= 4

    def move(self):
        if self.direction == UP:
            self.position.y += 1
        elif self.direction == RIGHT:
            self.position.x += 1
        elif self.direction == DOWN:
            self.position.y += -1
        elif self.direction == LEFT:
            self.position.x += -1


class PaintingRun(object):
    def __init__(self, opcodes, initial_panel_color=BLACK):
        self.intcode = Intcode(
            opcodes,
            input_data=[initial_panel_color],
            pause_on_output=True,
            computer_name="painter",
        )
        self.panels = [PaintedPanel(0, 0, initial_panel_color)]
        self.robot = PainterRobot()

    def execute(self):
        try:
            while True:
                while len(self.intcode.output_data) < 2:
                    self.intcode.execute()

                paint_color, turn_direction = self.intcode.output_data
                self.intcode.output_data = list()  # reset

                self.paint_panel(paint_color)
                self.robot.turn(turn_direction)
                self.robot.move()

                self.intcode.input_data = [self.get_paint_color_at(self.robot.position)]
        except IntcodeHaltedException:
            pass

    def get_paint_color_at(self, c):
        try:
            return self.panels[self.panels.index(c)].paint_color
        except ValueError:
            return BLACK

    def paint_panel(self, paint_color):
        rpos = self.robot.position

        new_panel = PaintedPanel(rpos.x, rpos.y, paint_color)

        #  This works because panels hash on coordinate only
        try:
            self.panels[self.panels.index(new_panel)] = new_panel
        except ValueError:
            self.panels.append(new_panel)

    def hull_dump(self):
        hull = ""
        for x in list(range(-40, 40)):
            for y in list(range(-50, 50)):
                color = self.get_paint_color_at(Coordinate(x, y))
                hull += "\u2588" if color == 1 else " "

            hull += "\n"

        return hull

    @property
    def unique_painted_panels(self):
        return len(self.panels)
