from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
import game.events.man_eating_bats as man_eating_bats
import game.events.giant_bat_boss as giant_bat_boss


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
        self.Handlepuzzle()
        print(self.colors)

    def enter (self, ship):
        print("arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
    
    def Handlepuzzle(self):
        self.colors = ['red', 'blue', 'white']
        random.shuffle(self.colors)

    def Checkpuzzle(self):
        user_input = []
        for color in self.colors:
            user_color = input(f"Enter the colors: ")
            user_input.append(user_color)
        if user_input ==  self.colors:
            print('Please enter on to the Cavern and head NorthWest')
        else:
            print('You do not have the correct password')

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
        announce (f"You see a remarkable shell that seems to be painted {self.main_location.colors[0]} I wonder if it has any significance" )
        

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
        announce(f"You find a strange stone it seems to be painted {self.main_location.colors[1]} I wonder if it has anything to do with the shell")              #Randomization factor

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
        if random.randint(0,1):
            self.item_in_tree = items.LongSword()
        else:
            self.item_in_tree = items.Axe()
    def enter (self):
        announce ("The thickness and visability have gotten worse, aswell as a massive mountain blocking your path to the north")
        announce ("You see a shiny metal object in the tree")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'south'):
            announce('You try and make youre way back where the trees arnt so thick.')
            config.the_player.next_loc = self.main_location.locations['trees1']
        elif (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['hotspring']
        elif (verb == 'west'):
            config.the_player.next_loc = self.main_location.locations['small cave']
        if(verb == 'take'):
            if self.item_in_tree == None:
                announce ('You dont see anything to take')
            else:
                item = self.item_in_tree
                announce ('you take the '+item.name+' from the tree.')
                config.the_player.add_to_inventory([item])
                self.item_in_tree = None
                config.the_player.go = True

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
        announce (f"You find a stange crystal in the water of the hotspring it seems to be {self.main_location.colors[2]}")                #Randomization factor
    
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
        self.verbs['red'] = self
        self.verbs['white'] = self
        self.verbs['blue'] = self
    def enter (self):
        announce('You have stumbled apon a bridge, Hello travlers a strange spirt says')
        announce('the only way to pass is to eneter the correct passcode sequence')
        self.main_location.Checkpuzzle()

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'northwest'):
            config.the_player.next_loc = self.main_location.locations['cavern']
        if (verb == 'south'):
            config.the_player.next_loc = self.main_locations.locations['hotspring'] 
    def puzzle_reward (self):
        for i in config.the_player.get_pirates():
            i.lucky = True
            i.sick = False

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
            config.the_player.next_loc = self.main_location.locations['in small cave']
        if (verb == 'southeast'):
            config.the_player.next_loc = self.main_location.locations['trees1']
        if (verb == 'east'):
            config.the_player.next_loc = self.main_location.locations['trees2']

class In_small_cave (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = 'in small cave'
        self.verbs['west'] = self
        self.verbs['south'] = self
        self.verbs['northeast'] =self
        self.event_chance = 100
        self.events.append(man_eating_bats.ManEatingBats())

    def enter (self):
        announce ('You enter the small cave however one of youre crewmates trips on a rock')
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
        for i in config.the_player.get_pirates():
            i.health = i.max_health
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
        self.event_chance = 100
        self.events.append(giant_bat_boss.GiantBatBoss())
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
        self.verbs['take'] = self
        self.weapons = True
    def enter (self):
        announce('You have entered the armory. Gear up to get off the island')

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == 'south'):
            config.the_player.next_loc = self.main_location.locations['cavern']
        if verb == 'take':
            if self.weapons == False:
                print('You cant take anymore items')
            
            else:    

                weapons = [items.HandPistol(), items.Trident(), items.BroadSword()]
                print('Available weapons:')
                for i, weapon in enumerate(weapons, 1):
                    print(f"{i}. {weapon}")
                choice = input('Enter which weapons you would like to recieve')
                if choice.isdigit():
                    choice = int(choice)
                    self.weapons = False
                    config.the_player.go = True
                    if 1 <= choice <= len(weapons):
                        chosen_weapon = weapons[choice - 1]
                        print(f'You have recieved {chosen_weapon}')
                        config.the_player.add_to_inventory([chosen_weapon])
                    else:
                        print("Please choose a valid weapon")
                else:
                    print("Please enter a valid number")
        else:
            print('Use the verb "take" to buy a weapon')
