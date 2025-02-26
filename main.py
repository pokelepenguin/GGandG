import spherey_visualization as vis
import zone_stats
import game_logic  # Renamed from game
import game_menu
import pygame
import company_start_menu
from datetime import datetime, timedelta
from company import Company  # Import the Company class
import spherey_core as core
from monthly_update import monthly_update  # Import the monthly_update function
import threading

# Number of players (choose from 2, 4, 5, 8)
num_players = 5

# Create the spherical mesh with 2 subdivisions
print("Creating spherical mesh")
vertices, faces = core.create_spherical_mesh(subdivisions=2)
print(f"Spherical mesh created with {len(vertices)} vertices and {len(faces)} faces")

# Assign zones and players
print("Assigning zones and players")
zones, players = zone_stats.assign_zones(faces, num_players)
print(f"{len(zones)} zones assigned to {len(players)} players")

# Generate stats for each zone
print("Generating stats for each zone")
zones = zone_stats.generate_zone_stats(zones)
print("Zone stats generated")

# For demonstration, we'll just use the first player
current_player = players[0]

# Custom event for monthly update
MONTHLY_UPDATE_EVENT = pygame.USEREVENT + 1

def main_game_loop(screen, current_player, vertices, faces, zones):
    while True:
        pygame.display.set_caption('Gold, Goop, and Gambling')
        game_menu.main_game_menu(screen, current_player, vertices, faces, zones)
        vis.visualize_sphere_pygame(vertices, faces, zones, screen, current_player)

def monthly_update_loop(companies, zones, players):
    while True:
        monthly_update(companies, zones, players)
        pygame.time.wait(5000)  # 5 seconds delay

def main():
    try:
        print("Initializing Pygame")
        pygame.init()
        print("Pygame initialized")

        print("Setting up the display mode")
        screen = pygame.display.set_mode((1920, 1080))
        print("Display mode set")

        companies = []
        print("Starting company creation menu")
        company = company_start_menu.company_creation_menu(current_player, screen, zones, current_player.spawn_zone_index)
        if company:
            companies.append(company)
            print(f"Company created: {company}")
        else:
            print("Failed to create company")
            return

        update_thread = threading.Thread(target=monthly_update_loop, args=(companies, zones, players))

        update_thread.start()
        main_game_loop(screen, current_player, vertices, faces, zones)
        update_thread.join()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
