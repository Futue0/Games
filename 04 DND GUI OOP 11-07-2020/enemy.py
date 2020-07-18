class Goblin:
    def __init__(self):
        self.attack = 1
        self.defence = 1


class Boss(Goblin):
    def __init__(self):
        self.attack = 2
        self.defence = 2


test_gobbo = Goblin()
print(test_gobbo.attack)

test_boss = Boss()
print(test_boss.attack)