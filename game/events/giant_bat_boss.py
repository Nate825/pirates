from game import event 
import random
from game.combat import Combat
from game.combat import Monster
from game.display import announce
import game.config as config

class GiantBatBoss (event.Event):
    def __init__ (self):
        self.name = 'Giant bat attack'
    
    def process (self, world):
        result = {}
        result['message'] = 'Congratulations you have deafted the Giant Bat boss fight'
        monsters = []
        #n_appearing = random.randrange(5, 10)
        n_appearing  = 2
        n = 1
        while n <= n_appearing:
            monsters.append(GiantBat('Man-eating Giant Bat' +str(n)))
            n += 1
        announce ('Your crew is being attack by a Giant Bat!')
        Combat(monsters).combat()
        if random.randrange(2) == 0:
            result['newevents'] = [ self ]
        else:
            result['newevents'] = [ ]
        return result

class GiantBat (Monster):
    def __init__ (self, name):
        attacks = {}
        attacks['bite'] = ['bites', random.randrange(100,150), (10,20)]
        attacks['slash'] = ['slashes', random.randrange(100,150), (10,20)]
        attacks['crush'] = ['crushes', random.randrange(110, 160), (10, 20)]
        super().__init__('Giant Bat', random.randint(64,96), attacks, 100 + random.randint(0, 10))