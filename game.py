from company import Company

company_counter = 1  # Global counter for company IDs

def generate_company_id():
    global company_counter
    company_id = f"C{company_counter}"
    company_counter += 1
    return company_id

def start_company(player, investment_amount, use_outside_investors, outside_investment_amount=0, company_name=None):
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

    # Assign the player's spawn zone to the company
    spawn_zone_index = player.spawn_zone_index  # Assume this attribute exists
    spawn_zone = game_zones[spawn_zone_index]   # Assume game_zones is a global list of zones
    spawn_zone.owner = company
    company.zones_owned.append(spawn_zone_index)

    player.companies.append(company)
    print(f"{player.name} started company {company.company_id} named {company.name} with investment {investment_amount} and outside investment {outside_investment_amount}.")
    return company

# Additional game logic functions...
