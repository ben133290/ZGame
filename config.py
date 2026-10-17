from enum import IntEnum

"""
Base probabilities for the Game given on a scale of 0 = 100% to 20 = 5%. Higher numbers make the event LESS likely!
"""
LOCATION_SWITCH_PROB = 15
ACTION_PROB = 10
DISASTER_PROB = 19

MESSAGES = [
    "{party} stare at the stars for a while",
    "{party} hear a strange noise in the distance",
    "{party} argue about which way is north",
    "{party} find an oddly shaped rock and name it Gerald",
    "{party} cuddle next to a camp fire",
    "{party} go skinny dipping",
    "{party} tell each other stories about David Goggins",
]


class SkillType(IntEnum):
    LETHALITY = 0
    INSTINCT = 1
    ENDURANCE = 2 # Makes you less likely to take damage from hunger
    RIZZ = 3

class Locations(IntEnum):
    CORNUCOPIA = 0
    THE_FOREST = 1
    THE_CLIFFS = 2
    THE_LAKE = 3
    THE_SWAMP = 4

FORAGE_FOODS = [
    "blackberries",
    "wild strawberries",
    "mulberries",
    "crab apples",
    "rose hips",
    "elderberries",
    "acorns",
    "hazelnuts",
    "pine nuts",
    "chestnuts",
    "dandelion greens",
    "wild garlic bulbs",
    "cattail roots",
    "fiddleheads",
    "sorrel leaves",
    "clover flowers",
    "puffball mushrooms",
    "chanterelle mushrooms",
    "crayfish",
    "freshwater mussels",
    "frog legs",
    "river snails",
    "bird eggs",
    "beetle grubs",
    "roasted crickets",
    "pine bark strips",
    "questionable mushrooms",
    "suspiciously shiny berries",
]

#Kämpfeee
DRAW_MESSAGES = [
    "{attacker} and {defender} clashed, but neither side came out ahead",
    "{attacker} charged {defender}, and the two groups ended up circling each other, too wary to strike",
    "{attacker} and {defender} traded blows until everyone was too tired to continue",
    "{attacker} ambushed {defender}, but it was a mess and both groups scattered",
    "{attacker} and {defender} stared each other down until a branch snapped and everyone panicked",
    "{attacker} and {defender} fought to a bloody stalemate and backed away",
]

ATTACKER_WINS = [
    "{attacker} ambushed {defender} from the treeline, and {victim} took the worst of it",
    "{attacker} caught {defender} off guard, and {victim} went down hard",
    "{attacker} charged in screaming, and {defender} broke ranks, leaving {victim} wounded",
    "{attacker} cornered {defender} against the rocks, and {victim} paid for it",
    "{attacker} struck at dawn while {defender} were still waking up, and {victim} was caught in the open",
    "{attacker} overwhelmed {defender} in a brutal scramble, and {victim} was left limping",
]

DEFENDER_WINS = [
    "{attacker} tried to ambush {defender}, but they were spotted, and {victim} got hurt in the retreat",
    "{defender} saw {attacker} coming and fought them off, leaving {victim} injured",
    "{attacker} rushed {defender} and got repelled, and {victim} took a nasty hit",
    "{defender} turned the ambush around, and {victim} of {attacker} was caught in their own trap",
    "{attacker} attacked {defender}, but they were better prepared, and {victim} was wounded as the attackers fled",
    "{defender} held their ground against {attacker}, and {victim} was the one who got hurt",
]

LOOT_MESSAGES = [
    "{winner} took some of {victim}'s food",
    "{winner} rifled through {victim}'s pack and made off with food",
    "{victim} dropped their food in the chaos, and {winner} snatched it up",
    "{winner} left with a portion of {victim}'s rations",
]

POINT_BUDGET = 10
MAX_STAT = 8
MIN_PLAYERS = 2
MAX_PLAYERS = 18

PLAYER_COLORS = [
    "#e6194b",  
    "#3cb44b",  
    "#4363d8",  
    "#f58231",  
    "#911eb4",  
    "#008080",  
    "#f032e6",  
    "#9a6324",  
    "#e6a800",  
    "#2a9df4",  
    "#800000",  
    "#6b8e23",  
    "#d6336c",  
    "#17a589",  
    "#7d5fff",  
    "#c0762b",  
    "#5c7080",  
    "#b5179e",  
]
GRID_LAYOUT = [1, None, 2,
               None, 0, None,
               3, None, 4]

LOCATIONS = [
    "Cornucopia",     # 0 - center
    "The Forest",     # 1 - top left
    "The Cliffs",     # 2 - top right
    "The Lake",       # 3 - bottom left
    "The Swamp",      # 4 - bottom right
]

STATS = ["lethality", "instinct", "endurance", "rizz"]
