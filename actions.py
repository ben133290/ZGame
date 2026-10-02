from game import Game, Party, Locations, LOCATION_SWITCH_PROB
from random import randint, choice

class Action:
    def is_available(self, game: "Game", party: Party) -> bool:
        return True

    def execute(self, game: "Game", party: Party) -> None:
        raise NotImplementedError


class FlavourAction(Action):
    """Nothing mechanical happens, just a bit of story."""
    def is_available(self, game: "Game", party: Party) -> bool:
        return len(party.players) > 1
    MESSAGES = [
        "{party} stare at the stars for a while",
        "{party} hear a strange noise in the distance",
        "{party} argue about which way is north",
        "{party} find an oddly shaped rock and name it Gerald",
        "{party} cuddle next to a camp fire",
        "{party} go skinny dipping",
        "{party} tell each other stories about David Goggins",
    ]

    def execute(self, game, party):
        party.log(choice(self.MESSAGES).format(party=party))


class ForageAction(Action):
    """Each member searches for food; instinct helps."""
    def execute(self, game, party):
        found = 0
        for player in party.players:
            if randint(1, 20) + player.instinct >= 12:
                player.food += 1
                found += 1
        if found:
            party.log(f"{party} foraged and found {found} food")
        else:
            party.log(f"{party} foraged but found nothing")


class RestAction(Action):
    def is_available(self, game, party):
        return any(p.health < 10 for p in party.players)

    def execute(self, game, party):
        for player in party.players:
            player.health = min(10, player.health + 1)
        party.log(f"{party} rested and recovered a little")


class ShareFoodAction(Action):
    """Well-fed members hand food to hungry party members."""
    def is_available(self, game, party):
        if len(party.players) < 2:
            return False
        return (any(p.food == 0 for p in party.players)
                and any(p.food > 1 for p in party.players))

    def execute(self, game, party):
        total = sum(p.food for p in party.players)
        for player in party.players:
            player.food = total // len(party.players)
        for player in party.players[:total % len(party.players)]:
            player.food += 1
        party.log(f"{party} shared their food")


class MoveAction(Action):
    def is_available(self, game, party):
        return game.num_locations > 1

    def execute(self, game, party):
        for party in game.parties:
            if (randint(0, 20) >= LOCATION_SWITCH_PROB):
                current_location = party.location
                new_location = randint(0, len(Locations))
                if new_location != current_location:
                    party.location = new_location
                    match new_location:
                        case Locations.CORNUCOPIA:
                            party.log(f"{party.get_team_name()} moved to the cornucopia")
                        case Locations.NORTH_QUAD:
                            party.log(f"{party.get_team_name()} moved to the north quadrant")
                        case Locations.SOUTH_QUAD:
                            party.log(f"{party.get_team_name()} moved to the south quadrant")
                        case Locations.EAST_QUAD:
                            party.log(f"{party.get_team_name()} moved to the east quadrant")
                        case Locations.WEST_QUAD:
                            party.log(f"{party.get_team_name()} moved to the west quadrant")

                for player in party.players:
                    player.location = party.location

class FightAction(Action):
    """Fight another party at the same location. Lethality decides the winner."""
    def _targets(self, game, party):
        return [o for o in game.parties
                if o is not party and o.location == party.location]

    def is_available(self, game, party):
        return bool(self._targets(game, party))

    def execute(self, game, party):
        target = choice(self._targets(game, party))
        attack = sum(p.lethality for p in party.players) + randint(1, 20)
        defence = sum(p.lethality for p in target.players) + randint(1, 20)

        if attack == defence:
            party.log(f"{party} and {target} clashed, but neither side came out ahead")
            return

        winner, loser = (party, target) if attack > defence else (target, party)
        victim = choice(loser.players)
        victim.health -= randint(1, 4)
        party.log(f"{party} attacked {target}: {winner} won and {victim.name} was hurt")

        # Winners loot a piece of food if the victim has any
        if victim.food > 0:
            victim.food -= 1
            choice(winner.players).food += 1
            party.log(f"{winner} took some of {victim.name}'s food")
