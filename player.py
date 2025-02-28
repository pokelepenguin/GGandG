class Player:
    def __init__(self, player_id, name, spawn_zone_index):
        self.player_id = player_id
        self.name = name
        self.spawn_zone_index = spawn_zone_index  # Assign the player's spawn zone index
        self.personal_gold = 10000  # Starting personal funds
        self.companies = []         # Companies started by the player
        self.stocks = {}            # Holdings in various companies (company_id: shares)

    def __repr__(self):
        return f"Player(id={self.player_id}, name={self.name}, gold={self.personal_gold})"

    def add_company(self, company):
        self.companies.append(company)

    def buy_shares(self, company, shares):
        if company.company_id not in self.stocks:
            self.stocks[company.company_id] = 0
        self.stocks[company.company_id] += shares
        company.shareholders[self.player_id] = self.stocks[company.company_id]

    def sell_shares(self, company, shares):
        if company.company_id in self.stocks and self.stocks[company.company_id] >= shares:
            self.stocks[company.company_id] -= shares
            company.shareholders[self.player_id] = self.stocks[company.company_id]
            if self.stocks[company.company_id] == 0:
                del self.stocks[company.company_id]
                company.remove_shareholder(self)
