import pygame_menu
import pygame
from time_tracker import time_tracker

MONTHLY_UPDATE_EVENT = pygame.USEREVENT + 1

def loan_screen_menu(screen, player, main_game_menu_callback, vertices, faces, zones):
    menu = pygame_menu.Menu('View Loans', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    # Function to display loans
    def display_loans():
        for loan in player.companies[0].loans:
            menu.add.label(f"Loan Amount: {loan['amount']:.2f} gold")
            menu.add.label(f"Interest Rate: {loan['interest_rate']:.2f}%")
            menu.add.label(f"Term: {loan['term']} years")
            menu.add.vertical_margin(10)

    # Display current loans
    display_loans()
    menu.add.button('Return to Main Menu', lambda: main_game_menu_callback(screen, player, vertices, faces, zones))

    def draw_time(screen):
        font = pygame.font.Font(None, 36)
        text = font.render(time_tracker.get_current_time(), True, (255, 255, 255))
        screen.blit(text, (screen.get_width() - text.get_width() - 10, screen.get_height() - text.get_height() - 10))

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
