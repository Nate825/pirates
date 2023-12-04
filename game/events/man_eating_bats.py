from game import event 
import random
from game.combat import Combat
from game.combat import Macaque
from game.display import announce
import game.config as config 

class manEatingBats (event.Event):
    def __init__ (self):
        self.name = 'Bat Attack'

    def process (self, world):
        result = {}
        result['message'] = 'the bats have been defeated! ... Maybe you can eat them'
        monsters = []
        n_appearing = random.randrange(4,8)
        n = 1
        while n <= n_appearing:
            monsters.append(Bat("Man-eating Bat" +str(n)))
            n += 1
        announce ("The crew is attacked by a troop of man-eating Bats!")
        Combat(monsters).combat()
        if random.randrange(2) == 0:
            result['newevents'] = [ self ]
        else:
            result['newevents'] = [ ]
        config.the_player.ship.food += n_appearing*3

        return result 