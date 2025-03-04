import pygame_menu
import pygame
import stock_market
import loan_screen
import tech_tree
import spherey_visualization as vis
from company_performance import company_performance_menu
from time_tracker import time_tracker

MONTHLY_UPDATE_EVENT = pygame.USEREVENT + 1

def main_game_menu(screen, player, vertices, faces, zones):
    def return_to_sphere():
        screen.fill((0, 0, 0))
        vis.visualize_sphere_pygame(vertices, faces, zones, screen, player)

    def draw_time(screen):
        font = pygame.font.Font(None, 36)
        text = font.render(time_tracker.get_current_time(), True, (255, 255, 255))
        screen.blit(text, (screen.get_width() - text.get_width() - 10, screen.get_height() - text.get_height() - 10))

    menu = pygame_menu.Menu('Main Menu', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Stock Market', lambda: stock_market.stock_market_menu(screen, player, main_game_menu))
    menu.add.button('Loans', lambda: loan_screen.loan_screen_menu(screen, player, main_game_menu))
    menu.add.button('Tech Tree', lambda: tech_tree.tech_tree_menu(screen, player))
    menu.add.button('Company Performance', lambda: company_performance_menu(screen, player, main_game_menu))
    menu.add.button('Return to Sphere', return_to_sphere)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == MONTHLY_UPDATE_EVENT:
                screen.fill((0, 0, 0))
                menu.update(events)
                menu.draw(screen)
                draw_time(screen)
                pygame.display.flip()

            if event.type == pygame.QUIT:
                pygame.quit()
                return

        menu.update(events)
        menu.draw(screen)
        draw_time(screen)
        pygame.display.flip()
        clock.tick(60)
