from random import randrange, randint


class Item:
    def __init__(self):
        self.id_number = randint(0, 100)

    def get_item_id(self):
        return self.id_number


class Food(Item):
    def __init__(self):
        super().__init__()
        self.energetic_value = randrange(50)

    def get_energetic_value(self):
        return self.energetic_value


class Npc:
    def __init__(self):
        self.id_number = randint(100, 200)

    def talk(self):
        return str(self.id_number) + '=' * 10 + ' Good morning peasant ! ' + '=' * 10


