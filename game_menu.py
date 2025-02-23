import pygame_menu
import stock_market
import loan_screen
import tech_tree
import spherey_visualization as vis


def main_game_menu(screen, player, vertices, faces, zones):
    def return_to_sphere():
        screen.fill((0, 0, 0))
        vis.visualize_sphere_pygame(vertices, faces, zones, screen, player)

    menu = pygame_menu.Menu('Main Menu', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Stock Market', lambda: stock_market.stock_market_menu(screen, player))
    menu.add.button('Loan Screen', lambda: loan_screen.loan_screen_menu(screen, player))
    menu.add.button('Tech Tree', lambda: tech_tree.tech_tree_menu(screen, player))
    menu.add.button('Return to Sphere', return_to_sphere)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)
