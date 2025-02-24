import pygame_menu

def loan_screen_menu(screen, player):
    menu = pygame_menu.Menu('Loan Screen', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    # Maximum loan amount
    max_loan_amount = player.companies[0].get_max_loan_amount()

    # Variables to store loan details
    loan_amount = [0]
    interest_rate = [0]
    monthly_payment = [0]

    # Function to update interest rate and monthly payment
    def update_loan_details(value):
        loan_amount[0] = value
        interest_rate[0] = calculate_interest_rate(loan_amount[0])
        monthly_payment[0] = calculate_monthly_payment(loan_amount[0], interest_rate[0])

        interest_label.set_title(f'Interest Rate: {interest_rate[0]:.2f}%')
        payment_label.set_title(f'Monthly Payment: {monthly_payment[0]:.2f} gold')

    # Function to calculate interest rate based on loan amount (example logic)
    def calculate_interest_rate(amount):
        base_rate = 5  # Base interest rate
        rate_increase = (amount / max_loan_amount) * 5  # Increase rate based on loan amount
        return base_rate + rate_increase

    # Function to calculate monthly payment (interest only)
    def calculate_monthly_payment(amount, rate):
        return amount * (rate / 100)

    # Function to create the loan and add it to the company
    def create_loan():
        loan_details = (loan_amount[0], interest_rate[0], 12)  # Assuming a 12-month term
        player.companies[0].loans.append(loan_details)
        print(f"Loan created: {loan_details}")
        return_to_main()

    # Add slider to menu
    menu.add.range_slider('Loan Amount: ', default=0, range_values=(0, max_loan_amount), increment=1, onchange=update_loan_details)

    # Add labels to display interest rate and monthly payment
    interest_label = menu.add.label(f'Interest Rate: {interest_rate[0]:.2f}%')
    payment_label = menu.add.label(f'Monthly Payment: {monthly_payment[0]:.2f} gold')

    # Add button to create loan
    menu.add.button('Create Loan', create_loan)

    def return_to_main():
        menu.disable()

    menu.add.button('Return to Main Menu', return_to_main)
    menu.mainloop(screen)
