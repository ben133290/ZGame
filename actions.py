from random import randint, choice
from config import *
from player import *

class Action:
    def is_available(self, party: Party, *args) -> bool:
        return True

    def execute(self, party: Party, *args) -> str:
        raise NotImplementedError


class FlavourAction(Action):
    """Nothing mechanical happens, just a bit of story."""
    def is_available(self, party: Party, *_) -> bool:
        return len(party.players) > 1

    def execute(self, party, *_):
        return choice(MESSAGES).format(party=party)


class ForageAction(Action):
    def is_available(self, party: Party, *args) -> bool:
        return party.location != Locations.CORNUCOPIA

    def execute(self, party, *_):
        found = 0
        failed = 0
        food = choice(FORAGE_FOODS)
        for player in party.players:
            roll = randint(1, 20)
            if roll + player.instinct >= 12:
                player.food += 1
                found += 1
            elif roll <= 2:
                failed += 1
                player.health -= 3


        if found and not failed:
            return f"{party} foraged and found {found} {food}"
        elif failed and not found:
            return f"{party} foraged but found only poisonous {food} instead"
        elif failed and found:
            return f"{party} foraged and found {found} {food} but some of the found food was poisonous"
        else:
            return f"{party} foraged but found nothing"

"""
class RestAction(Action):
    def is_available(self, party, *_):
        return any(p.health < 10 for p in party.players)

    def execute(self, party, *_):
        for player in party.players:
            player.health = min(10, player.health + 1)
        return f"{party} rested and recovered a little"
"""

class ShareFoodAction(Action):
    """Well-fed members hand food to hungry party members."""
    def is_available(self, party, *_):
        if len(party.players) < 2:
            return False
        return (any(p.food == 0 for p in party.players)
                and any(p.food > 1 for p in party.players))

    def execute(self, party, *_):
        total = sum(p.food for p in party.players)
        for player in party.players:
            player.food = total // len(party.players)
        for player in party.players[:total % len(party.players)]:
            player.food += 1
        return f"{party} shared their food"


class MoveAction(Action):
    def execute(self, party, *_):
        options = [loc for loc in Locations if loc != party.location]
        party.location = choice(options)

        for player in party.players:
            player.location = party.location

        return f"{party} moved to {party.location.name.replace('_', ' ').title()}"


class FightAction(Action):
    """Fight another party at the same location. Lethality decides the winner."""

    def _targets(self, party, parties):
        return [
            other
            for other in parties
            if other is not party
            and other.location == party.location
        ]

    def is_available(self, party, *args):
        parties = args[0]
        return bool(self._targets(party, parties))

    def execute(self, party, *args):
        parties = args[0]
        target = choice(self._targets(party, parties))

        attack = sum(p.lethality for p in party.players) + randint(1, 20)
        defence = sum(p.lethality for p in target.players) + randint(1, 20)

        if attack == defence:
            return choice(DRAW_MESSAGES).format(attacker=party, defender=target)

        attacker_won = attack > defence
        winner, loser = (party, target) if attacker_won else (target, party)

        victim = choice(loser.players)
        victim.health -= randint(1, 5)

        pool = ATTACKER_WINS if attacker_won else DEFENDER_WINS
        log_string = choice(pool).format(
            attacker=party, defender=target, victim=victim.name
        )

        if victim.food > 0:
            victim.food -= 1
            choice(winner.players).food += 1
            log_string += "\n" + choice(LOOT_MESSAGES).format(
                winner=winner, victim=victim.name
            )

        return log_string
