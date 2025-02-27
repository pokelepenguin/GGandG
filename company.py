from credit_score import CreditTier, calculate_credit_score
from interest_rate import calculate_interest_rate
import zone_stats

class Company:
    def __init__(self, company_id, founder, initial_investment, public=False, outside_investment_amount=0):
        print(f"Creating company with ID: {company_id}")
        self.company_id = company_id
        self.founder = founder  # Player object
        self.gold = initial_investment
        self.zones_owned = []  # List of zone indices owned
        self.shares_outstanding = 1000  # Total shares
        self.share_price = initial_investment / self.shares_outstanding
        self.shareholders = {}  # Mapping of player_id to shares
        self.public = public  # True if outside investors are involved
        self.loans = []
        self.research_level = 0
        self.goop_inventory = 0
        self.total_assets = initial_investment
        self.total_liabilities = 0
        self.credit_score = CreditTier.B  # Default credit score

        # New attributes for company performance screen
        self.triangle_income = 0
        self.patent_income = 0
        self.interest_expense = 0
        self.goop_upgrade_expense = 0
        self.patent_expense = 0
        self.dividend = 0

        self.monthly_income_history = []

        # Assign shares to founder and outside investors
        if public:
            total_investment = initial_investment + outside_investment_amount
            founder_shares = self.shares_outstanding * (initial_investment / total_investment)
            self.shareholders[founder.player_id] = founder_shares
            # Remaining shares held by outside investors (abstracted)
            self.shareholders['public'] = self.shares_outstanding - founder_shares
        else:
            # Founder owns all shares
            self.shareholders[founder.player_id] = self.shares_outstanding

        print(f"Company created: {self}")

    def __repr__(self):
        return f"Company(id={self.company_id}, founder={self.founder.name}, gold={self.gold})"

    def update_credit_score(self):
        self.credit_score = calculate_credit_score(self)

    def issue_stock(self, amount):
        self.total_assets += amount
        self.update_credit_score()

    def take_loan(self, amount, term):
        if amount > self.get_max_loan_amount():
            raise ValueError("Loan amount exceeds the maximum allowable limit.")

        interest_rate = calculate_interest_rate(self, amount, term)
        self.loans.append((amount, interest_rate, term))
        self.total_liabilities += amount
        self.update_credit_score()
        self.update_interest_expense()

    def repay_loan(self, amount):
        if self.loans:
            loan_amount, interest_rate, term = self.loans.pop(0)
            self.total_liabilities -= loan_amount
            self.update_credit_score()
            self.update_interest_expense()

    def get_max_loan_amount(self):
        return 0.5 * (self.total_assets - self.total_liabilities)

    def add_zone(self, zone_index):
        if zone_index not in self.zones_owned:
            self.zones_owned.append(zone_index)
            print(f"Zone {zone_index} added to company {self.company_id}")
        else:
            print(f"Zone {zone_index} is already owned by company {self.company_id}")

    def update_triangle_income(self, zones):
        self.triangle_income = sum(zone_stats.calculate_gold(zones[zone_index]) for zone_index in self.zones_owned)

    def update_interest_expense(self):
        self.interest_expense = sum(loan["amount"] * loan["interest_rate"] / 1200 for loan in self.loans)

    def update_monthly_income_history(self):
        self.monthly_income_history.append(self.triangle_income)  # Add current month's income
        if len(self.monthly_income_history) > 12:
            self.monthly_income_history.pop(0)  # Remove income from 13 months ago

    def get_rolling_yearly_income(self):
        return sum(self.monthly_income_history)

    def calculate_dividend(self):
        total_dividend = self.dividend * self.shares_outstanding
        return total_dividend

    def distribute_dividends(self, players):
        total_dividend = self.calculate_dividend()
        for player_id, shares in self.shareholders.items():
            if player_id in players:
                players[player_id].personal_gold += total_dividend * (shares / self.shares_outstanding)

    def update_company_gold(self, total_gold_earned, total_gold_expenses):
        total_dividend = self.calculate_dividend()
        self.gold = self.gold + total_gold_earned - total_gold_expenses - total_dividend