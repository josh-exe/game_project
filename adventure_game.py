import random

# Location Class Definition
class Location:
    def __init__(self, name, description, enemies, items):
        self.name = name
        self.description = description
        self.enemies = enemies  # List of enemies in this location
        self.items = items  # List of items in this location

    def explore(self):
        print(f"\nYou have arrived at {self.name}. {self.description}")
        print("Do you want to explore the area?")
        action = input("[1] Explore the location\n[2] Leave the location\n> ").strip()

        if action == "1":
            # Encounter enemies
            if self.enemies:
                enemy = random.choice(self.enemies)
                print(f"\nA wild {enemy.name} appears!")
                return enemy
            else:
                print("No enemies are around. You find some items instead.")
                return self.items
        else:
            print("You leave the location.")
            return None  # Return None if the player leaves the location

# Combat system: Player vs. Enemy
def combat(player, enemy, location_items):
    print(f"\nBattle begins! You are facing a {enemy.name}.")
    
    while player.health > 0 and enemy.health > 0:
        print(f"\nYour health: {player.health}")
        print(f"{enemy.name}'s health: {enemy.health}")
        
        # Player's turn
        print("\nChoose an action:")
        print("[1] Attack")
        print("[2] Defend")
        print("[3] Use Item")
        print("[4] Flee")
        action = input("> ").strip()

        if action == "1":  # Attack
            damage = random.randint(5, 15) + player.attack - enemy.defense
            damage = max(damage, 0)  # Prevent negative damage
            # Add chance for critical hit
            if random.random() < 0.1:  # 10% chance for a critical hit
                damage *= 2
                print("\nCritical Hit!")
            enemy.health -= damage
            print(f"\nYou attack the {enemy.name} and deal {damage} damage!")
        elif action == "2":  # Defend
            player.defending = True
            print("\nYou brace yourself and prepare to defend the next attack!")
        elif action == "3":  # Use Item
            if player.inventory:
                print("\nYour inventory:")
                for i, item in enumerate(player.inventory, 1):
                    print(f"{i}. {item.name}")
                item_choice = int(input("> ")) - 1
                item = player.inventory[item_choice]
                item.effect(player)
                player.inventory.remove(item)  # Remove used item
            else:
                print("\nYou have no items left!")
        elif action == "4":  # Flee
            if random.random() < 0.5:
                print("\nYou successfully flee from the battle!")
                return True  # Indicating player fled successfully
            else:
                print("\nYou failed to flee! The battle continues.")

        # Enemy's turn
        if enemy.health > 0:
            if random.random() < 0.5:
                damage = random.randint(5, 15) + enemy.attack - player.defense
                damage = max(damage, 0)  # Prevent negative damage
                if player.defending:
                    damage = max(damage - 3, 0)  # Reduce damage if defending
                    print("\nYou defended successfully!")
                player.health -= damage
                print(f"\n{enemy.name} attacks you and deals {damage} damage.")
                player.defending = False  # Reset defense for the next round

    if player.health <= 0:
        print("\nYou have been defeated! Game Over.")
        return False  # Player lost the combat
    elif enemy.health <= 0:
        print(f"\nYou have defeated the {enemy.name}!")
        # Give the player an item from the location after a successful battle
        item = random.choice(location_items)
        player.add_item(item)
        print(f"\nYou have received a {item.name}!")
        return True  # Player won the combat

# Sample classes for items and enemies to use with this code
class Item:
    def __init__(self, name, type_, effect):
        self.name = name
        self.type = type_
        self.effect = effect

class Enemy:
    def __init__(self, name, health, attack, defense, speed):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed

class Character:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.speed = 10
        self.inventory = []
        self.defending = False  # For defense status in combat

        # Set class-specific stats and abilities
        self.set_class_stats()

    def set_class_stats(self):
        """Modify stats based on class."""
        class_stats = {
            "Paladin": {"health": 120, "attack": 8, "defense": 12, "speed": 6},
            "Necromancer": {"health": 80, "attack": 15, "defense": 4, "speed": 10},
            "Hunter": {"health": 100, "attack": 12, "defense": 6, "speed": 12},
            "Berserker": {"health": 90, "attack": 18, "defense": 3, "speed": 9},
            "Sorcerer": {"health": 75, "attack": 20, "defense": 2, "speed": 11},
            "Druid": {"health": 110, "attack": 10, "defense": 8, "speed": 8},
            "Assassin": {"health": 95, "attack": 14, "defense": 5, "speed": 15},
            "Knight": {"health": 130, "attack": 10, "defense": 15, "speed": 5},
            "Wizard": {"health": 70, "attack": 18, "defense": 3, "speed": 10},
            "Monk": {"health": 110, "attack": 12, "defense": 7, "speed": 10},
            "Shaman": {"health": 95, "attack": 13, "defense": 6, "speed": 9},
            "Warlock": {"health": 85, "attack": 17, "defense": 4, "speed": 10},
            "HIM": {"health": 1000, "attack": 1000, "defense": 1000, "speed": 1000},  # HIM stats set to 1000
        }

        stats = class_stats.get(self.char_class, {})
        self.health = stats.get("health", 100)
        self.attack = stats.get("attack", 10)
        self.defense = stats.get("defense", 5)
        self.speed = stats.get("speed", 10)

    def add_item(self, item):
        self.inventory.append(item)

    def special_ability(self):
        """Class-based special ability (e.g., Berserker Rage, Paladin Shield)."""
        if self.char_class == "Berserker":
            print("You enter a berserker rage, increasing your attack for this turn!")
            self.attack += 10  # Temporary increase in attack
        elif self.char_class == "Paladin":
            print("You use your shield to defend against the next attack!")
            self.defending = True  # Set defending status to true
        # Add more class abilities here

# Game Loop with class options based on the player's name
def game():
    print("Welcome to the game!")
    name = input("Enter your character's name: ").strip()

    # Determine which classes are available based on the player's name
    class_options = ["Paladin", "Necromancer", "Hunter", "Berserker", "Sorcerer", "Druid", "Assassin", "Knight", "Wizard", "Monk", "Shaman", "Warlock"]

    # If player name is "im him", add "HIM" to the class options
    if name.lower() == "im him":
        class_options.append("HIM")

    # Let the player choose a class from the available options
    print("Choose your class:")
    for idx, class_name in enumerate(class_options, 1):
        print(f"{idx}. {class_name}")
    class_choice_idx = int(input("> ")) - 1
    class_choice = class_options[class_choice_idx]

    player = Character(name, class_choice)

    # Add some starting items for the player (for demonstration purposes)
    player.add_item(Item("Health Potion", "healing", lambda p: setattr(p, "health", min(p.health + 30, 100))))
    player.add_item(Item("Mana Potion", "healing", lambda p: print("You regain 20 mana (not implemented)")))

    # List of available locations
    locations = [
    Location("Forest", "A dark and gloomy forest filled with wild creatures.", [Enemy("Goblin", 30, 5, 0, 5)], [Item("Health Potion", "healing", 30)]),
    Location("Cave", "A dark cave with a mysterious aura.", [Enemy("Orc", 50, 10, 0, 6)], [Item("Mana Potion", "healing", 20)]),
    Location("Village", "A small village with friendly villagers.", [], [Item("Sword", "weapon", 10)]),
    
    # New locations
    Location("Desert", "A vast, hot desert with nothing but sand as far as the eye can see.", [Enemy("Sand Demon", 40, 6, 0, 10)], [Item("Water Flask", "healing", 10)]),
    Location("Mountain Peak", "A towering mountain with a chilling wind blowing at the summit.", [Enemy("Mountain Troll", 60, 15, 0, 7)], [Item("Ice Shield", "defense", 10)]),
    Location("Swamp", "A murky swamp filled with dangerous creatures lurking in the fog.", [Enemy("Swamp Hag", 45, 8, 5, 4)], [Item("Poison Vial", "weapon", 15)]),
    Location("Abandoned Castle", "An eerie and abandoned castle filled with dust and cobwebs.", [Enemy("Specter", 30, 5, 10, 3)], [Item("Ghost Lantern", "misc", "Can reveal hidden enemies.")]),
    Location("Ice Cavern", "A frozen cavern with glowing crystals embedded in the walls.", [Enemy("Ice Elemental", 70, 8, 20, 5)], [Item("Frozen Sword", "weapon", 15)]),
    Location("Volcano", "A dangerous, active volcano with flowing lava.", [Enemy("Lava Beast", 80, 20, 0, 8)], [Item("Fireproof Cloak", "armor", 15)]),
    Location("Enchanted Forest", "A magical forest where time seems to pass differently.", [Enemy("Fairy Warrior", 50, 10, 15, 6)], [Item("Magic Elixir", "healing", 50)]),
    Location("Dark Abyss", "A bottomless pit where only the brave dare to venture.", [Enemy("Abyssal Horror", 100, 25, 5, 10)], [Item("Abyssal Blade", "weapon", 20)]),
    Location("Graveyard", "An ancient graveyard where restless souls wander.", [Enemy("Zombie", 40, 5, 0, 2)], [Item("Tomb Key", "misc", "Opens ancient tombs.")]),
    Location("Haunted Mansion", "A grand mansion, haunted by spirits of the past.", [Enemy("Ghost Knight", 60, 15, 0, 6)], [Item("Spectral Armor", "armor", 10)]),
    Location("Ruins of Eldar", "The ruins of an ancient city, crumbling and forgotten by time.", [Enemy("Guardian Statue", 50, 10, 0, 7)], [Item("Ancient Relic", "misc", "Can boost your strength.")]),
    Location("Crystal Cave", "A cave full of glowing crystals, creating an almost magical atmosphere.", [Enemy("Crystal Golem", 70, 12, 5, 4)], [Item("Crystal Staff", "weapon", 18)]),
    Location("Jungle", "A dense jungle filled with strange, exotic creatures.", [Enemy("Jungle Beast", 55, 10, 0, 9)], [Item("Vine Whip", "weapon", 10)]),
    Location("Sky Castle", "A castle floating in the sky, suspended by ancient magic.", [Enemy("Sky Serpent", 60, 15, 10, 8)], [Item("Wings of the Sky", "misc", "Allows limited flight.")]),
    Location("Underground Cavern", "A series of underground tunnels that stretch for miles.", [Enemy("Cave Spider", 40, 8, 0, 6)], [Item("Spider Silk Rope", "misc", "Can be used to escape dangerous situations.")]),
    Location("Frozen Tundra", "A desolate frozen tundra with blizzards blocking your path.", [Enemy("Frost Giant", 80, 25, 0, 3)], [Item("Frostbite Gauntlets", "armor", 12)]),
    Location("Crystal Lake", "A serene lake surrounded by crystal clear water.", [Enemy("Water Nymph", 50, 5, 20, 6)], [Item("Water Crystal", "misc", "Can summon water-based spells.")]),
    Location("Stormy Coast", "A rocky coastline where the sea crashes against the rocks in violent waves.", [Enemy("Sea Leviathan", 120, 30, 0, 4)], [Item("Stormcaller Horn", "misc", "Can summon a storm.")]),
    Location("Goblin Camp", "A camp of mischievous goblins, they are not friendly to strangers.", [Enemy("Goblin Chief", 60, 10, 0, 5)], [Item("Goblin Dagger", "weapon", 8)]),
    Location("Mystic Meadow", "A peaceful meadow that hides dark secrets beneath its beauty.", [Enemy("Witch", 40, 10, 15, 5)], [Item("Potion of Invisibility", "healing", 30)]),
    Location("Desolate Wasteland", "A barren wasteland with nothing but dry, cracked earth.", [Enemy("Scavenger", 35, 5, 0, 6)], [Item("Dust Mask", "armor", 5)]),
    Location("Feywild", "A mystical realm where magic flows freely and time works differently.", [Enemy("Fey Warrior", 70, 12, 20, 10)], [Item("Fey Blade", "weapon", 20)]),
    Location("Sunken Ship", "An ancient shipwreck lying at the bottom of the sea.", [Enemy("Shipwreck Ghost", 50, 10, 0, 6)], [Item("Captain's Sword", "weapon", 12)]),
    Location("Magma Chamber", "A molten chamber beneath the earth, filled with flowing magma.", [Enemy("Magma Elemental", 90, 18, 0, 5)], [Item("Magma Armor", "armor", 20)]),
    Location("Obsidian Desert", "A desert made of sharp, black obsidian rocks under the hot sun.", [Enemy("Obsidian Demon", 70, 15, 0, 7)], [Item("Obsidian Blade", "weapon", 20)]),
    Location("The Nexus", "A mystical point where different realms of reality converge.", [Enemy("Nexus Keeper", 100, 30, 25, 15)], [Item("Nexus Orb", "misc", "Allows travel between realms.")]),
    Location("Ancient Library", "A grand library filled with knowledge and hidden lore.", [Enemy("Arcane Guardian", 60, 12, 20, 5)], [Item("Spellbook", "misc", "Can teach new spells.")]),
]
    
    visited_locations = set()  # Set to track visited locations

    while True:
        # Filter out locations the player has already visited
        unvisited_locations = [loc for loc in locations if loc.name not in visited_locations]

        if not unvisited_locations:  # No more locations to visit
            print("You have explored all locations. The game is over!")
            break

        current_location = random.choice(unvisited_locations)

        # Mark this location as visited
        visited_locations.add(current_location.name)

        encounter = current_location.explore()

        if encounter is None:  # If the player left the location
            print("You leave the location and head to a new one.")
            continue  # Proceed to a new random location
        elif isinstance(encounter, list):  # Player finds items instead of enemies
            print("You find the following items:")
            for item in encounter:
                print(item.name)
        else:  # Encounter an enemy
            result = combat(player, encounter, current_location.items)
            if result:  # If the player wins
                print("You defeated the enemy! Would you like to continue exploring?")
                continue_choice = input("[1] Explore more\n[2] Leave the location\n> ").strip()
                if continue_choice == "2":
                    print("You leave the location and head to a new one.")
                    continue  # Proceed to a new random location
            else:
                print("Game over.")
                break

if __name__ == "__main__":
    game()
