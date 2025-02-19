import pygame
import pygame_menu
from player import Player
from company import Company
import game


def company_creation_menu(player, screen):
    pygame.init()
    menu = pygame_menu.Menu('Start a Company', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    investment = [1000]  # Default investment
    use_outside_investors = [False]

    def set_investment(value):
        investment[0] = int(value)

    def set_outside_investors(value, bool_value):
        use_outside_investors[0] = bool_value

    def submit():
        # Validate investment amount
        if investment[0] <= 0:
            print("Investment amount must be greater than zero.")
            return

        # Start company
        company = game.start_company(player, investment[0], use_outside_investors[0])

        if company:
            print(f"Company {company.company_id} created successfully!")

        # Proceed to the main game
        pygame.quit()
        # Here you would call the main game function

    # Add widgets to the menu
    menu.add.label(f"Available Personal Gold: {player.personal_gold}")
    menu.add.range_slider('Investment Amount: ', default=1000, range_values=(1000, player.personal_gold), increment=500, onchange=set_investment)
    menu.add.selector('Use Outside Investors: ', [('Yes', True), ('No', False)], default=1, onchange=set_outside_investors)
    menu.add.button('Submit', submit)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)

