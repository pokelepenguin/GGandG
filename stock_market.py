import pygame_menu
import pygame
from time_tracker import time_tracker

MONTHLY_UPDATE_EVENT = pygame.USEREVENT + 1

def stock_market_menu(screen, player, main_game_menu_callback, vertices, faces, zones):
    def set_dividend(value):
        try:
            rolling_net_income_12 = player.companies[0].triangle_income - (
                    player.companies[0].interest_expense + player.companies[0].goop_upgrade_expense + player.companies[0].patent_expense)
            max_dividend = rolling_net_income_12 / 12
            player.companies[0].dividend = min(int(value), max_dividend)
        except ValueError:
            player.companies[0].dividend = 0

    menu = pygame_menu.Menu('Stock Market', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    def refresh_menu():
        menu.clear()

        this_month_net_income = player.companies[0].triangle_income - (
            player.companies[0].interest_expense + player.companies[0].goop_upgrade_expense + player.companies[0].patent_expense)
        menu.add.label(f"This Month Net Income: {this_month_net_income:.2f}")

        total_income_12 = player.companies[0].triangle_income + player.companies[0].get_rolling_yearly_income() + player.companies[0].patent_income
        total_expense_12 = player.companies[0].interest_expense + player.companies[0].goop_upgrade_expense + player.companies[0].patent_expense
        total_net_income_12 = total_income_12 - total_expense_12
        menu.add.label(f"Rolling 12 Month Net Income: {total_net_income_12:.2f}")

        menu.add.label('Dividend')
        # Add slider to menu
        menu.add.range_slider('Monthly Dividend: ', default=0, range_values=(0, this_month_net_income), increment=1, onchange=set_dividend)

        def return_to_main():
            menu.disable()
            main_game_menu_callback(screen, player, vertices, faces, zones)

        menu.add.label(f"Company Gold: {player.companies[0].gold:.2f}")
        menu.add.label(f"Player Gold: {player.personal_gold:.2f}")
        menu.add.button('Return to Main Menu', return_to_main)
        menu.add.button('Quit', pygame_menu.events.EXIT)

    def draw_time(screen):
        font = pygame.font.Font(None, 36)
        text = font.render(time_tracker.get_current_time(), True, (255, 255, 255))
        screen.blit(text, (screen.get_width() - text.get_width() - 10, screen.get_height() - text.get_height() - 10))

    clock = pygame.time.Clock()
    refresh_menu()

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