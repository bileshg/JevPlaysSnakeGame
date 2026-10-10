import pygame

from src.game.engine import game_loop
from src.utils.config import conf


def run_game():
    pygame.init()

    screen = pygame.display.set_mode((conf.window.width, conf.window.height))
    font = pygame.font.SysFont(conf.font.name, conf.font.size, bold=True)
    clock = pygame.time.Clock()

    pygame.display.set_caption(conf.window.title)

    game_loop(screen, font, clock)
