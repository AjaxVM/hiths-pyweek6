
capitol_defense_gain = 10
capitol_troop_gain = 5 #every turn
supply_troop_gain = 4
troop_attack_gain = 3
troop_defense_gain = 2


import random
def perform_battle(terr1, terr2):
    #returns casualties1, casualties2
    a = random.randint(terr1.units, terr1.units * troop_attack_gain)
    b = random.randint(terr2.units, terr2.units * troop_defense_gain)

    if terr2.capitol:
        b += capitol_defense_gain

    result = a - b
    if result <= -10:#critical - terr1 takes total casualties - 1
        return terr1.units - 1, 0
    if result <= -5:#critical - terr1 takes total casualties, terr2 takes minimal
        return terr1.units - 1, int(terr2.units / 4)
    if result >= -2 and result <= 2:#equal damage
        return int(terr1.units / 2), int(terr2.units / 2)
    if result >= 5:
        return int(terr1.units / 4), terr2.units
    return 0, terr2.units
