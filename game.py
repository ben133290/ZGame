from random import randint, choice
from actions import *
from config import *
from player import *

class Game:

    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.parties = [Party([player]) for player in players]
        self.dead_players = []
        self.running = True
        self.round = 1
        self.teams = []
        self.num_locations = len(Locations)
        for player in players:
            if player.team not in self.teams:
                self.teams.append(player.team)
        self.actions: list[Action] = [ FlavourAction(),
            ForageAction(),
            #RestAction(),
            ShareFoodAction(),
            MoveAction(),
            FightAction(),
        ]


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
            return roll + player.rizz >= dc

    """ 
    ROUND PHASE 1: Player's lose food proportional to their hunger.
    """
    def tick_food_and_hunger(self):
        for player in self.players:
            if player.alive:
                if not self.skill_check(SkillType.ENDURANCE, player, 12):
                    if player.food > 0:
                        player.food -= 1
                        player.hunger = 0
                        if player.health < 10:
                            player.health += 1
                    else:
                        player.hunger += 1
                        player.health -= player.hunger

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
            available = [a for a in self.actions if a.is_available(party, self.parties)]
            print(available)
            action = choice(available)
            logstring = action.execute(party, self.parties)
            party.log(logstring)


    def check_alive(self):
        # Check aliveness
        alive_players = 0
        for player in self.players:
            if player.alive:
                alive_players += 1
            else:
                for party in self.parties:
                    if player in party.players:
                        party.remove_player(player)

        # Remove parties that no longer have any members
        self.parties = [party for party in self.parties if party.players]
        self.dead_players = [player for player in self.players if not player.alive]

        # Game End
        if alive_players < 2:
            self.running = False

    def clear_logs(self):
        for player in self.players:
            player.log = []

    def next_round(self):
        print(f"-- STARTING ROUND {self.round} --")
        self.clear_logs()
        self.tick_food_and_hunger()
        self.check_alive()
        self.tick_location()
        self.tick_parties()
        self.tick_actions()
        self.check_alive()
        self.round += 1


