import random
from company import Company
from player import Player
from zone_stats import Zone  # Adjust import based on your project structure

company_counter = 1  # Global counter for company IDs

def generate_company_id():
    global company_counter
    company_id = f"C{company_counter}"
    company_counter += 1
    return company_id

def start_company(player, investment_amount, use_outside_investors):
    min_investment = 1000  # Define minimum investment required
    if investment_amount < min_investment:
        print(f"Minimum investment amount is {min_investment}.")
        return None
    if investment_amount > player.personal_gold:
        print("You don't have enough personal gold to invest that amount.")
        return None

    # Calculate total investment
    if use_outside_investors:
        outside_investment = investment_amount * 3
        total_investment = investment_amount + outside_investment
        public = True
    else:
        total_investment = investment_amount
        public = False

    player.personal_gold -= investment_amount

    company_id = generate_company_id()
    company = Company(company_id, player, total_investment, public)

    # Assign the player's spawn zone to the company
    spawn_zone_index = player.spawn_zone_index  # Assume this attribute exists
    spawn_zone = game_zones[spawn_zone_index]   # Assume game_zones is a global list of zones
    spawn_zone.owner = company
    company.zones_owned.append(spawn_zone_index)

    player.companies.append(company)
    print(f"{player.name} started company {company.company_id} with investment {investment_amount}.")
    return company

# Additional game logic functions...
