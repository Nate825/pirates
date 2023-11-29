class headers
class Island (location.Location):
    def __init__ (self, x, y, w):
    def enter (self, ship):
    def visit (self):
class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
    def enter(self)
    def process_verb (self, verb, cmd_list, nouns):
class Trees (location.SubLocation):
    def __init__ (self, m):
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['take'] = self
    def enter (self):

    def process_verb(self, verb, cmd_list, nouns):