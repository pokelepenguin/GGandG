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

