from textual.screen import Screen
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, HorizontalScroll, VerticalScroll, HorizontalGroup, Grid
from textual.widgets import Footer, Header, Button, Static, Label, RichLog
from rich.text import Text
from config import *
from game import Player, Game

class PlayerStats(VerticalGroup):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player

    def compose(self) -> ComposeResult:
        color = self.app.player_colors[self.player.name]
        yield Label(Text(self.player.name, style=f"bold {color}"), classes="player-name")
        with HorizontalGroup(classes="stats"):
            yield Label(f"{self.player.health}/10 ♥ ", id="health", classes="statcell")
            yield Label(f"{self.player.lethality} Leth.", classes="statcell")
            yield Label(f"{self.player.instinct} Inst.", classes="statcell")
            yield Label(f"{self.player.endurance} End.", classes="statcell")
            yield Label(f"{self.player.rizz} Rizz", classes="statcell")
            yield Label(f"Food {self.player.food}", classes="statcell")
            if self.player.hunger > 0:
                yield Label(f"hungry", classes="statcell statcon")

    def on_mount(self) -> None:
        self.set_class(not self.player.alive, "dead")
        if not self.player.alive:
            self.query_one("#health", Label).update("DEAD")


class PartyPanel(VerticalScroll):
    def compose(self) -> ComposeResult:
        for party in self.app.game.parties:
            with VerticalGroup(classes="party") as group:
                group.border_title = f"{party}"
                for player in party.players:
                    yield PlayerStats(player)
        if self.app.game.dead_players:
            with VerticalGroup(classes="party") as group:
                group.border_title = "Dead players"
                for player in self.app.game.dead_players:
                    yield PlayerStats(player)

class LocationBox(Static):
    def __init__(self, index: int, name: str):
        super().__init__(classes="location")
        self.index = index
        self.border_title = name

    def set_players(self, players) -> None:
        if players:
            self.update("\n".join(f"• {p.name}" for p in players))
        else:
            self.update("[dim]empty[/dim]")

class ControlBar(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button("Next Round", id="start", variant="success")

class ArenaMap(Grid):
    def compose(self) -> ComposeResult:
        for cell in GRID_LAYOUT:
            if cell is None:
                yield Static(classes="spacer")
            else:
                yield LocationBox(cell, LOCATIONS[cell])

    def on_mount(self) -> None:
        self.refresh_map()

    def refresh_map(self) -> None:
        players = self.app.game.players
        for box in self.query(LocationBox):
            here = [p for p in players if p.location == box.index and p.alive]
            box.set_players(here)

class EventLog(RichLog):
    def compose(self) -> ComposeResult:
        return super().compose()

class GameScreen(Screen):
    BINDINGS = [("n", "next_round", "Next round")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with HorizontalScroll():
            yield PartyPanel()
            with VerticalGroup():
                yield ArenaMap()
                yield EventLog(wrap=True)
        yield ControlBar()

    async def action_next_round(self) -> None:
        game = self.app.game
        game.next_round()
        await self.query_one(PartyPanel).recompose()
        self.query_one(ArenaMap).refresh_map()
        text_log = self.query_one(EventLog)
        text_log.clear()
        for player in game.players:
            for line in player.log:
                text = Text(line)
                for name, color in self.app.player_colors.items():
                    text.highlight_words([name], f"bold {color}")
                text_log.write(text)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            await self.action_next_round()
