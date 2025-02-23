import pygame_menu
import stock_market
import loan_screen
import tech_tree


def main_game_menu(screen):
    menu = pygame_menu.Menu('Main Menu', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Stock Market', lambda: stock_market.stock_market_menu(screen))
    menu.add.button('Loan Screen', lambda: loan_screen.loan_screen_menu(screen))
    menu.add.button('Tech Tree', lambda: tech_tree.tech_tree_menu(screen))
    menu.add.button('Return to Sphere', pygame_menu.events.BACK)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)
