import pygame_menu


def tech_tree_menu(screen, player):
    menu = pygame_menu.Menu('Tech Tree', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    # Add tech tree options here

    def return_to_main():
        menu.disable()

    menu.add.button('Return to Main Menu', return_to_main)
    menu.mainloop(screen)
