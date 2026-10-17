from config import Locations


class Player:

    def __init__(self, name: str, lethality: int, instinct: int, endurance: int, rizz: int, team: int) -> None:
        self.health = 10
        self.hunger = 0
        self.food = 0
        self.location = Locations.CORNUCOPIA
        self.name = name
        self.lethality = lethality
        self.instinct = instinct
        self.endurance = endurance
        self.rizz = rizz
        self.team = team
        self.log: list[str] = []

    def get_status(self):
        return f"{self.name}:\n\thealth: {self.health}\n\tfood: {self.food}"

    @property
    def alive(self) -> bool:
        return self.health > 0

class Party:
    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.location = players[0].location

    def set_location(self, location):
        self.location = location
        for player in self.players:
            player.location = location

    def remove_player(self, player):
        self.players.remove(player)

    def get_team_name(self):
        names = [p.name for p in self.players]
        if len(names) == 1:
            return names[0]
        return "Team " + ", ".join(names[:-1]) + " and " + names[-1]

    def log(self, message: str):
        self.players[0].log.append(message)

    def __str__(self) -> str:
        return self.get_team_name()

