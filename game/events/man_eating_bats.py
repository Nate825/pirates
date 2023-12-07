import game.event as event
import random
import game.combat as combat
import game.superclasses as superclass
from game.display import announce

class ManEatingBats (event.Event):
    def __init__ (self):
        self.name = 'Bat Attack'

    def process (self, world):
        result = {}
        result['message'] = 'the bats have been defeated! ... Maybe you can eat them'
        monsters = []
        min = 2
        uplim = 6
        if random.randrange(2) == 0:
            min = 1
            uplim = 5
            monsters.append(ManEatingBat('big bat'))
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(ManEatingBat("Man-eating Bat" +str(n)))
            n += 1
        announce ("Youre crewmate has woken up the bats and are quickly being attacked!")
        combat.Combat(monsters).combat()
        result['newevents'] = [  ]
        return result 
    
class ManEatingBat(combat.Monster):
    
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(50,70), (5,15)]
        attacks["slash"] = ["slashs",random.randrange(50,80), (1,10)]
        attacks["swarm"] = ["swarms",random.randrange(50,80), (1,10)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 100 + random.randrange(-10,11))