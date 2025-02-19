import spherey
import zone_stats
import game
import menu
import pygame

# Number of players (choose from 2, 4, 5, 8)
num_players = 5

# Create the spherical mesh with 2 subdivisions
vertices, faces = spherey.create_spherical_mesh(subdivisions=2)

# Assign zones and players
zones, players = zone_stats.assign_zones(faces, num_players)

# Generate stats for each zone
zones = zone_stats.generate_zone_stats(zones)

# Store zones globally for access in game.py
game.game_zones = zones  # Assign the zones to a global variable in game.py

# For demonstration, we'll just use the first player
current_player = players[0]

# Initialize Pygame screen for menu
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Company Creation')

# Open company creation menu for the current player
menu.company_creation_menu(current_player, screen)

# After company creation, proceed to the main game visualization
pygame.display.set_caption('Gold, Goop, and Gambling')
spherey.visualize_sphere_pygame(vertices, faces, zones)


