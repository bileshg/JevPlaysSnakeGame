from enum import Enum


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)

    @classmethod
    def from_vector(cls, x: int, y: int) -> "Direction":
        mapping = {
            (0, -1): cls.UP,
            (0, 1): cls.DOWN,
            (1, 0): cls.RIGHT,
            (-1, 0): cls.LEFT,
        }
        return mapping[(x, y)]
