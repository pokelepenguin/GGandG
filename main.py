import spherey_visualization as vis
import zone_stats
import game_logic  # Renamed from game
import game_menu
import pygame
import company_start_menu
from datetime import datetime, timedelta
from company import Company  # Import the Company class
import spherey_core as core
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

# Function to perform monthly updates
def monthly_update(companies, zones):
    for company in companies:
        print(f"Updating company: {company.company_id}")
        # Generate gold for each triangle owned
        company.update_triangle_income(zones)

        # Apply interest to loans
        company.update_interest_expense()

        # Update monthly income history
        company.update_monthly_income_history()

        # Update credit score
        company.update_credit_score()

def main():
    try:
        print("Initializing Pygame")
        # Initialize Pygame screen for menu
        pygame.init()
        print("Pygame initialized")

        print("Setting up the display mode")
        screen = pygame.display.set_mode((1920, 1080))
        print("Display mode set")

        # List of companies
        companies = []
        print("Entering main loop")

        # Start with the company creation menu
        print("Starting company creation menu")
        company = company_start_menu.company_creation_menu(current_player, screen, zones, current_player.spawn_zone_index)
        if company:
            companies.append(company)
            print(f"Company created: {company}")
            monthly_update(companies, zones)  # Start monthly updates immediately
        else:
            print("Failed to create company")
            return

        while True:
            pygame.display.set_caption('Gold, Goop, and Gambling')

            # Regular game updates
            print("Running game updates")
            game_menu.main_game_menu(screen, current_player, vertices, faces, zones)
            vis.visualize_sphere_pygame(vertices, faces, zones, screen, current_player)

            monthly_update(companies, zones)  # Perform monthly update

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
