# zone_stats.py

import random
import numpy as np


class Zone:
    def __init__(self, index, zone_type='normal', owner=None, properties=None):
        self.index = index
        self.zone_type = zone_type
        self.owner = owner  # Company or player who owns the zone
        self.properties = properties or {}  # Additional features

        # Initialize stats
        self.goop_sv = 0  # Goop saturation value (0 to 100)
        self.gold_py = 0  # Gold generation per year (100 to 1000)
        self.defense = 0  # Defense stat

    def __repr__(self):
        return (f"Zone(index={self.index}, type='{self.zone_type}', owner={self.owner}, "
                f"goop_sv={self.goop_sv:.2f}, gold_py={self.gold_py:.2f}, defense={self.defense:.2f})")


def assign_zones(faces, num_players):
    num_faces = len(faces)
    zones = []

    # Define spawn points for different player counts
    spawn_points = {
        2: [152, 264],
        4: [7, 40, 207, 244],
        5: [11, 114, 143, 148, 204],
        8: [5, 26, 50, 137, 210, 241, 258, 309]
    }

    # Ensure the number of players is supported
    if num_players not in spawn_points:
        raise ValueError("Unsupported number of players. Choose from 2, 4, 5, or 8.")

    # Set the spawn zones and assign to players
    spawn_indices = spawn_points[num_players]
    player_indices = list(range(num_players))
    random.shuffle(player_indices)  # Randomize player order
    player_spawns = dict(zip(spawn_indices, player_indices))

    for index in range(num_faces):
        if index in spawn_indices:
            zone_type = 'spawn'
            owner = player_spawns[index]
            properties = {'resource_yield': 5}  # High initial resource yield
        else:
            zone_type = 'normal'
            owner = None
            properties = {}

        zone = Zone(index=index, zone_type=zone_type, owner=owner, properties=properties)
        zones.append(zone)

    return zones


def generate_zone_stats(zones):
    mu_goop = 50
    sigma_goop = 15
    mu_gold = 550
    sigma_gold = 200
    balancing_value = 100  # Adjust this for game balance

    for zone in zones:
        # Generate normally distributed goop saturation value (goop_sv)
        goop_sv = np.random.normal(mu_goop, sigma_goop)
        goop_sv = max(0, min(100, goop_sv))  # Clamp to [0, 100]

        # Generate normally distributed gold per year (gold_py)
        gold_py = np.random.normal(mu_gold, sigma_gold)
        gold_py = max(100, min(1000, gold_py))  # Clamp to [100, 1000]

        # Calculate defense stat
        defense = goop_sv * gold_py + balancing_value

        # Assign values to the zone
        zone.goop_sv = goop_sv
        zone.gold_py = gold_py
        zone.defense = defense

    return zones


def calculate_color(zone, min_defense, max_defense):
    if zone.zone_type == 'spawn':
        # Spawn zones are colored red
        return (255, 0, 0)  # Red color
    else:
        # Normalize defense between 0 and 1
        normalized_defense = (zone.defense - min_defense) / (max_defense - min_defense)
        normalized_defense = max(0, min(1, normalized_defense))

        # Invert normalized defense to get darker color for higher defense
        inverted_defense = 1 - normalized_defense

        # Calculate green intensity (50 to 255 to avoid too dark colors)
        min_intensity = 50
        max_intensity = 255
        green_intensity = int(min_intensity + inverted_defense * (max_intensity - min_intensity))
        green_intensity = max(0, min(255, green_intensity))

        # Return RGB color (R=0, G=green_intensity, B=0)
        return (0, green_intensity, 0)


def calculate_defense_range(zones, balancing_value=100):
    # Calculate minimum and maximum defense values from the zones
    defenses = [zone.defense for zone in zones if zone.zone_type != 'spawn']
    min_defense_actual = min(defenses)
    max_defense_actual = max(defenses)

    # Return actual min and max for better color distribution
    return min_defense_actual, max_defense_actual

