from dotenv import load_dotenv

from src.agents.jev_agent import JevAgent
from src.runner import run_game

load_dotenv()

if __name__ == "__main__":
    run_game(JevAgent())
