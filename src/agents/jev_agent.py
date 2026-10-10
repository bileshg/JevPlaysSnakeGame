import json

from typesafe_sdk import Choice, TypeSafeClient

from src.game.direction import Direction
from src.game.engine import Agent, GameState

INSTRUCTIONS = (
    "Play Snake and try to get a high score. Choose UP, DOWN, LEFT, or RIGHT for the next move. "
    "Eating food grows the snake and adds one point; the score corresponds to the length of the snake. "
    "Priorities:\n"
    "1. Avoid collisions with walls and the snake's body.\n"
    "2. Prefer moves that keep future movement options open.\n"
    "3. Move toward the food when it is safe to do so.\n"
    "4. Do not reverse directly into the snake's body."
)
CRITERIA = {
    "UP": "Move the snake up",
    "DOWN": "Move the snake down",
    "LEFT": "Move the snake left",
    "RIGHT": "Move the snake right",
}
SCHEMA = {
    "move": Choice(
        instructions=INSTRUCTIONS,
        criteria=CRITERIA,
    )
}


class JevAgent(Agent):
    def __init__(self):
        self.game_state = None

    def format_game_state(self) -> str:
        if self.game_state is None:
            return json.dumps({})

        return json.dumps(
            {
                "board_rows": self.game_state.board_rows,
                "board_cols": self.game_state.board_cols,
                "snake": self.game_state.snake.get_state(),
                "food": self.game_state.food.get_state(),
            }
        )

    def update(self, game_state: GameState) -> None:
        self.game_state = game_state

    def get_direction(self) -> Direction | None:
        with TypeSafeClient() as client:
            response = client.system_one(
                state=self.format_game_state(),
                questions=SCHEMA,
            )
            return Direction[response.answers["move"].choice]  # type: ignore
