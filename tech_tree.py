import pygame_menu

def tech_tree_menu(screen):
    menu = pygame_menu.Menu('Tech Tree', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    def unlock_technology(tech_name):
        # Logic for unlocking a technology
        pass

    tech_name = [""]  # Default technology name

    menu.add.text_input('Technology Name: ', default=tech_name[0], onchange=lambda value: tech_name.__setitem__(0, value))
    menu.add.button('Unlock', lambda: unlock_technology(tech_name[0]))
    menu.add.button('Return to main menu', pygame_menu.events.BACK)

    menu.mainloop(screen)
