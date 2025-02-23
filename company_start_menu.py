import pygame_menu
import game_logic

def company_creation_menu(player, screen):
    menu = pygame_menu.Menu('Start a Company', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    investment = [player.personal_gold]  # Default investment to all personal gold
    use_outside_investors = [True]
    outside_investment_amount = [0]  # Default to 0
    company_name = [""]

    def set_investment(value):
        try:
            investment[0] = int(value)
            if investment[0] <= 0:
                raise ValueError("Investment amount must be greater than zero.")
            if investment[0] > player.personal_gold:
                raise ValueError("Investment amount must be equal or less than Player Gold")
            validate_outside_investment()
            update_labels()
        except ValueError as e:
            print(f"Invalid investment amount: {e}")
            investment[0] = 0
            investment_input.set_value('0')

    def set_outside_investors(value, bool_value):
        use_outside_investors[0] = bool_value
        if not bool_value:
            outside_investment_amount[0] = 0
        validate_outside_investment()
        update_labels()

    def set_outside_investment_amount(value):
        try:
            if use_outside_investors[0]:
                outside_investment_amount[0] = int(value)
                validate_outside_investment()
                update_labels()
        except ValueError as e:
            print(f"Invalid outside investment amount: {e}")
            outside_investment_amount[0] = 0
            outside_investment_input.set_value('0')

    def set_company_name(value):
        company_name[0] = value

    def validate_outside_investment():
        max_outside_investment = investment[0] * 3
        if outside_investment_amount[0] > max_outside_investment:
            outside_investment_amount[0] = max_outside_investment
            outside_investment_input.set_value(str(max_outside_investment))

        if not use_outside_investors[0]:
            outside_investment_amount[0] = 0
            outside_investment_input.set_value('0')

    def update_labels():
        player_ownership_percentage = round((investment[0] / (investment[0] + outside_investment_amount[0])) * 100, 2) if (investment[0] + outside_investment_amount[0]) > 0 else 100
        total_company_value = investment[0] + outside_investment_amount[0]
        player_ownership_label.set_title(f"Player Ownership: {player_ownership_percentage}%")
        company_value_label.set_title(f"Total Company Value: {total_company_value}")

    def submit():
        # Validate investment amount
        if investment[0] <= 0:
            print("Investment amount must be greater than zero.")
            return

        # Calculate outside investment amount
        outside_investment = outside_investment_amount[0] if use_outside_investors[0] else 0

        # Start company
        company = game_logic.start_company(player, investment[0], use_outside_investors[0], outside_investment, company_name[0])

        if company:
            print(f"Company {company.company_id} named {company.name} created successfully!")
            # Assign the spawn zone to the company
            spawn_zone = 0  # Assuming the first zone is the spawn zone
            print(f"Assigning spawn zone {spawn_zone} to company {company.company_id}")
            company.add_zone(spawn_zone)

        # Close the menu to proceed to the main game
        menu.disable()

    # Add widgets to the menu
    menu.add.label(f"Available Personal Gold: {player.personal_gold}")
    investment_input = menu.add.text_input('Investment Amount: ', default=str(player.personal_gold), onchange=set_investment)
    menu.add.selector('Use Outside Investors: ', [('Yes', True), ('No', False)], default=0, onchange=set_outside_investors)
    outside_investment_input = menu.add.text_input('Outside Investment Amount: ', default='0', onchange=set_outside_investment_amount)
    menu.add.text_input('Company Name: ', default='', onchange=set_company_name)
    player_ownership_label = menu.add.label('Player Ownership: 100%')
    company_value_label = menu.add.label('Total Company Value: 0')
    menu.add.button('Submit', submit)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)