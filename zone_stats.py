import random
import numpy as np
from player import Player
current_filter = 'none'  # Options: 'none', 'goop', 'gold', 'defense'

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

    # Create players and assign spawn zones
    players = []
    spawn_indices = spawn_points[num_players]
    for i, spawn_index in enumerate(spawn_indices):
        player_id = i
        player_name = f"Player {i + 1}"
        player = Player(player_id, player_name, spawn_index)
        players.append(player)

    # Create zones
    for index in range(num_faces):
        zone_type = 'normal'
        owner = None

        # Check if the zone is a spawn zone
        player_owner = next((p for p in players if p.spawn_zone_index == index), None)
        if player_owner:
            zone_type = 'spawn'
            owner = player_owner  # Assign the player as the owner (temporarily)

        zone = Zone(index=index, zone_type=zone_type, owner=None)
        zones.append(zone)

    return zones, players

def generate_zone_stats(zones):
    mu_goop = 50
    sigma_goop = 15
    mu_gold = 550
    sigma_gold = 200
    balancing_value = 100  # Adjust this for game balance

    for zone in zones:
        if zone.zone_type == 'spawn':
            # Set default values for spawn zones
            zone.goop_sv = 85  # 85% Goop saturation
            zone.gold_py = 850  # 850 Gold per year
        else:
            # Generate normally distributed goop saturation value (goop_sv)
            goop_sv = np.random.normal(mu_goop, sigma_goop)
            goop_sv = max(0, min(100, goop_sv))  # Clamp to [0, 100]

            # Generate normally distributed gold per year (gold_py)
            gold_py = np.random.normal(mu_gold, sigma_gold)
            gold_py = max(100, min(1000, gold_py))  # Clamp to [100, 1000]

            # Assign generated values to the zone
            zone.goop_sv = goop_sv
            zone.gold_py = gold_py

        # Calculate defense stat for all zones
        zone.defense = zone.goop_sv * zone.gold_py + balancing_value

    return zones

def calculate_color(zone, min_values, max_values, current_filter):
    if current_filter == 'none':
        if zone.zone_type == 'spawn':
            return (255, 0, 0)  # Red color for spawn zones
        else:
            return (0, 255, 255)  # Cyan color for normal zones
    else:
        # Get the stat to filter on
        if current_filter == 'goop':
            stat = zone.goop_sv
            color_scheme = 'green'
        elif current_filter == 'gold':
            stat = zone.gold_py
            color_scheme = 'yellow'
        elif current_filter == 'ownership':
            return 200, 200, 200

        elif current_filter == 'defense':
            stat = zone.defense
            color_scheme = 'grey'
        else:
            stat = 0
            color_scheme = 'white'

        # Normalize the stat between 0 and 1
        min_stat = min_values[current_filter]
        max_stat = max_values[current_filter]
        normalized_stat = (stat - min_stat) / (max_stat - min_stat)
        normalized_stat = max(0, min(1, normalized_stat))

        # Calculate color based on the color scheme
        if color_scheme == 'green':
            # Shades of green
            intensity = int(normalized_stat * 255)
            return 0, intensity, 0
        elif color_scheme == 'yellow':
            # Shades of yellow (red + green)
            intensity = int(normalized_stat * 255)
            return intensity, intensity, 0
        elif color_scheme == 'grey':
            # Shades of grey
            intensity = int(normalized_stat * 255)
            return intensity, intensity, intensity
        else:
            return 255, 255, 255  # Default white color

def calculate_defense_range(zones, balancing_value=100):
    # Calculate minimum and maximum defense values from the zones
    defenses = [zone.defense for zone in zones if zone.zone_type != 'spawn']
    min_defense_actual = min(defenses)
    max_defense_actual = max(defenses)

    # Return actual min and max for better color distribution
    return min_defense_actual, max_defense_actual

def calculate_gold(zone):
    """
    Calculate the gold generated by a zone.
    """
    return zone.gold_py / 12  # Assuming gold_py is annual, this gives monthly gold
