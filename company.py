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
