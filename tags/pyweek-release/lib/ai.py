import util

class AI(object):
    def __init__(self, player_name, world):
        self.player_name = player_name
        self.world = world

        self.mode = "attack"

    def update(self, whos_turn):
        my_player = self.world.players[whos_turn]

        #favor = biggest player or None if we re the biggest player...
        favor = self.world.get_biggest_player()
        if favor == my_player:
            favor = None

        if self.mode == "attack":
            #we need to pick two territories
            for i in my_player.territories:
                if i.can_move and i.units>1:
                    a = util.get_nearest_weakest(i,
                                self.world.grid,
                                favor)
                    if a:
                        #do battle with these two
                        if i.units >= a.units or i.units == i.max_units:
                            return "battle", i, a
            self.mode = "defend"
        if self.mode == "defend":
##            print "AI: defend"
##            return ["defend"]
            #basically - see if either our supply center or capitol is next to any enemy - if so - retreat!!!!
            for i in my_player.territories:
                if i.capitol or i.supply:
                    if util.get_enemies_touching(i, self.world.grid):
                        for x in util.get_friendlies_touching(i, self.world.grid):
                            if x.units > 1 and x.can_move:
                                return "move", x, i

            #now loop through again - this time ignoring capitols/supplies
            #basically, mass our troops :P
            for i in my_player.territories:
                if not (i.capitol or i.supply):
                    if util.get_enemies_touching(i, self.world.grid):
                        for x in util.get_friendlies_touching(i, self.world.grid):
                            if x.units > 1 and x.can_move:
                                return "move", x, i
            self.mode = "press"
        if self.mode == "press":
            for i in my_player.territories:
                if i.units > 1 and i.can_move:
                    goto = util.get_nearest_to_enemy(i, self.world.grid)
                    return "move", i, goto
            self.mode = "done"
        if self.mode == "done":
            return ["end_turn"]
