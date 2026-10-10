import logging

import pygame

from src.game.engine import Agent, game_loop
from src.utils.config import conf

logger = logging.getLogger(__name__)


def run_game(agent: Agent):
    try:
        pygame.init()

        screen = pygame.display.set_mode((conf.window.width, conf.window.height))
        font = pygame.font.SysFont(conf.font.name, conf.font.size, bold=True)
        clock = pygame.time.Clock()

        pygame.display.set_caption(conf.window.title)

        logger.info("Starting the game loop")
        game_loop(screen, font, clock, agent)
    except Exception as e:
        logger.error("An error occurred: %s", e)
    finally:
        pygame.quit()
