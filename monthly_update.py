def monthly_update(companies, zones, players):
    for company in companies:
        print(f"Updating company: {company.company_id}")
        # Generate gold for each triangle owned
        company.update_triangle_income(zones)

        # Apply interest to loans
        company.update_interest_expense()

        # Update monthly income history
        company.update_monthly_income_history()

        # Update credit score
        company.update_credit_score()

        # Calculate and distribute dividends
        company.distribute_dividends(players)

        # Update company gold
        total_gold_earned = company.triangle_income(zones) # Assuming this is the total gold earned this month
        total_gold_expenses = company.interest_expense + company.goop_upgrade_expense + company.patent_expense
        company.update_company_gold(total_gold_earned, total_gold_expenses)