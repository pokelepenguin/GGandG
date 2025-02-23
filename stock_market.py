import pygame_menu


def stock_market_menu(screen, player):
    menu = pygame_menu.Menu('Stock Market', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    # Add stock market options here

    def return_to_main():
        menu.disable()

    menu.add.button('Return to Main Menu', return_to_main)
    menu.mainloop(screen)