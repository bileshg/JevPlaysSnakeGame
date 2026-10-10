import atexit
import random
import sys
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox
from typing import Protocol

import pygame

from src.game.direction import Direction
from src.game.food import Food
from src.game.snake import Snake
from src.utils.config import conf

_TK_ROOT = tk.Tk()
_TK_ROOT.attributes("-topmost", True)
_TK_ROOT.withdraw()

atexit.register(_TK_ROOT.destroy)


@dataclass(frozen=True)
class GameState:
    board_rows: int
    board_cols: int
    snake: Snake
    food: Food


class Agent(Protocol):
    def update(self, game_state: GameState) -> None: ...

    def get_direction(self) -> Direction | None: ...


def draw_grid(screen: pygame.Surface):
    screen.fill(conf.window.background.color)

    x = 0
    for _ in range(conf.game.cols):
        pygame.draw.line(
            screen, conf.window.grid.color, (x, 0), (x, conf.window.height)
        )
        x += conf.block.width

    y = 0
    for _ in range(conf.game.rows):
        pygame.draw.line(screen, conf.window.grid.color, (0, y), (conf.window.width, y))
        y += conf.block.height


def random_empty_block(snake: Snake) -> tuple[int, int]:
    max_attempts = conf.game.cols * conf.game.rows * 2
    for _ in range(max_attempts):
        x = random.randint(0, conf.game.cols - 1) * conf.block.width
        y = random.randint(0, conf.game.rows - 1) * conf.block.height

        if not any(block.x == x and block.y == y for block in snake.body):
            return x, y

    raise RuntimeError("Failed to find an empty block for the food.")


def create_food(snake: Snake) -> Food:
    return Food(*random_empty_block(snake))


def end_game():
    pygame.quit()
    sys.exit()


def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()


def update_score(
    screen: pygame.Surface,
    font: pygame.font.Font,
    score_panel: pygame.Rect,
    snake: Snake,
):
    score = font.render(f"{len(snake.body) - 1}", True, conf.font.color)
    screen.blit(score, score_panel)


def get_game_state(snake: Snake, food: Food) -> GameState:
    return GameState(
        board_rows=conf.game.rows, board_cols=conf.game.cols, snake=snake, food=food
    )


def game_loop(
    screen: pygame.Surface,
    font: pygame.font.Font,
    clock: pygame.time.Clock,
    agent: Agent,
):
    score = font.render("0", True, conf.font.color)
    score_panel = score.get_rect(
        center=(conf.window.width / 2, conf.window.height / 20)
    )

    snake = Snake()
    food = create_food(snake)

    draw_grid(screen)

    while True:
        clock.tick(conf.game.tick)
        handle_quit()

        if len(snake.body) == conf.game.cols * conf.game.rows - 1:
            if _ := messagebox.askyesno(
                "Wow! You Won!", "Do you want to play again?", parent=_TK_ROOT
            ):
                snake.reset()
                food = create_food(snake)
            else:
                end_game()

        state = get_game_state(snake, food)
        agent.update(state)
        if direction := agent.get_direction():
            snake.set_direction(direction)

        if snake.is_dead:
            if _ := messagebox.askyesno(
                "You Lost!", "Do you want to play again?", parent=_TK_ROOT
            ):
                snake.reset()
                food = create_food(snake)
            else:
                end_game()
        snake.move()

        draw_grid(screen)

        snake.draw(screen)
        food.draw(screen)

        update_score(screen, font, score_panel, snake)

        if snake.head.x == food.x and snake.head.y == food.y:
            snake.grow()
            food = create_food(snake)

        pygame.display.update()
