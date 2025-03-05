import pygame_menu
import pygame
from time_tracker import time_tracker

MONTHLY_UPDATE_EVENT = pygame.USEREVENT + 1

def company_performance_menu(screen, player, main_game_menu_callback, vertices, faces, zones):
    def set_dividend(value):
        try:
            rolling_net_income_12 = player.companies[0].triangle_income - (
                    player.companies[0].interest_expense + player.companies[0].goop_upgrade_expense + player.companies[0].patent_expense)
            max_dividend = rolling_net_income_12 / 12
            player.companies[0].dividend = min(int(value), max_dividend)
        except ValueError:
            player.companies[0].dividend = 0

    def refresh_menu():
        menu.clear()
        menu.add.label('Revenue')
        menu.add.label(f'Triangle Income: {player.companies[0].triangle_income:.2f}')
        menu.add.label(f'Patent Income: {player.companies[0].patent_income:.2f}')

        menu.add.label('Expenses')
        menu.add.label(f'Interest Expense: {player.companies[0].interest_expense:.2f}')
        menu.add.label(f'Goop Upgrade Expense: {player.companies[0].goop_upgrade_expense:.2f}')
        menu.add.label(f'Patent Expense: {player.companies[0].patent_expense:.2f}')

        total_income_12 = player.companies[0].triangle_income + player.companies[0].get_rolling_yearly_income() + player.companies[0].patent_income
        menu.add.label(f"Rolling 12 Month Total Income: {total_income_12:.2f}")
        total_expense_12 = player.companies[0].interest_expense + player.companies[0].goop_upgrade_expense + player.companies[0].patent_expense
        menu.add.label(f"Rolling 12 Month Total Expense: {total_expense_12:.2f}")
        total_net_income_12 = total_income_12 - total_expense_12
        menu.add.label(f"Rolling 12 Month Net Income: {total_net_income_12:.2f}")

        menu.add.label(f'Dividend: {player.companies[0].dividend}')

        def return_to_main():
            menu.disable()
            main_game_menu_callback(screen, player, vertices, faces, zones)

        menu.add.label(f"Company Gold: {player.companies[0].gold:.2f}")
        menu.add.label(f"Player Gold: {player.personal_gold:.2f}")
        menu.add.button('Return to Main Menu', return_to_main)
        menu.add.button('Quit', pygame_menu.events.EXIT)

    def draw_time():
        font = pygame.font.Font(None, 36)
        text = font.render(time_tracker.get_current_time(), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)
        pygame.draw.rect(screen, (0, 0, 0), text_rect)
        screen.blit(text, text_rect.topleft)

    menu = pygame_menu.Menu('Company Performance', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    clock = pygame.time.Clock()
    refresh_menu()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == MONTHLY_UPDATE_EVENT:
                refresh_menu()

            if event.type == pygame.QUIT:
                pygame.quit()
                return

        menu.update(events)
        menu.draw(screen)
        draw_time()
        pygame.display.flip()
        clock.tick(60)
