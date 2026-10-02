from enum import Enum
from random import randint, choice
from actions import *

"""
Base probabilities for the Game given on a scale of 0 = 100% to 20 = 5%. Higher numbers make the event LESS likely!
"""
LOCATION_SWITCH_PROB = 15
ACTION_PROB = 10
DISASTER_PROB = 19

class SkillType(Enum):
    LETHALITY = 0
    INSTINCT = 1
    ENDURANCE = 2 # Makes you less likely to take damage from hunger
    RIZZ = 3

class Locations(Enum):
    CORNUCOPIA = 0
    SOUTH_QUAD = 1
    NORTH_QUAD = 2
    EAST_QUAD = 3
    WEST_QUAD = 4


class Player:

    def __init__(self, name: str, lethality: int, instinct: int, endurance: int, rizz: int, team: int) -> None:
        self.health = 10
        self.hunger = 0
        self.alive = True
        self.food = 0
        self.location = 0
        self.name = name
        self.lethality = lethality
        self.instinct = instinct
        self.endurance = endurance
        self.rizz = rizz
        self.team = team
        self.log: list[str] = []

    def get_status(self):
        return f"{self.name}:\n\thealth: {self.health}\n\tfood: {self.food}"

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


class Game:

    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.parties = [Party([player]) for player in players]
        self.running = True
        self.round = 1
        self.teams = []
        self.num_locations = len(Locations)
        for player in players:
            if player.team not in self.teams:
                self.teams.append(player.team)
        self.actions = [ FlavourAction(),
            ForageAction(),
            RestAction(),
            ShareFoodAction(),
            MoveAction(),
            FightAction(),
        ]

    def get_available_actions(self, party: Party):
         return [a for a in self.actions if a.is_available(self, party)]

    def join_parties(self, party, other):
        self.parties.remove(party)
        self.parties.remove(other)
        merged = Party(party.players + other.players)
        self.parties.append(merged)
        print(f"{party.get_team_name()} and {other.get_team_name()} have banded together")

    def split_parties(self, party, where):
        # where is the index of the last player in the first group
        self.parties.remove(party)
        self.parties.append(Party(party.players[:where + 1]))
        self.parties.append(Party(party.players[where + 1:]))
        print(f"{party.get_team_name()} have split up")

    def skill_check(self, type: SkillType, player: Player, dc: int) -> bool:
        roll = randint(0, 20) 
        if (type is SkillType.LETHALITY):
            return roll + player.lethality >= dc
        elif (type is SkillType.ENDURANCE):
            return roll + player.endurance >= dc
        elif (type is SkillType.INSTINCT):
            return roll + player.instinct >= dc
        elif (type is SkillType.RIZZ):
            return roll + player.rizz>= dc

    """ 
    ROUND PHASE 1: Player's lose food proportional to their hunger.
    """
    def tick_food_and_hunger(self):
        for player in self.players:
            if player.alive:
                if self.skill_check(SkillType.ENDURANCE, player, 12):
                    if player.food > 0:
                        player.food -= 1
                        player.hunger = 0
                        player.health += 1
                        player.log.append(f"{player.name} consumed some food")
                    else:
                        player.hunger += 1
                        player.health -= player.hunger
                        player.log.append(f"{player.name} is hungry")

        for player in self.players:
            if player.alive:
                if player.health <= 0:
                    player.health = 0
                    player.alive = False
                    player.log.append(f"{player.name} starved to death")

    """ 
    ROUND PHASE 2: A disaster occurs at a location
    """
    def tick_location(self):
        for i in range(self.num_locations):
            if (randint(0, 20) >= DISASTER_PROB):
                print(f"a disaster occurs at location {i} - it's not implemented yet :(")

    """ 
    ROUND PHASE 3: Players build new teams 
    """
    def tick_parties(self):
        # Parties
        old_parties = self.parties.copy()
        for party in old_parties:
            # Skip parties that were already split/merged earlier this round
            if party not in self.parties:
                continue

            if len(party.players) > 1 and randint(1, 20) > 15:
                self.split_parties(party, randint(0, len(party.players) - 2))
                continue  # don't let a party that just split try to join again

            if randint(1, 20) > (15 + len(party.players)):
                for other in self.parties:
                    if other is not party and party.location == other.location:
                        self.join_parties(party, other)
                        break

    """ 
    ROUND PHASE 4: Players perform various actions 
    """
    def tick_actions(self):
        old_parties = self.parties.copy()
        for party in old_parties:
            if (randint(1, 20) > ACTION_PROB):
                action = choice(self.get_available_actions(party))
                action.execute(self, party)


    def next_round(self):
        print(f"-- STARTING ROUND {self.round} --")

        self.tick_food_and_hunger()
        self.tick_location()
        self.tick_parties()
        self.tick_actions()

        # Check aliveness
        alive_players = 0
        for player in self.players:
            if player.alive:
                if player.health <= 0:
                    player.alive = False
                    player.log.append(f"{player.name} died")
                    # Remove the dead player from whatever party they were in
                    for party in self.parties:
                        if player in party.players:
                            party.remove_player(player)
                            break
                else:
                    alive_players += 1

        # Remove parties that no longer have any members
        self.parties = [party for party in self.parties if party.players]

        # Present round details
        for player in self.players:
            for l in player.log:
                print(l)
            player.log = []

        # Game End
        if alive_players < 2:
            self.running = False

        print("-- END OF ROUND --")
        print([party.__str__() for party in self.parties])
        for player in self.players:
            print(player.get_status())

        self.round += 1

if __name__ == '__main__':
    maria = Player("Maria", 3, 0, 2, 5, 0)
    tobi = Player("Tobi", 5, 0, 5, 0, 1)
    benny = Player("Benny", 0, 4, 2, 4, 0)
    andrina = Player("Andrina", 3, 2, 2, 3, 1)
    giovanni = Player("Giovanni", 1, 1, 2, 8, 2)
    carina = Player("Carina", 1, 6, 2, 1, 2)
    game = Game([maria, tobi, benny, andrina, giovanni, carina])
    while (game.running):
        if (input("continue? (y/n): ") == "y"):
            game.next_round()
        else:
            break




