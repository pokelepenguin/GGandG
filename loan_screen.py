import pygame_menu

def loan_screen_menu(screen):
    menu = pygame_menu.Menu('Loan Screen', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    def take_loan(amount, interest_rate):
        # Logic for taking a loan
        pass

    def repay_loan(amount):
        # Logic for repaying a loan
        pass

    loan_amount = [0]  # Default loan amount
    interest_rate = [0]  # Default interest rate

    menu.add.text_input('Loan Amount: ', default=str(loan_amount[0]), onchange=lambda value: loan_amount.__setitem__(0, int(value)))
    menu.add.text_input('Interest Rate: ', default=str(interest_rate[0]), onchange=lambda value: interest_rate.__setitem__(0, float(value)))
    menu.add.button('Take Loan', lambda: take_loan(loan_amount[0], interest_rate[0]))
    menu.add.button('Repay Loan', lambda: repay_loan(loan_amount[0]))
    menu.add.button('Return to main menu', pygame_menu.events.BACK)

    menu.mainloop(screen)
