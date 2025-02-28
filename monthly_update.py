from time_tracker import time_tracker


def monthly_update(companies, zones, players):
    players_dict = {player.player_id: player for player in players}
    for company in companies:
        print(f"Updating company: {company.company_id}")
        company.update_triangle_income(zones)
        company.update_interest_expense()
        company.update_monthly_income_history()
        company.update_credit_score()
        company.distribute_dividends(players_dict)
        total_gold_earned = company.triangle_income  # Access the attribute directly
        total_gold_expenses = company.interest_expense + company.goop_upgrade_expense + company.patent_expense
        company.update_company_gold(total_gold_earned, total_gold_expenses)

    # Advance the in-game time by one month
    time_tracker.advance_month()
    print(f"Advanced time to: {time_tracker.get_current_time()}")