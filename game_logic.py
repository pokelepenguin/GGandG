from company import Company

company_counter = 1  # Global counter for company IDs

def generate_company_id():
    global company_counter
    company_id = f"C{company_counter}"
    company_counter += 1
    return company_id

def start_company(player, investment_amount, use_outside_investors, outside_investment_amount=0, company_name=None, zones=None):
    print(f"Starting company for player {player.name} with investment {investment_amount} and outside investment {outside_investment_amount}")
    min_investment = 1000  # Define minimum investment required
    if investment_amount < min_investment:
        print(f"Minimum investment amount is {min_investment}.")
        return None
    if investment_amount > player.personal_gold:
        print("You don't have enough personal gold to invest that amount.")
        return None
    if use_outside_investors and outside_investment_amount > investment_amount * 3:
        print("Outside investment cannot exceed three times the player's investment amount.")
        return None

    # Calculate total investment
    if use_outside_investors:
        total_investment = investment_amount + outside_investment_amount
        public = True
    else:
        total_investment = investment_amount
        public = False

    player.personal_gold -= investment_amount

    company_id = generate_company_id()
    if not company_name:
        company_name = f"GGG_{company_counter - 1} LLC"  # Default name format

    company = Company(company_id, player, total_investment, public, outside_investment_amount)
    company.name = company_name

    # Check if zones is not None
    if zones is None:
        print("Error: zones is None")
        return None

    # Assign the player's spawn zone to the company
    spawn_zone_index = player.spawn_zone_index  # Assume this attribute exists
    if spawn_zone_index >= len(zones):
        print(f"Error: Invalid spawn_zone_index {spawn_zone_index}")
        return None

    spawn_zone = zones[spawn_zone_index]  # Use the zones parameter
    spawn_zone.owner = company
    company.zones_owned.append(spawn_zone_index)

    player.companies.append(company)
    print(f"{player.name} started company {company.company_id} named {company.name} with investment {investment_amount} and outside investment {outside_investment_amount}.")
    return company

# Additional game logic functions...
