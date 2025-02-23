import pygame_menu


def loan_screen_menu(screen, player):
    menu = pygame_menu.Menu('Loan Screen', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    # Add loan screen options here

    def return_to_main():
        menu.disable()

    menu.add.button('Return to Main Menu', return_to_main)
    menu.mainloop(screen)
