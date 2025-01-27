from item import Food
import terrain
import pygame


class Crew:
    def __init__(self, world):
        self.world = world
        self.x = 0
        self.y = 0
        self.inventory = []
        self.crew = [Luffy()]
        self.current_nakama = 0
        self.energy_level = 100
        self.wounded_nakamas = []

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
                    self.inventory.remove(item)
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

    def gets_tired(self, location):
        self.energy_level -= self.crew[self.current_nakama].get_tiredness(location)
        if self.energy_level <= 0:
            self.die_from_exhaustion()
            return ['That was too much !', 'I\'m going to rest for a bit ...']
        else:
            return []

    def die_from_exhaustion(self):
        self.respawn()
        self.energy_level = 100

    def add_nakama(self, nakama):
        self.crew.append(nakama)

    def is_in_the_crew(self, name):
        name_list = [nakama.name for nakama in self.crew]
        return name in name_list

    def get_corresponding_crew_member(self, name):
        crew_names = {nakama.name: nakama for nakama in self.crew}
        return crew_names[name]

    def respawn(self):
        self.world.player_respawn()

    def get_icon(self):
        return self.crew[self.current_nakama].get_icon()

    def get_energy(self):
        return self.energy_level


class Nakama:
    def __init__(self):
        self.icon = pygame.image.load('graphics/player_icons/zorro.png')
        self.tiredness = {}
        self.standard_tiredness = 1
        self.terrains_characteristics = {}
        self.health = 50
        self.name = ''
        self.combat_characteristics = {
            'close_attack': 10,
            'range_attack': 10,
            'morale_attack': 10,
            'close_defense': 10,
            'range_defense': 10,
            'morale_defense': 10
        }
        # Get the terrains descriptions and add a default value for tiredness
        for terrain_id, description in terrain.Terrain.get_terrains().items():
            if "tiredness" not in description:
                description["tiredness"] = self.standard_tiredness
            self.terrains_characteristics[terrain_id] = description

    def get_icon(self):
        return self.icon

    def get_nakama_tiredness_for(self, location_characteristics):
        return location_characteristics['tiredness']

    def get_tiredness(self, location):
        if location not in self.terrains_characteristics:
            return self.standard_tiredness
        return self.get_nakama_tiredness_for(self.terrains_characteristics[location])

    def get_name(self):
        return self.name

    @classmethod
    def get_possible_nakamas(cls):
        return Nami(), Zorro(), Sanji(), Usopp()

    @classmethod
    def get_nakama_skin(cls):
        return {type(nakama): nakama.icon for nakama in Nakama.get_possible_nakamas()}

    def get_health(self):
        return self.health


class Luffy(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = pygame.image.load('graphics/player_icons/luffy.png')
        self.name = 'Luffy'

    def get_nakama_tiredness_for(self, location):
        if location["type"] == "Mountain":
            return 3
        if location["type"] == "Water":
            return 100
        return super().get_nakama_tiredness_for(location)


class Nami(Nakama):
    def __init__(self):
        super().__init__()
        self.tiredness = {'X': 10, 'M': 10, 'S': 1, 'E': 1}
        self.tiredness = {'ground': 3, 'mountain': 10, 'water': 1}
        self.name = 'Nami'
        self.health = 25
        self.icon = pygame.image.load('graphics/player_icons/nami.png')


    def get_nakama_tiredness_for(self, location):
        if location["type"] == "Ground":
            return 3
        if location["type"] == "Mountain":
            return 10
        if location["type"] == "Water":
            return 1
        return super().get_nakama_tiredness_for(location)


class Zorro(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = pygame.image.load('graphics/player_icons/zorro.png')
        self.name = 'Zorro'

    def get_nakama_tiredness_for(self, location):
        if location["type"] == "Ground":
            return 3
        if location["type"] == "Mountain":
            return 10
        if location["type"] == "Water":
            return 1
        return super().get_nakama_tiredness_for(location)


class Usopp(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = pygame.image.load('graphics/player_icons/usopp.png')
        self.name = 'Usopp'
        self.health = 20

    def get_nakama_tiredness_for(self, location):
        if location["type"] == "Ground":
            return 3
        if location["type"] == "Mountain":
            return 10
        if location["type"] == "Water":
            return 1
        return super().get_nakama_tiredness_for(location)


class Sanji(Nakama):
    def __init__(self):
        super().__init__()
        self.icon = pygame.image.load('graphics/player_icons/sanji.png')
        self.name = 'Sanji'

    def get_nakama_tiredness_for(self, location):
        if location["type"] == "Ground":
            return 3
        if location["type"] == "Mountain":
            return 10
        if location["type"] == "Water":
            return 1
        return super().get_nakama_tiredness_for(location)
