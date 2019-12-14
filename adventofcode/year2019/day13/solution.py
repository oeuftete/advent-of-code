from collections import defaultdict
from enum import Enum
import logging

from adventofcode.common.coordinate import Coordinate
from adventofcode.common.year2019.intcode_computer import Intcode


class TileId(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


#  class Tile(Coordinate):
#      def __init__(self, x, y, tile_id):
#          super(Tile, self).__init__(x, y)
#          self.tile_id = TileId(tile_id)


class ArcadeCabinet(object):
    def __init__(self, opcodes):
        self.intcode = Intcode(opcodes, pause_on_output=True)
        self.tiles = defaultdict(lambda: TileId.EMPTY)
        self.build()

    def build(self):
        while not self.intcode.halted or len(self.intcode.output_data) < 3:
            self.intcode.execute()

            if len(self.intcode.output_data) == 3:
                x, y, tile_id = self.intcode.output_data
                logging.info(f'Adding output: {x}, {y}, {tile_id}')
                self.intcode.output_data = list()
                self.tiles[Coordinate(x, y)] = TileId(tile_id)

            if self.intcode.halted:
                logging.info('HALTED')
                break

    @property
    def blocks_count(self):
        return len(
            [t for t in self.tiles.values() if t.value == TileId.BLOCK.value])
