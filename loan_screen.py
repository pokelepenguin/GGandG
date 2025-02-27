import pygame_menu

def loan_screen_menu(screen, player):
    menu = pygame_menu.Menu('Loan Screen', 600, 400, theme=pygame_menu.themes.THEME_DARK)

    loan_details = {
        'loan_amount': 0,
        'interest_rate': 0,
        'monthly_payment': 0,
        'term': 5  # Default term of 5 years
    }

    # Maximum loan amount
    max_loan_amount = player.companies[0].get_max_loan_amount()

    # Function to update interest rate and monthly payment
    def update_loan_details(value, term):
        loan_details['loan_amount'] = value
        loan_details['term'] = term
        loan_details['interest_rate'] = calculate_interest_rate(loan_details['loan_amount'], loan_details['term'])
        loan_details['monthly_payment'] = calculate_monthly_payment(loan_details['loan_amount'], loan_details['interest_rate'])

        interest_label.set_title(f'Interest Rate: {loan_details["interest_rate"]:.2f}%')
        payment_label.set_title(f'Monthly Payment: {loan_details["monthly_payment"]:.2f} gold')

    # Function to calculate interest rate based on loan amount and term
    def calculate_interest_rate(amount, term):
        base_rate = 5  # Base interest rate
        rate_increase = (amount / max_loan_amount) * 5  # Increase rate based on loan amount
        term_increase = 0
        if term == 10:
            term_increase = 0.75
        elif term == 25:
            term_increase = 1.5
        return base_rate + rate_increase + term_increase

    # Function to calculate monthly payment (interest only)
    def calculate_monthly_payment(amount, rate):
        return amount * (rate / 100) / 12

    # Function to create the loan and add it to the company
    def create_loan():
        loan = {
            'amount': loan_details['loan_amount'],
            'interest_rate': loan_details['interest_rate'],
            'term': loan_details['term']
        }
        player.companies[0].loans.append(loan)
        print(f"Loan created: {loan}")
        update_interest_expense()
        return_to_main()

    # Function to update the total interest expense for the company
    def update_interest_expense():
        total_interest_expense = sum(loan['amount'] * (loan['interest_rate'] / 100) / 12 for loan in player.companies[0].loans)
        player.companies[0].interest_expense = total_interest_expense

    # Add slider to menu
    menu.add.range_slider('Loan Amount: ', default=0, range_values=(0, max_loan_amount), increment=1, onchange=lambda value: update_loan_details(value, loan_details['term']))

    # Add selector for loan term
    menu.add.selector('Loan Term: ', [('5 years', 5), ('10 years', 10), ('25 years', 25)], onchange=lambda _, term: update_loan_details(loan_details['loan_amount'], term))

    # Add labels to display interest rate and monthly payment
    interest_label = menu.add.label(f'Interest Rate: {loan_details["interest_rate"]:.2f}%')
    payment_label = menu.add.label(f'Monthly Payment: {loan_details["monthly_payment"]:.2f} gold')

    # Add button to create loan
    menu.add.button('Create Loan', create_loan)

    def return_to_main():
        menu.disable()

    menu.add.button('Return to Main Menu', return_to_main)
    menu.mainloop(screen)
