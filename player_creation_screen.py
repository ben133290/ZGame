from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Footer, Label, Header, Button, Static, Input, Digits
from textual.containers import Vertical, Horizontal, HorizontalGroup, VerticalGroup
from config import *
from player import Player

class PlayerCreationScreen(Screen):
    BINDINGS = [("escape", "app.quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.players = []
        self.draft = {s: 0 for s in STATS}
        self.draft_name = ""
        self.remaining_points = POINT_BUDGET

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="setup"):
            with Vertical(classes="panel"):
                yield Label("New character")
                yield Input(placeholder="Name", id="name", max_length=16)
                for stat in STATS:
                    with HorizontalGroup(classes="stat-row"):
                        yield Label(stat.title(), classes="stat-name")
                        yield Digits("0", id=f"{stat}-value", classes="stat-value")
                        yield Button("-", id=f"{stat}-minus", classes="step")
                        yield Button("+", id=f"{stat}-plus", classes="step")
                with HorizontalGroup(classes="stat-row"):
                    yield Label("Points Left: ", id="points")
                    yield Digits("0", id="points-value", classes="stat-value")
                yield Button("Submit character", id="add", variant="primary")
                yield Label("", id="error")
            with Vertical(classes="panel"):
                yield Label("Roster")
                yield Static("", id="roster")
                yield Button("Remove last", id="undo")
                yield Button("Start game", id="begin", variant="success", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_view()

    def refresh_view(self) -> None:
        for stat, value in self.draft.items():
            self.query_one(f"#{stat}-value", Digits).update(str(value))
        self.query_one("#points-value", Digits).update(f"{self.remaining_points}")
        self.query_one("#roster", Static).update("\n".join([player.name for player in self.players]) or "[dim]nobody yet[/dim]")
        self.query_one("#begin", Button).disabled = len(self.players) < MIN_PLAYERS
        self.query_one("#undo", Button).disabled = not self.players

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "add":
            self.add_player()
        elif bid == "undo":
            self.players.pop()
            self.refresh_view()
        elif bid == "begin":
            self.start_game()
        elif bid and bid.endswith(("-plus", "-minus")):
            stat, _, action = bid.rpartition("-")
            delta = 1 if action == "plus" else -1
            new = self.draft[stat] + delta
            if 0 <= new <= MAX_STAT and (delta < 0 or self.remaining_points > 0):
                self.draft[stat] = new
                self.remaining_points -= delta
        self.refresh_view()


    def add_player(self):
        name = self.query_one("#name", Input).value.strip()
        error = self.query_one("#error", Label)
        if not name:
            error.update("Give your character a name.")
        elif name.lower() in (p.name.lower() for p in self.players):
            error.update("That name is taken.")
        elif len(self.players) >= MAX_PLAYERS:
            error.update("The arena is full.")
        elif self.remaining_points > 0:
            error.update(f"Spend all your stat points ({self.remaining_points} left).")
        else:
            player = Player(name=name, lethality=self.draft.get("lethality", 0), instinct=self.draft.get("instinct", 0), endurance=self.draft.get("endurance", 0), rizz=self.draft.get("rizz", 0), team=0)
            self.players.append(player)
            error.update(f"")
        self.refresh_view()

    def start_game(self):
        self.dismiss(self.players)


