import spherey_core as core
import spherey_visualization as vis
import zone_stats
import game
import game_menu
import pygame
import company_start_menu
from datetime import datetime, timedelta
from company import Company  # Import the Company class

# Number of players (choose from 2, 4, 5, 8)
num_players = 5

# Create the spherical mesh with 2 subdivisions
vertices, faces = core.create_spherical_mesh(subdivisions=2)

# Assign zones and players
zones, players = zone_stats.assign_zones(faces, num_players)

# Generate stats for each zone
zones = zone_stats.generate_zone_stats(zones)

# Store zones globally for access in game.py
game.game_zones = zones  # Assign the zones to a global variable in game.py

# For demonstration, we'll just use the first player
current_player = players[0]


# Function to perform monthly updates
def monthly_update(companies):
    for company in companies:
        # Generate gold for each triangle owned
        for zone in company.zones_owned:
            company.gold += zone_stats.calculate_gold(zone)

        # Apply interest to loans
        for loan in company.loans:
            loan_amount, interest_rate, term = loan
            company.total_liabilities += loan_amount * interest_rate

        # Update credit score
        company.update_credit_score()


def main():
    # Initialize Pygame screen for menu
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

    # List of companies
    companies = [Company(i, players[i], 10000) for i in range(num_players)]

    # Set up timer for monthly updates
    next_update_time = datetime.now() + timedelta(seconds=5)
    initial_setup_end_time = datetime.now() + timedelta(minutes=3)
    game_started = False

    while True:
        pygame.display.set_caption('Gold, Goop, and Gambling')

        # Check if the initial setup period has ended
        if datetime.now() >= initial_setup_end_time and not game_started:
            game_started = True
            company_start_menu.company_creation_menu(current_player, screen)

        if game_started:
            # Regular game updates
            game_menu.main_game_menu(screen, current_player, vertices, faces, zones)
            vis.visualize_sphere_pygame(vertices, faces, zones, screen, current_player)

            # Check if it's time for a monthly update
            if datetime.now() >= next_update_time:
                monthly_update(companies)
                next_update_time = datetime.now() + timedelta(seconds=5)


if __name__ == "__main__":
    main()