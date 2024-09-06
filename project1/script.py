# Need another for player 2
attacked1 = []
attacked2 = []
for i in range(10):
	attacked1.append([False]*10)
	attacked2.append([False]*10)

ships1 = []
ships2 = []

def is_on_a_ship(ships, x, y):
	for ship in ships:
		for coord in ship:
			if coord[0] == x and coord[1] == y:
				return True
	return False

def is_sunk(ship):
	for coord in ship:
		if not missiles[coord[0], coord[1]]:
			return False
	return True

