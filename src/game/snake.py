import pygame

from src.game.direction import Direction
from src.utils.config import conf


class Snake:
    def __init__(self):
        self.x, self.y = conf.block.width, conf.block.height
        self.x_dir, self.y_dir = 1, 0
        self.head = pygame.Rect(self.x, self.y, conf.block.width, conf.block.height)
        self.body = [
            pygame.Rect(
                self.x - conf.block.width, self.y, conf.block.width, conf.block.height
            )
        ]

    def reset(self):
        self.x, self.y = conf.block.width, conf.block.height
        self.x_dir, self.y_dir = 1, 0
        self.head = pygame.Rect(self.x, self.y, conf.block.width, conf.block.height)
        self.body = [
            pygame.Rect(
                self.x - conf.block.width, self.y, conf.block.width, conf.block.height
            )
        ]

    @property
    def direction(self) -> Direction:
        return Direction.from_vector(self.x_dir, self.y_dir)

    def set_direction(self, direction: Direction):
        x, y = direction.value

        # Prevent the snake from reversing
        if self.x_dir * x == 0 and self.y_dir * y == 0:
            self.x_dir, self.y_dir = x, y

    @property
    def is_dead(self) -> bool:
        for segment in self.body:
            if self.head.x == segment.x and self.head.y == segment.y:
                return True
            if self.head.x not in range(conf.window.width) or self.head.y not in range(
                conf.window.height
            ):
                return True
        return False

    def move(self):
        self.body.append(self.head)
        for i in range(len(self.body) - 1):
            self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
        self.head.x += self.x_dir * conf.block.width
        self.head.y += self.y_dir * conf.block.height
        self.body.remove(self.head)

    def grow(self):
        tail = self.body[-1]
        self.body.append(
            pygame.Rect(tail.x, tail.y, conf.block.width, conf.block.height)
        )

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, conf.game.snake.color, self.head)
        for segment in self.body:
            pygame.draw.rect(screen, conf.game.snake.color, segment)

    def get_state(self) -> dict:
        return {
            "head": {"x": self.head.x, "y": self.head.y},
            "body": [{"x": segment.x, "y": segment.y} for segment in self.body],
            "direction": list(self.direction.value),
            "is_dead": self.is_dead,
        }
