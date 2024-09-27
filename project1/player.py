class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.ships = None
        self.sunk_ships = []
        self.hits = []
        self.attack_grid = [[None for _ in range(10)] for _ in range(10)]

    def all_ships_sunk(self, player_ships):
        return all(self.check_ship_sunk(ship) for ship in player_ships)
    
    def check_ship_sunk(self, ship):
        # Logic to check if a ship is sunk
        return 0

    def update_sunk_ships(self, opponent_sunk_ships):
        self.sunk_ships = opponent_sunk_ships