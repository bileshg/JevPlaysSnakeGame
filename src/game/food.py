import pygame

from src.utils.config import conf


class Food:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, conf.block.width, conf.block.height)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, conf.game.food.color, self.rect)

    def get_state(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
        }
