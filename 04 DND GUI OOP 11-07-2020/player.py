# "Player" has a "Backpack"
class Backpack:
    def __init__(self):
        self.gold = 50


class Player:
    def __init__(self, name):
        self.name = name
        self.backpack = Backpack()


player = Player("jombi")