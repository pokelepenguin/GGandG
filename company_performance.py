import pygame_menu
from player import Player
from company import Company

def company_performance_menu(screen, player):
    def set_dividend(value):
        try:
            player.companies[0].dividend = int(value)
        except ValueError:
            player.companies[0].dividend = 0

    menu = pygame_menu.Menu('Company Performance', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    # Revenue Section
    menu.add.label('Revenue')
    menu.add.label(f'Triangle Income: {player.companies[0].triangle_income}')
    menu.add.label(f'Rolling Yearly Income: {player.companies[0].get_rolling_yearly_income()}')
    menu.add.label(f'Patent Income: {player.companies[0].patent_income}')

    # Expense Section
    menu.add.label('Expenses')
    menu.add.label(f'Interest Expense: {player.companies[0].interest_expense}')
    menu.add.label(f'Goop Upgrade Expense: {player.companies[0].goop_upgrade_expense}')
    menu.add.label(f'Patent Expense: {player.companies[0].patent_expense}')

    # Total Section
    total_income_12 = player.companies[0].triangle_income + player.companies[0].get_rolling_yearly_income() + player.companies[0].patent_income
    menu.add.label(f"Rolling 12 Month Total Income: {total_income_12}")
    total_expense_12 = player.companies[0].interest_expense + player.companies[0].goop_upgrade_expense + player.companies[0].patent_expense
    menu.add.label(f"Rolling 12 Month Total Expense: {total_expense_12}")
    total_net_income_12 = total_income_12 - total_expense_12
    menu.add.label(f"Rolling 12 Month Net Income: {total_net_income_12}")


    # Modifiable Dividend Section
    menu.add.label('Dividend')
    menu.add.text_input('Set Dividend: ', default=str(player.companies[0].dividend), onchange=set_dividend)
    menu.add.button('Return to Main Menu', pygame_menu.events.BACK)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)