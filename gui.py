from os import name

from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, HorizontalScroll, VerticalScroll, HorizontalGroup, Grid
from textual.widgets import Footer, Header, Button, Static, Label, RichLog
from rich.text import Text
from config import *

from game import Player, Game
from player_creation_screen import PlayerCreationScreen
from game_screen import GameScreen


class GameGUI(App):
    CSS_PATH = "stylesheet.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("n", "next_round", "Next round")]

    def on_mount(self) -> None:
        self.push_screen(PlayerCreationScreen(), self.start_game)

    def start_game(self, players) -> None:
        self.game = Game(players)
        self.player_colors = {p.name: PLAYER_COLORS[i % len(PLAYER_COLORS)] for i, p in enumerate(self.game.players)}
        self.push_screen(GameScreen())


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
