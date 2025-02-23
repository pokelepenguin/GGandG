import spherey_core as core
import spherey_visualization as vis
import zone_stats
import game_logic  # Renamed from game
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

# For demonstration, we'll just use the first player
current_player = players[0]


# Function to perform monthly updates
def monthly_update(companies, zones):
    for company in companies:
        # Generate gold for each triangle owned
        for zone_index in company.zones_owned:
            zone = zones[zone_index]
            company.gold += zone_stats.calculate_gold(zone)

        # Apply interest to loans
        for loan in company.loans:
            loan_amount, interest_rate, term = loan
            company.total_liabilities += loan_amount * interest_rate

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
        company = company_start_menu.company_creation_menu(current_player, screen)
        if company:
            companies.append(company)
            print(f"Company created: {company}")
        else:
            print("Failed to create company")
            return

        # Set up timer for monthly updates
        next_update_time = datetime.now() + timedelta(seconds=5)
        initial_setup_end_time = datetime.now() + timedelta(minutes=3)
        game_started = False

        while True:
            pygame.display.set_caption('Gold, Goop, and Gambling')

            # Regular game updates
            print("Running game updates")
            game_menu.main_game_menu(screen, current_player, vertices, faces, zones)
            vis.visualize_sphere_pygame(vertices, faces, zones, screen, current_player)

            if datetime.now() >= next_update_time:
                print("Performing monthly update")
                monthly_update(companies, zones)
                next_update_time = datetime.now() + timedelta(seconds=5)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
