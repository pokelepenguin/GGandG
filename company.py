from credit_score import CreditTier, calculate_credit_score
from interest_rate import calculate_interest_rate


class Company:
    def __init__(self, company_id, founder, initial_investment, public=False, outside_investment_amount=0):
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

    def repay_loan(self, amount):
        if self.loans:
            loan_amount, interest_rate, term = self.loans.pop(0)
            self.total_liabilities -= loan_amount
            self.update_credit_score()

    def get_max_loan_amount(self):
        return 0.5 * self.total_assets