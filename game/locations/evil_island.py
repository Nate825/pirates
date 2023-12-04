from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import random
import events.man_eating_bats as event 

class Island (location.Location):
    def __init__ (self,x, y, w):
        super().__init__(x, y, w)
        self.name = 'island'
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Beach_with_ship(self)
        self.locations = {}
        self.locations['beach'] = self.starting_location
        self.locations['trees1'] = Trees1(self)
        self.locations['trees2'] = Trees2(self)
        self.locations['hotspring'] = Hotspring(self)
        self.locations['puzzle'] = Puzzle(self)
        self.locations['small cave'] = Small_cave(self)
        self.locations['in small cave'] = In_small_cave(self)
        self.locations['infermery'] = Infermery(self)
        self.locations['cavern'] = Cavern(self)
        self.locations['armory'] = Armory(self)


    def enter (self, ship):
        print("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'beach'
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce ('arrive at the beach. Your ship is at anchor in a small bay to the south')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce ('You return to your ship')
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif(verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['trees1']
        elif (verb == 'east' or verb == 'west'):
            announce ("you walk all the way around the island on the beach. Its not very interesting.")

class Trees1 (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees1"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['northeast'] = self
        self.verbs['northwest'] = self

    def enter (self):
        announce('You make youre way through the thick trees visability isnt the best')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce("You return to the beach.")
            config.the_player.next_loc = self.main_location.locations['beach']
        elif (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['trees2']
        elif (verb == 'northeast'):
            config.the_player.next_loc = self.main_location.locations['hotspring']
        elif (verb == 'northwest'):
            config.the_player.next_loc = self.main_location.locations['small cave']


class Trees2 (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'trees2'
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = items.Cutlass()
        self.item_in_clothes = items.Flintlock()

    def enter (self):
        announce ("The thickness and visability have gotten worse, aswell as a massive mountain blocking your path to the north")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce('You try and make youre way back where the trees arnt so thick.')
            config.the_player.next_loc = self.main_location.locations['trees1']
        elif (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['hotspring']
        elif (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['small cave']

class Hotspring (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'hotspring'
        self.verbs['north'] = self
        self.verbs['southwest'] = self
        self.verbs['west'] = self    
        self.event_chance = 100
        self.events.append(drowned_pirates.DrownedPirates())
        if drowned_pirates == True:
            announce ('Their is a horde of drowned zombies approaching you')
    def enter (self):
        announce ('Something isnt right about this place')
    
    def process_verb (self, verb, smd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['puzzle']
        elif (verb == 'southwest'):
            config.the_player.next_loc = self.main_location.locations['trees1']
        elif (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['trees2']

class Puzzle (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'puzzle'
        self.verbs['northwest'] = self
        self.verbs['south'] = self
    def enter (self):
        announce('')
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'northwest'):
            config.the_player.next_loc = self.main_location.locations['cavern']
        if (verb == 'south'):
            config.the_player.next_loc = self.main_locations.locations['hotspring']

class Small_cave (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'small cave'
        self.verbs['north'] = self
        self.verbs['southeast'] = self
        self.verbs['east'] = self
    def enter (self):
        announce ('You approach a small cave somthing doesnt seem right')
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['in the cave']
        if (verb == 'southeast'):
            config.the_player.next_loc = self.main_location.locations['trees1']
        if (verb == east):
            config.the_player.next_loc = self.main_location.locations['trees2']

class In_small_cave (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'in small cave'
        self.verbs['west'] = self
        self.verbs['south'] = self
        self.verbs['northeast'] =self
    def enter (self):
        announce ('You enter the small cave a quickly realize you are getting attacked by a swarm of man eating bats')
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['infermery']
        elif (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['small cave']
        elif (verb == 'northeast'):
            config.the_player.next_loc = self.main_location.locations['cavern']

class Infermery (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'infermery'
        self.verbs['east'] = self
    def enter (self):
        announce("You have entered the infermery heal your crewmates after that tough battle")
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['in small cave']

class Cavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'carven'
        self.verbs['north'] = self
        self.verbs['southeast'] = self
        self.verbs['southwest'] = self
    def enter (self):
        announce('You have entered into the Bat Cave')
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'north'):
            config.the_player.next_loc = self.main_location.locations['armory']
        elif (verb == 'southeast'):
            config.the_player.next_loc = self.main_location.locations['puzzle']
        elif (verb == 'southwest'):
            config.the_player.next_loc = self.main_location.locations['in small cave']

class Armory (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'armory'
        self.verbs['south'] = self

    def enter (self):
        announce('You have entered the armory. Gear up to get off the island')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['cavern']

class Bat(Monster):
    def __init__ (self):
        attacks = {}
        attacks['bite'] = ['bites',random.randrange(60,80), (5,15)]
        attacks['slash'] = ['slashes',random.randrange(60,80), (5,15)]
        super().__init__('Man Eating Bats',random.randint(64,96), attacks, 100 + random.randint(0, 10))
            
    
    
    
    
    
    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into the small forest on the island."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the forest floor."
        announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")