from pathlib import Path

from omegaconf import OmegaConf

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.yaml"

conf = OmegaConf.load(CONFIG_PATH)

conf.block = {}
conf.block.width = conf.window.width // conf.game.cols  # type: ignore
conf.block.height = conf.window.height // conf.game.rows  # type: ignore
