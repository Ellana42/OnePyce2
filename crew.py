from item import Food


class Crew:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.inventory = []
        self.crew = [Luffy()]
        self.current_nakama = 0
        self.energy_level = 101

    def switch_nakama(self):
        self.current_nakama = (self.current_nakama + 1) % len(self.crew)
        return ['You can count on your nakamas !']

    def use_item(self):
        if len(self.inventory) == 0:
            return ['No item to use']
        else:
            for item in self.inventory:
                if type(item) is Food:
                    self.energy_level += item.get_energetic_value()
                    return ['Yummy !']
                else:
                    return ['There\'s a problem with item generation']

    def take_item(self, item):
        self.inventory.append(item)

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y

    def get_nakama(self):
        return self.crew[self.current_nakama]

    def get_inventory(self):
        return self.inventory

    def get_crew(self):
        return self.crew

    def gets_tired(self, terrain):
        self.energy_level -= self.crew[self.current_nakama].tiredness[terrain]
        if self.energy_level <= 0:
            self.die_from_exhaustion()
            return ['That was too much ! I\'m going to rest for a bit ...']
        else:
            return []

    def die_from_exhaustion(self):
        self.x = 0
        self.y = 0
        self.energy_level = 100

    def add_nakama(self, nakama):
        self.crew.append(nakama)


class Nakama:
    def __init__(self):
        self.icon = ' '
        self.tiredness = {}
        self.standard_tiredness = 1

    def get_icon(self):
        return self.icon

    def get_tiredness(self, terrain):
        if terrain in self.tiredness:
            return self.tiredness[terrain]
        else:
            return self.standard_tiredness

    @classmethod
    def get_possible_nakamas(cls):
        return Nami(), Zorro(), Sanji(), Usopp()

    @classmethod
    def get_nakama_skin(cls):
        return {type(nakama): nakama.icon for nakama in Nakama.get_possible_nakamas()}


class Luffy(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = 'L '
        self.tiredness = {'ground': 1, 'mountain': 3, 'water': 100}


class Nami(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = 'N '
        self.tiredness = {'ground': 3, 'mountain': 10, 'water': 1}


class Zorro(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = 'Z '
        self.tiredness = {'ground': 10, 'mountain': 10, 'water': 10}


class Usopp(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = 'U '
        self.tiredness = {'ground': 20, 'mountain': 20, 'water': 10}


class Sanji(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = 'S '
        self.tiredness = {'ground': 1, 'mountain': 5, 'water': 10}
