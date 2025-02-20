class Player:
    def __init__(self):
        self.traits = {
            'aggression': 0,
            'creativity': 0,
            'empathy': 0
        }
        self.inventory = []
        self.current_location = 'terminal_room'

class Location:
    def __init__(self, name, base_description, trait_modifiers, actions, objects=None, items=None):
        self.name = name
        self.base_description = base_description
        self.trait_modifiers = trait_modifiers
        self.actions = actions
        self.objects = objects or {}
        self.items = items or []

    def get_description(self, player):
        desc = self.base_description
        for trait, modifier in self.trait_modifiers.items():
            if player.traits[trait] > 0:
                desc += " " + modifier
        if self.items:
            desc += " You see: " + ", ".join(self.items)
        return desc

    def look_at(self, object_name):
        return self.objects.get(object_name, "There's no such thing here.")

def parse_input(input_str, player, locations):
    words = input_str.lower().split()
    if not words:
        return player.current_location
    command = words[0]
    args = ' '.join(words[1:])
    current_location = locations[player.current_location]
    if command == 'look':
        if args:
            print(current_location.look_at(args))
        else:
            print(current_location.get_description(player))
    elif command == 'take':
        if args:
            if args in current_location.items:
                player.inventory.append(args)
                current_location.items.remove(args)
                print(f"You take the {args}.")
            else:
                print("There's no such item here.")
        else:
            print("Take what?")
    elif command == 'inventory':
        print("Inventory:", player.inventory)
    elif command == 'quit':
        return 'quit'
    elif input_str in current_location.actions:
        action_func = current_location.actions[input_str]
        result = action_func(player)
        if isinstance(result, str):
            return result
        else:
            return player.current_location
    else:
        print("I don't understand that command.")
    return player.current_location

# Define locations
def enter_simulation(player):
    return 'meadow'

terminal_room = Location(
    name='Terminal Room',
    base_description='You are in a dark, metallic room aboard a space station. A glowing terminal hums in front of you. The screen flickers: "Welcome, player. Enter the simulation?"',
    trait_modifiers={},
    actions={
        'yes': enter_simulation,
        'enter': enter_simulation,
        'no': lambda p: 'quit',
    },
    objects={}
)

meadow_objects = {
    'giant': 'The giant is a hulking mass of flesh, his skin pocked with scars. His eyes glint with cruel amusement.',
    'green chalice': 'The green liquid fizzes and spits, releasing a sharp, acidic smell.',
    'red chalice': 'The red liquid is thick and syrupy, with a sweet, cloying scent.',
    'table': 'A rough stone table, weathered by time.'
}

def drink_green(player):
    print("You drink the green liquid. It burns your throat, and your vision blurs. You collapse.")
    player.traits['aggression'] += 1
    return 'glass_forest'

def drink_red(player):
    print("You drink the red liquid. It tastes sweet, but then your body seizes up. You fall to the ground, paralyzed.")
    player.traits['empathy'] += 1
    return 'frozen_tundra'

def attack_giant(player):
    print("You charge at the giant, but he swats you away like a fly. 'Foolish child,' he laughs.")
    player.traits['aggression'] += 2
    return 'meadow'

def talk_to_giant(player):
    print("You try to speak to the giant. 'Why are you doing this?' you ask. He sneers, 'Because it's fun.'")
    player.traits['empathy'] += 1
    return 'meadow'

def burrow_eye(player):
    print("You leap onto the giant's face and burrow into his eye. He screams, and the world shifts. You find yourself in a castle.")
    player.traits['creativity'] += 3
    return 'castle'

meadow = Location(
    name='Meadow',
    base_description="You stand in a misty meadow beneath a bruised purple sky. A massive giant looms ahead, reclining against a gnarled tree. Two chalices sit on a stone table before him: one green, one red. The giant speaks: 'Drink, little one. One is life, one is death. Choose, or I’ll crush you.'",
    trait_modifiers={},
    actions={
        'drink green': drink_green,
        'drink red': drink_red,
        'attack giant': attack_giant,
        'talk to giant': talk_to_giant,
        'burrow through eye': burrow_eye,
    },
    objects=meadow_objects
)

glass_forest_trait_modifiers = {
    'empathy': 'You hear a faint sobbing from the west.',
    'creativity': 'You notice patterns in the glass trees that seem to point north.'
}

def go_north(player):
    return 'frozen_lake'

def go_west(player):
    if player.traits['empathy'] > 0:
        return 'child_encounter'
    else:
        print("You wander west but find nothing of interest.")
        return 'glass_forest'

def touch_glass_tree(player, location):
    if player.traits['creativity'] > 0 and 'glass shard' not in location.items:
        location.items.append('glass shard')
        print("You notice a loose glass shard on the tree.")
    else:
        print("The glass tree is sharp, but you don't find anything useful.")
    return location.name

glass_forest = Location(
    name='Glass Forest',
    base_description='You are in a forest of glass trees. The sky is crimson, and the air is still.',
    trait_modifiers=glass_forest_trait_modifiers,
    actions={
        'go north': go_north,
        'go west': go_west,
        'touch glass tree': lambda p: touch_glass_tree(p, glass_forest),
    },
    items=[]
)

def talk_to_child(player):
    print("You kneel down and ask the child why they are crying. 'I lost my way,' the child says. 'Can you help me?'")
    player.traits['empathy'] += 1
    return 'child_encounter'

child_encounter = Location(
    name='Child Encounter',
    base_description='You find a child sitting beneath a glass tree, crying. The child looks up at you with tear-filled eyes.',
    trait_modifiers={},
    actions={
        'talk to child': talk_to_child,
        'leave': lambda p: 'glass_forest',
    }
)

frozen_tundra = Location(
    name='Frozen Tundra',
    base_description='You are in a vast, icy tundra. The wind howls, and snow obscures your vision.',
    trait_modifiers={},
    actions={}
)

castle = Location(
    name='Castle',
    base_description='You are inside a majestic castle. The halls are lined with tapestries, and a sense of peace fills the air.',
    trait_modifiers={},
    actions={}
)

locations = {
    'terminal_room': terminal_room,
    'meadow': meadow,
    'glass_forest': glass_forest,
    'child_encounter': child_encounter,
    'frozen_tundra': frozen_tundra,
    'castle': castle,
}

def main():
    player = Player()
    while True:
        current_location = locations[player.current_location]
        print(current_location.get_description(player))
        action = input("> ").lower()
        result = parse_input(action, player, locations)
        if result == 'quit':
            print("You exit the simulation.")
            break
        elif result in locations:
            player.current_location = result

if __name__ == "__main__":
    main()