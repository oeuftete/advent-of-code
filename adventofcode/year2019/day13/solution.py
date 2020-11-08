import logging
import math
from collections import defaultdict
from enum import Enum
from time import sleep

from adventofcode.common.coordinate import Coordinate
from adventofcode.common.year2019.intcode_computer import (
    Intcode,
    IntcodeNeedInputException,
)


class TileId(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def __repr__(self):
        return self.c

    @property
    def c(self):
        if self.value == self.EMPTY.value:
            return " "
        elif self.value == self.WALL.value:
            return "\u2588"
        elif self.value == self.BLOCK.value:
            return "#"
        elif self.value == self.PADDLE.value:
            return "|"
        elif self.value == self.BALL.value:
            return "o"
        return "?"


class ArcadeCabinet(object):
    def __init__(self, opcodes, play=False, manual=False, screen=False):
        self.play = play
        self.manual = manual
        self.screen = screen

        self.intcode = Intcode(opcodes, pause_on_output=True)

        self.tiles = defaultdict(lambda: TileId.EMPTY)
        self.score = 0
        self.paddle_location = None
        self.ball_location = None
        self.build()

    def build(self):
        if self.play:
            self.intcode.memory[0] = 2

        while not self.intcode.halted or len(self.intcode.output_data) < 3:
            try:
                self.intcode.execute()

                if len(self.intcode.output_data) == 3:
                    x, y, tile_id = self.intcode.output_data

                    if x == -1 and y == 0:
                        logging.debug(f"Setting score: {tile_id}")
                        self.score = tile_id
                    else:
                        c = Coordinate(x, y)
                        t = TileId(tile_id)
                        self.tiles[c] = t
                        logging.debug(f"Tile update: {c} -> {t}")

                        if tile_id == TileId.PADDLE.value:
                            logging.debug(f"*** Paddle at {c}")
                            self.paddle_location = c
                        elif tile_id == TileId.BALL.value:
                            logging.debug(f"*** Ball at {c}")
                            self.ball_location = c

                    self.intcode.output_data = list()

                if self.intcode.halted:
                    logging.debug("HALTED")
                    break

            except IntcodeNeedInputException:
                self.dump_screen()

                if self.manual:
                    move = input("\nMove joystick:")
                    move = int(move)
                else:
                    if self.ball_location.x < self.paddle_location.x:
                        move = -1
                    elif self.ball_location.x > self.paddle_location.x:
                        move = 1
                    else:
                        move = 0

                self.intcode.input_data.append(move)

    def dump_screen(self):
        if not self.screen:
            return

        print(
            f"  SCORE: {self.score}, ball: {self.ball_location}, "
            f"paddle: {self.paddle_location}"
        )
        screen = defaultdict(lambda: defaultdict(lambda: TileId.EMPTY))

        min_x = min_y = math.inf
        max_x = max_y = -math.inf

        for c, t in self.tiles.items():
            screen[c.x, c.y] = t
            max_x = max(max_x, c.x)
            max_y = max(max_y, c.y)
            min_x = min(min_x, c.x)
            min_y = min(min_y, c.y)

        for x in range(min_x, max_x + 1):
            line = ""
            for y in range(min_y, max_y + 1):
                line += screen[x, y].c
            print(line)
        sleep(0.1)

    @property
    def blocks_count(self):
        return len([t for t in self.tiles.values() if t.value == TileId.BLOCK.value])
